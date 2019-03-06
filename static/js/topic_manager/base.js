/*
右键菜单的相关实现
对json进行处理
初始时保存一份空白的表
初始时禁用提交按钮
添加按钮
加号按钮
表单验证
表格项目被右击后，记录被右击的表格id
*/

$(document).ready(function () {
    /* 对json进行处理 */
    $(".table_content").each(function () {
        for (i = 0; i <= $(this).find("td").length; i++) {
            if ($(this).find("td").eq(i).hasClass("json")) {
                var array_ = JSON.parse($(this).find("td").eq(i).text());
                new_text = "";
                for (j = 0; j < array_.length - 1; j++) {
                    new_text = new_text + array_[j] + "\n";
                }
                new_text = new_text + array_[array_.length - 1];
                $(this).find("td").eq(i).text(new_text);
            }
        }
    });
    /* 对json进行处理结束 */



    /* 初始时保存一份空白的表 */
    empty_form = $("#form").html();
    /* 初始时禁用提交按钮 */
    $("#submit_form").attr("disabled", true);

    /* 点击主界面左下角添加按钮 */
    $("#add").click(function () {
        active_table = "";
        $('#form').html(empty_form);
        /* 设置日期时间 */
        var date = new Date();
        var year = date.getFullYear();
        var month = date.getMonth() + 1;
        var day = date.getDate();
        $("#date").val(year + "-" + month + "-" + day);
        $("#date").addClass("is-valid");
        $("#modal").modal('show');
    });

    /* 点击加号按钮，会自动增加并恢复表单的初始状态 */
    $(document).on('click', '#add_target', function () {
        element_ = $(".target:first").clone(true);
        $(element_).find("input").val("");
        $(element_).find("input").removeClass("is-valid");
        $(element_).find("input").removeClass("is-invalid");
        element_.appendTo(".all_record");
        $("#submit_form").attr("disabled", true);
    });

    /* 表格项目被右击后，记录被右击的表格id */
    $('tr').mousedown(function (event) {
        if (event.which == 3) {
            active_table = this.title;
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
                $("#submit_form").attr("disabled", true);
            }
        });

        /* 客户端验证是否有缺失内容 */
        var form_complete = 1;
        $("input").each(function () {

            if (($(this).val() == "")) {
                if ($(this).attr("class").split(" ")[0] != "end_of_term_summary" && $(this).attr("id") != "target_id") {
                    form_complete = 0;
                }
            }
        });
        if (form_complete) {
            $("#submit_form").attr("disabled", false);
        } else {
            $("#submit_form").attr("disabled", true);
        }
    });
    /* 表单验证结束 */
});