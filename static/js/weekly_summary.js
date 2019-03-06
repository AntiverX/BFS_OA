/*
初始时保存一份空白的表
初始时禁用提交按钮
点击主界面左下角添加按钮
对json进行处理
添加按钮实现
修改按钮实现
提交按钮实现
点击加号增加表单
表单验证（服务端验证和本地验证）
*/
$(document).ready(function () {
    /* 初始时保存一份空白的表 */
    empty_form = $(".all_record").clone(true);

    /* 初始时禁用提交按钮 */
    $("#submitForm").attr("disabled", true);

    /* 点击主界面左下角添加按钮 */
    $("#add").click(function () {
        $("#addForm").click();
    });

    /* 表格项目被右击后，记录被右击的表格id */
    $('tr').mousedown(function (event) {
        if (event.which == 3) {
            active_table = this.title;
        }
    });

    /* 右键菜单的相关实现 */
    $.contextMenu({
        // define which elements trigger this menu
        selector: ".table_content",
        // define the elements of the menu
        items: {
            add: {
                name: "添加",
                icon: "add",
                callback: function (key, opt) {
                    $("#addForm").click();
                }
            },
            modify: {
                name: "修改",
                icon: "edit",
                callback: function (key, opt) {
                    $("#modifyForm").click();
                }
            },
            separator1: "-----",
            delete: {
                name: "删除",
                icon: "delete",
                callback: function () {
                    csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
                    data = {
                        "target_id": active_table,
                        csrfmiddlewaretoken: csrftoken,
                        "btn": "delete"
                    }
                    $.post("/topic_manager/weekly_summary", data, function (response, status) {
                        if (status == "success") {
                            window.location.reload(true);
                        }
                    });
                }
            }
        },
        events: {
            show: function () {
                $('tr[title=' + active_table + ']').addClass("table-active");
            },
            hide: function () {
                $('tr[title=' + active_table + ']').removeClass("table-active");
            }
        }
    });
    /* 右键菜单的相关实现结束 */

    /* 对json进行处理，分行显示本周和下周工作 */
    $("tr").each(function () {
        if ($(this).find("td").length != 0) {
            var array_ = JSON.parse($(this).find("td").eq(-1).text());
            new_text = "";
            for (var i = 0; i < array_.length - 1; i++) {
                new_text = new_text + array_[i] + "\n";
            }
            new_text = new_text + array_[array_.length - 1];
            $(this).find("td").eq(-1).text(new_text);
        }
    });
    $("tr").each(function () {
        if ($(this).find("td").length != 0) {
            var array_ = JSON.parse($(this).find("td").eq(-2).text());
            new_text = "";
            for (var i = 0; i < array_.length - 1; i++) {
                new_text = new_text + array_[i] + "\n";
            }
            new_text = new_text + array_[array_.length - 1];
            $(this).find("td").eq(-2).text(new_text);
        }
    });


    /* 点击添加按钮 */
    $("#addForm").click(function () {
        $.get("/get_current_week", function (data) {
            $("#week").val(data);
        });
        $("#week").addClass("is-valid");
        $("#absent_hour").addClass("is-valid");
        $("#form").replaceWith(empty_form);
        if ($("tr").hasClass("table-active")) {
            $("tr").removeClass("table-active");
        }
        active_table = "";
    });

    /* 修改按钮相关实现 */
    $("#modifyForm").click(function () {
        console.log("修改按钮触发");
        $("#form").replaceWith(empty_form);
        var target_id = active_table;
        var week = $("tr[title=" + target_id + "]").find("td").eq(0).text();
        var average_work_hour = $("tr[title=" + target_id + "]").find("td").eq(2).text();
        var absent_hour = $("tr[title=" + target_id + "]").find("td").eq(3).text();
        var this_week_task = $("tr[title=" + target_id + "]").find("td").eq(4).text();
        var next_week_task = $("tr[title=" + target_id + "]").find("td").eq(5).text();
        var this_week_task_split = this_week_task.split("\n");
        var next_week_task_split = next_week_task.split("\n");
        for (var i = 0; i < this_week_task_split.length - 1; i++) {
            element_ = $(".this_week_work:first").clone(true);
            $(element_).find("input").val("");
            element_.appendTo(".all_this_week_work");
        }
        for (var i = 0; i < next_week_task_split.length - 1; i++) {
            element_ = $(".next_week_work:first").clone(true);
            $(element_).find("input").val("");
            element_.appendTo(".all_next_week_work");
            console.log("增加了一个下周工作");
        }
        $("#week").val(week);
        $("#average_work_hour").val(average_work_hour);
        $("#absent_hour").val(absent_hour);
        for (var i = 0; i < this_week_task_split.length; i++) {
            $(".this_week_task").eq(i).val(this_week_task_split[i]);
        }
        for (var i = 0; i < next_week_task_split.length; i++) {
            $(".next_week_task").eq(i).val(next_week_task_split[i]);
        }
        /* 点击修改按钮后使得所有的内容都is-valid */
        $("input").each(function () {
            $(this).addClass("is-valid");
        });

    });

    /* 提交按钮相关功能实现 */
    $("#submitForm").click(function () {
        /* 获取输入的本周工作 */
        var this_week_task = [];
        $(".this_week_task").each(function () {
            item = {};
            item['this_week_task'] = $(this).val();
            this_week_task.push($(this).val());
        });
        /* 获取输入的下周工作 */
        var next_week_task = [];
        $(".next_week_task").each(function () {
            item = {};
            item['next_week_task'] = $(this).val();
            next_week_task.push($(this).val());
        });
        var jsonString_this_week_task = JSON.stringify(this_week_task);
        var jsonString_next_week_task = JSON.stringify(next_week_task);
        csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        var data = {
            "target_id": active_table,
            "this_week_task": jsonString_this_week_task,
            "next_week_task": jsonString_next_week_task,
            'week': $("#week").val(),
            'average_work_hour': $("#average_work_hour").val(),
            'absent_hour': $("#absent_hour").val(),
            csrfmiddlewaretoken: csrftoken,
            "btn": ""
        }
        $.post("/topic_manager/weekly_summary", data, function (response, status) {
            if (status == "success") {
                window.location.reload(true);
            }
        });
    });

    /* 点击加号按钮，会自动增加 */
    $("#add_this_week_work").click(function () {
        element_ = $(".this_week_work:first").clone(true);
        $(element_).find("input").val("");
        $(element_).find("input").removeClass("is-valid");
        $(element_).find("input").removeClass("is-invalid");
        element_.appendTo(".all_this_week_work");
        $("#submitForm").attr("disabled", true);
    });
    $("#add_next_week_work").click(function () {
        element_ = $(".next_week_work:first").clone(true);
        $(element_).find("input").val("");
        $(element_).find("input").removeClass("is-valid");
        $(element_).find("input").removeClass("is-invalid");
        element_.appendTo(".all_next_week_work");
        $("#submitForm").attr("disabled", true);
    });

    /* 表单验证 */
    $(document).on('change', 'input', function () {
        /* 在线验证表单内容 */
        text = $(this).val();
        class_name = $(this).attr('class').split(" ")[0];
        csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        parent = $(this);
        data = {
            class_name: class_name,
            value: text,
            'csrfmiddlewaretoken': csrftoken
        }
        $.post('/topic_manager/valid', data, function (result) {

            if (result == "OK") {
                parent.removeClass("is-invalid");
                parent.addClass("is-valid");
            } else {
                $("#" + class_name + "-invalid").text(result);
                parent.removeClass("is-valid");
                parent.addClass("is-invalid");
                $("#submitForm").attr("disabled", true);
            }
        });

        /* 客户端验证是否有缺失内容 */
        var form_complete = 1;
        $("input").each(function () {

            if (($(this).val() == "")) {
                if ($(this).attr("id") != "target_id") {
                    form_complete = 0;
                }
            }
        });
        if (form_complete) {
            $("#submitForm").attr("disabled", false);
        } else {
            $("#submitForm").attr("disabled", true);
        }
    });
});