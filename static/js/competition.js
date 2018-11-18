$(document).ready(function () {
    /* 禁用修改和删除按钮 */
    $("#deleteForm").attr("disabled", true);
    $("#modifyForm").attr("disabled", true);
    $("#submitForm").attr("disabled", true);
    /* 删除按钮相关功能实现 */
    $("#deleteForm").click(function () {
        var button_action = $("<input type='text' name='btn' value='delete' hidden>")
        $("#target_form").append(button_action);
        $("#target_form").submit();
    });
    /* 点击某一行启用修改和删除按钮 */
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
        $("#semester").val($(this).children("td").eq(0).text());
        $("#date").val($(this).children("td").eq(1).text());
        $("#expected_result").val($(this).children("td").eq(2).text());
        $("#time_consumed").val($(this).children("td").eq(3).text());

        $("#content").val($(this).children("td").eq(4).text());
        $("#end_of_term_summary").val($(this).children("td").eq(5).text());

        $("#target_id").val(this.title);
    });

    /* 点击添加按钮 */
    $("#addForm").click(function () {
        $("#submitForm").attr("disabled", true);
        $("#competition_form").replaceWith("                        <div id=\"competition_form\">\n" +
            "                            <div class=\"row\">\n" +
            "                                <div class=\"form-group col-12\">\n" +
            "                                    <label for=\"expected_result\">赛事名称</label>\n" +
            "                                    <input type=\"text\" class=\"name input form-control\" id=\"name\" required>\n" +
            "                                </div>\n" +
            "                            </div>\n" +
            "                            <div class=\"row\">\n" +
            "                                <div class=\"form-group col-3\">\n" +
            "                                    <label for=\"content\">报名开始时间</label>\n" +
            "                                    <input type=\"text\" class=\"registration_start_time input form-control\" id=\"registration_start_time\" required>\n" +
            "                                </div>\n" +
            "                                <div class=\"form-group col-3\">\n" +
            "                                    <label for=\"content\">报名开始时间</label>\n" +
            "                                    <input type=\"text\" class=\"registration_end_time input form-control\" id=\"registration_end_time\" required>\n" +
            "                                </div>\n" +
            "                                <div class=\"form-group col-3\">\n" +
            "                                    <label for=\"content\">比赛开始时间</label>\n" +
            "                                    <input type=\"text\" class=\"start_time input form-control\" id=\"start_time\" required>\n" +
            "                                </div>\n" +
            "                                <div class=\"form-group col-3\">\n" +
            "                                    <label for=\"content\">比赛结束时间</label>\n" +
            "                                    <input type=\"text\" class=\"end_time input form-control\" id=\"end_time\" required>\n" +
            "                                </div>\n" +
            "                            </div>\n" +
            "                            <div class=\"row\">\n" +
            "                                <div class=\"form-group col-12\">\n" +
            "                                    <label for=\"content\">比赛地址</label>\n" +
            "                                    <input type=\"text\" class=\"address input form-control\" id=\"address\" required>\n" +
            "                                </div>\n" +
            "                            </div>\n" +
            "                            <div class=\"row\">\n" +
            "                                <div class=\"form-group col-6\">\n" +
            "                                    <label for=\"content\">参与人员</label>\n" +
            "                                    <textarea type=\"text\" class=\"participant input form-control\" id=\"participant\" rows=\"3\" required></textarea>\n" +
            "                                </div>\n" +
            "                                <div class=\"form-group col-6\">\n" +
            "                                    <label for=\"content\">注意事项</label>\n" +
            "                                    <textarea type=\"text\" class=\"attention input form-control\" id=\"attentation\" rows=\"3\" required></textarea>\n" +
            "                                </div>\n" +
            "                            </div>\n" +
            "                            <div class=\"row\">\n" +
            "                                <div class=\"form-group col-12\">\n" +
            "                                    <label for=\"content\">比赛情况</label>\n" +
            "                                    <textarea type=\"text\" class=\"condition input form-control\" id=\"condition\" rows=\"3\" required></textarea>\n" +
            "                                </div>\n" +
            "                            </div>\n" +
            "                        </div>");
        if ($("tr").hasClass("table-active")) {
            $("tr").removeClass("table-active");
            $("#target_id").val();
        }
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
        $.post('/valid', data, function (result) {
            if (result == "OK") {
                parent.removeClass("is-invalid");
                parent.addClass("is-valid");
            }
            else {
                $("#" + class_name + "-invalid").text(result);
                parent.removeClass("is-valid");
                parent.addClass("is-invalid");
            }
        });

        /* 客户端验证是否有缺失内容 */
        var form_complete = 1;
        $(".input").each(function () {

            if (($(this).val() == "")) {
                if ($(this).attr("id") != "target_id" && $(this).attr("class").split(" ")[0] != "attention" && $(this).attr("class").split(" ")[0] != "condition") {
                    form_complete = 0;
                }
            }
            if ($(this).hasClass("is-invalid")) {
                form_complete = 0;
            }
        });
        if (form_complete) {
            $("#submitForm").attr("disabled", false);
        }
        else {
            $("#submitForm").attr("disabled", true);
        }
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