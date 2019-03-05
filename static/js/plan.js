/*
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

    /* 禁用修改和删除按钮 */
    $("#deleteForm").attr("disabled", true);
    $("#modify").attr("disabled", true);
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
    /* 点击某一行自动填充表单，与数据库结构有关，不可直接复制 */
    $("tr").click(function () {
        $("#plan_name").val($(this).children("td").eq(1).text());
        $("#plan_result").val($(this).children("td").eq(2).text());
        $("#type").val($(this).children("td").eq(0).text());
        if ($(this).children("td").eq(3).text() == "是") {
            $("#is_reviewed").val(1).change();
        }
        else {
            $("#is_reviewed").val(0).change();
        }
        $("#head_person").val($(this).children("td").eq(4).text());
        $("#affiliated_person").val($(this).children("td").eq(5).text());
        $("#planed_time").val($(this).children("td").eq(6).text());
        $("#planed_start_time").val($(this).children("td").eq(7).text());
        $("#planed_end_time").val($(this).children("td").eq(8).text());
        $("#actual_time").val($(this).children("td").eq(9).text());
        $("#actual_start_time").val($(this).children("td").eq(10).text());
        $("#actual_end_time").val($(this).children("td").eq(11).text());
        $("#advanced_postponed_time").val($(this).children("td").eq(12).text());
        $("#remark").val($(this).children("td").eq(13).text());
        $("#target_id").val(this.title);
    });

    $("#planed_start_time").change(function () {
        text = $("#planed_start_time").val();
        csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        $.post('/topic_manager/valid', {
            planed_start_time: text,
            csrfmiddlewaretoken: csrftoken
        }, function (result) {
            if (result == "OK") {
                $("#planed_start_time").removeClass("is-invalid");
                $("#planed_start_time").addClass("is-valid");
                if (!$("input").hasClass("is-invalid")) {
                    $("submitForm").attr("disabled", false);
                }
            }
            else {
                $("#planed_start_time-invalid").text(result);
                $("#planed_start_time").removeClass("is-valid");
                $("#planed_start_time").addClass("is-invalid");
                $("submitForm").attr("disabled", true);
            }
        });
    });

    $("#planed_end_time").change(function () {
        text = $("#planed_end_time").val();
        csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        $.post('/topic_manager/valid', {
            planed_end_time: text,
            csrfmiddlewaretoken: csrftoken
        }, function (result) {
            if (result == "OK") {
                $("#planed_end_time").removeClass("is-invalid");
                $("#planed_end_time").addClass("is-valid");
                if (!$("input").hasClass("is-invalid")) {
                    $("submitForm").attr("disabled", false);
                }
            }
            else {
                $("#planed_end_time-invalid").text(result);
                $("#planed_end_time").removeClass("is-valid");
                $("#planed_end_time").addClass("is-invalid");
                $("submitForm").attr("disabled", true);
            }
        });
    });
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
});