/*
初始时保存一份空白的表
初始时禁用提交按钮
点击主界面左下角添加按钮
表格项目被右击后，记录被右击的表格id
右键菜单的相关实现
对json进行处理，分行显示主题和主题内容说明
* 删除按钮实现
* 修改按钮实现
* 添加按钮实现
* 提交按钮实现
* 点击加号增加表单
* 表单验证（服务端验证和本地验证）

* */

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
                        'date': "",
                        'semester': "",
                        "expected_result": "",
                        "time_consumed": "",
                        "content": "",
                        "end_of_term_summary": "",
                        csrfmiddlewaretoken: csrftoken,
                        "btn": "delete"
                    }
                    $.post("/topic_manager/meeting_record", data, function (response, status) {
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

    /* 对json进行处理，分行显示主题和主题内容说明 */
    $("tr").each(function () {

        if ($(this).find("td").length != 0) {
            var array_ = JSON.parse($(this).find("td").eq(-1).text());
            theme_content = "";
            for (var i = 0; i < array_.length - 1; i++) {
                theme_content = theme_content + array_[i] + "\n\n";
            }
            theme_content = theme_content + array_[array_.length - 1];
            $(this).find("td").eq(-1).text(theme_content);
        }

        /* 对主题内容说明进行处理 */
        var theme_content_length = new Array();
        if ($(this).find("td").length != 0) {
            var array_ = JSON.parse($(this).find("td").eq(-2).text());
            new_text = "";
            for (var i = 0; i < array_.length - 1; i++) {
                new_text = new_text + array_[i].trim() + "\n\n";
                console.log(array_[i].trim());
                theme_content_length[i] = array_[i].trim().split("\n").length;
            }
            new_text = new_text + array_[array_.length - 1].trim();
            theme_content_length[array_.length - 1] = array_[array_.length - 1].trim().split("\n").length;
            $(this).find("td").eq(-2).text(new_text);
            console.log(theme_content_length);
        }

        if ($(this).find("td").length != 0) {
            var array_ = JSON.parse($(this).find("td").eq(-3).text());
            new_text = "";
            for (var i = 0; i < array_.length - 1; i++) {
                new_text = new_text + array_[i] + "\n\n";
                for (var j = 0; j < theme_content_length[i] - 1; j++) {
                    new_text = new_text + "\n";
                }
            }
            new_text = new_text + array_[array_.length - 1];
            $(this).find("td").eq(-3).text(new_text);
        }
    });
    /* 对json进行处理，分行显示主题和主题内容说明结束 */

    /* 删除按钮相关功能实现 */
    $("#deleteForm").click(function () {
        data = {
            "target_id": active_table,
            csrfmiddlewaretoken: jQuery("[name=csrfmiddlewaretoken]").val(),
            "btn": "delete"
        }
        $.post("/topic_manager/meeting_record", data, function (response, status) {
            if (status == "success") {
                window.location.reload(true);
            }
        });
    });

    /* 修改按钮相关实现 */
    $("#modifyForm").click(function () {
        console.log("修改按钮触发");
        /*清空原有记录*/
        $(".all_record").replaceWith(empty_form);

        /* 获得要修改记录的值 */
        var target_id = active_table;
        var date = $("tr[title=" + target_id + "]").find("td").eq(0).text();
        var time = $("tr[title=" + target_id + "]").find("td").eq(1).text();
        var cost_time = $("tr[title=" + target_id + "]").find("td").eq(2).text();
        var place = $("tr[title=" + target_id + "]").find("td").eq(3).text();
        var theme = $("tr[title=" + target_id + "]").find("td").eq(4).text();
        var theme_content = $("tr[title=" + target_id + "]").find("td").eq(5).text();
        var remark = $("tr[title=" + target_id + "]").find("td").eq(6).text();
        var theme_split = theme.split("\n\n");
        var theme_content_split = theme_content.split("\n\n");
        var remark_split = remark.split("\n\n");
        for (var i = 0; i < theme_split.length - 1; i++) {
            element_ = $(".record:first").clone(true);
            $(element_).find("input").val("");
            element_.appendTo(".all_record");
        }

        /* 赋值 */
        $("#date").val(date);
        $("#time").val(time);
        $("#cost_time").val(cost_time);
        $("#place").val(place);
        for (var i = 0; i < theme_split.length; i++) {
            $(".theme").eq(i).val(theme_split[i]);
            $(".theme_content").eq(i).val(theme_content_split[i]);
            $(".remark").eq(i).val(remark_split[i]);
        }

        /* 所有的内容都是OK的 */
        $(".form").find("input").addClass("is-valid");
        $(".form").find("textarea").addClass("is-valid");
    });

    /* 点击添加按钮 */
    $("#addForm").click(function () {
        active_table = "";
        $("#form").find("input").val("");
        /* 设置日期时间 */
        var date = new Date();
        var year = date.getFullYear();
        var month = date.getMonth() + 1;
        var day = date.getDate();
        $("#date").val(year + "-" + month + "-" + day);
        $("#time").val(date.getHours() + ":" + date.getMinutes());
        $("#cost_time").val("");
        $("#cost_time").removeClass("is-valid");
        $("#cost_time").removeClass("is-invalid");
        $("#place").val("10#420");
        $("#date").addClass("is-valid");
        $("#time").addClass("is-valid");
        $("#place").addClass("is-valid");
        /* 除表头外，其他内容清空 */
        $(".all_record").replaceWith(empty_form);
        if ($("tr").hasClass("table-active")) {
            $("tr").removeClass("table-active");
        }
    });

    /* 提交按钮相关功能实现 */
    $("#submitForm").click(function () {
        /* 获取所有主题 */
        var theme = [];
        $(".theme").each(function () {
            item = {};
            item['theme'] = $(this).val();
            theme.push($(this).val());
        });
        /* 获取所有主题内容说明 */
        var theme_content = [];
        $(".theme_content").each(function () {
            item = {};
            item['theme_content'] = $(this).val();
            theme_content.push($(this).val());
        });
        /* 获取所有备注 */
        var remark = [];
        $(".remark").each(function () {
            item = {};
            item['remark'] = $(this).val();
            remark.push($(this).val());
        });
        var jsonString_theme = JSON.stringify(theme);
        var jsonString_theme_content = JSON.stringify(theme_content);
        var jsonString_remark = JSON.stringify(remark);
        csrftoken = $("[name=csrfmiddlewaretoken]").val();
        var data = {
            "target_id": active_table,
            'date': $("#date").val(),
            'time': $("#time").val(),
            'cost_time': $("#cost_time").val(),
            'place': $("#place").val(),
            "theme": jsonString_theme,
            "theme_content": jsonString_theme_content,
            "remark": jsonString_remark,
            csrfmiddlewaretoken: csrftoken,
            "btn": ""
        }
        $.post("/topic_manager/meeting_record", data, function (response, status) {
            if (status == "success") {
                window.location.reload(true);
            }
        });

    });

    /* 点击加号按钮，会自动增加 */
    $("#add_record").click(function () {
        element_ = $(".record:first").clone(true);
        $(element_).find("input").val("");
        $(element_).find("textarea").val("");
        $(element_).find(".input").removeClass("is-valid");
        element_.appendTo(".all_record");
        $("#submitForm").attr("disabled", true);
    });

    /* 表单验证 */
    $(document).on('change', '.input', function () {
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
        $(".input").each(function () {

            if (($(this).val() == "")) {
                if ($(this).attr("id") != "target_id" && $(this).attr("class").split(" ")[0] != "remark") {
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