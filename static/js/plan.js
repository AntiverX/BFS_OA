/*
初始时保存一份空白的表
点击主界面左下角添加按钮
表格项目被右击后，记录被右击的表格id
右键菜单的相关实现
对json进行处理
删除按钮实现
修改按钮实现
添加按钮实现
提交按钮实现
点击某一行实现选中效果,并启用删除和修改按钮
点击加号增加表单
表单验证（服务端验证和本地验证）
*/

$(document).ready(function () {
    /* 初始时保存一份空白的表 */
    empty_form = $(".all_record").clone(true);

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
                    $("#modify").click();
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
                    $.post("/topic_manager/plan", data, function (response, status) {
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

    /* 初始时禁用提交按钮 */
    $("#submitForm").attr("disabled", true);

    /* 删除按钮相关功能实现 */
    $("#deleteForm").click(function () {
        var button_action = $("<input type='text' name='btn' value='delete' hidden>")
        $("#planForm").append(button_action);
        $("#planForm").submit();
    });
    /* 点击某一行启用修改和删除按钮并增加选中效果 */
    $("tbody tr").click(function () {
        $("#target_id").val(this.title);
        $("#deleteForm").attr("disabled", false);
        $("#modify").attr("disabled", false);
        if ($("tr").hasClass("table-active")) {
            $("tr").removeClass("table-active");
        }
        $(this).addClass("table-active");
    });

    /* 修改按钮相关实现 */
    $("#modify").click(function () {

        /* 清空表格已有内容 */
        $("#planForm").find(".form-control").val("").addClass("is-valid");
        $("#planForm").find(".is_reviewed").val("").addClass("is-valid");

        /* 获得要修改的条目的各列值 */
        var target_id = active_table;
        var plan_name = $("tr[title=" + target_id + "]").find("td").eq(0).text();
        var plan_result = $("tr[title=" + target_id + "]").find("td").eq(1).text();
        var type = $("tr[title=" + target_id + "]").find("td").eq(2).text();
        var is_reviewed = $("tr[title=" + target_id + "]").find("td").eq(3).text();
        var head_person = $("tr[title=" + target_id + "]").find("td").eq(4).text();
        var affiliated_person = $("tr[title=" + target_id + "]").find("td").eq(5).text();
        var planed_time = $("tr[title=" + target_id + "]").find("td").eq(6).text();
        var planed_start_time = $("tr[title=" + target_id + "]").find("td").eq(7).text();
        var planed_end_time = $("tr[title=" + target_id + "]").find("td").eq(8).text();
        var actual_time = $("tr[title=" + target_id + "]").find("td").eq(9).text();
        var actual_start_time = $("tr[title=" + target_id + "]").find("td").eq(10).text();
        var actual_end_time = $("tr[title=" + target_id + "]").find("td").eq(11).text();
        var advanced_postponed_time = $("tr[title=" + target_id + "]").find("td").eq(12).text();
        var remark = $("tr[title=" + target_id + "]").find("td").eq(13).text();

        /* 赋值 */
        $("#target_id").val(target_id);
        $("#plan_name").val(plan_name);
        $("#plan_result").val(plan_result);
        $("#type").val(type);
        $("#is_reviewed").val(is_reviewed == "是" ? 1 : 0);
        $("#head_person").val(head_person);
        $("#affiliated_person").val(affiliated_person);
        $("#planed_time").val(planed_time);
        $("#planed_start_time").val(planed_start_time);
        $("#planed_end_time").val(planed_end_time);
        $("#actual_time").val(actual_time);
        $("#actual_start_time").val(actual_start_time);
        $("#actual_end_time").val(actual_end_time);
        $("#advanced_postponed_time").val(advanced_postponed_time);
        $("#remark").val(remark);

    });
    /* 修改按钮相关实现结束 */

    /* 点击空白处失去选中，并清空id记录 */
    $(document).on("click", function (e) {
        if (e.target.tagName != "TH" && e.target.tagName !== "TD") {
            $("#target_id").val();
            $("#deleteForm").attr("disabled", true);
            $("#modifyForm").attr("disabled", true);
            if ($("tr").hasClass("table-active")) {
                $("tr").removeClass("table-active");
            }
        }
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
                if ($(this).attr("class").split(" ")[0] != "end_of_term_summary" && $(this).attr("id") != "target_id") {
                    console.log($(this).attr("class"));
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
    /* 表单验证结束 */

});