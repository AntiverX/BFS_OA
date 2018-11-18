/*
* 对json进行处理
* 禁用按钮
* 删除按钮实现
* 修改按钮实现
* 添加按钮实现
* 提交按钮实现
* 点击某一行实现选中效果,并启用删除和修改按钮
* 点击加号增加表单
* 表单验证（服务端验证和本地验证）
* */

$(document).ready(function () {
    /* 禁用按钮 */
    $("#deleteForm").attr("disabled", true);
    $("#modifyForm").attr("disabled", true);
    $("#submitForm").attr("disabled", true);

    /* 删除按钮相关功能实现 */
    $("#deleteForm").click(function () {
        csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        data = {
            "target_id": $("#target_id").val(),
            'class_name': "",
            'teacher_name': "",
            "week_start": "",
            "week_end": "",
            "day": "",
            "class_number": "",
            "class_location": "",
            csrfmiddlewaretoken: csrftoken,
            "btn": "delete"
        }
        $.post("/info/time_table_list", data, function (response, status) {
            if (status == "success") {
                window.location.reload(true);
            }
        });
    });

    /* 修改按钮相关实现 */
    $("#modifyForm").click(function () {
        $("#single_form").replaceWith("   <div id=\"single_form\">\n" +
            "                                <div class=\"form-group\">\n" +
            "                                    <label for=\"plan_name\">课程名称</label>\n" +
            "                                    <input type=\"text\" class=\"class_name form-control\" id=\"class_name\" name=\"class_name\" required>\n" +
            "                                    <div id=\"content-valid\" class=\"valid-feedback\">\n" +
            "                                        OK\n" +
            "                                    </div>\n" +
            "                                    <div id=\"content-invalid\" class=\"invalid-feedback\">\n" +
            "                                        ERROR\n" +
            "                                    </div>\n" +
            "                                </div>\n" +
            "                                <div class=\"row\">\n" +
            "                                    <div class=\"form-group col-2\">\n" +
            "                                        <label for=\"plan_result\">教师名称</label>\n" +
            "                                        <input type=\"text\" class=\"teacher_name form-control\" id=\"teacher_name\" name=\"teacher_name\" required>\n" +
            "                                        <div id=\"content-valid\" class=\"valid-feedback\">\n" +
            "                                            OK\n" +
            "                                        </div>\n" +
            "                                        <div id=\"content-invalid\" class=\"invalid-feedback\">\n" +
            "                                            ERROR\n" +
            "                                        </div>\n" +
            "                                    </div>\n" +
            "                                    <div class=\"form-group col-2\">\n" +
            "                                        <label for=\"plan_result\">开始周</label>\n" +
            "                                        <input type=\"text\" class=\"week_start form-control\" id=\"week_start\" name=\"week_start\" required>\n" +
            "                                        <div id=\"content-valid\" class=\"valid-feedback\">\n" +
            "                                            OK\n" +
            "                                        </div>\n" +
            "                                        <div id=\"content-invalid\" class=\"invalid-feedback\">\n" +
            "                                            ERROR\n" +
            "                                        </div>\n" +
            "                                    </div>\n" +
            "                                    <div class=\"form-group col-2\">\n" +
            "                                        <label for=\"plan_result\">结束周</label>\n" +
            "                                        <input type=\"text\" class=\"week_end form-control\" id=\"week_end\" name=\"week_end\" required>\n" +
            "                                        <div id=\"content-valid\" class=\"valid-feedback\">\n" +
            "                                            OK\n" +
            "                                        </div>\n" +
            "                                        <div id=\"content-invalid\" class=\"invalid-feedback\">\n" +
            "                                            ERROR\n" +
            "                                        </div>\n" +
            "                                    </div>\n" +
            "                                    <div class=\"form-group col-2\">\n" +
            "                                        <label for=\"plan_result\">星期</label>\n" +
            "                                        <select class=\"day form-control is-valid\" id=\"day\" name=\"day\">\n" +
            "                                            <option value=\"1\">一</option>\n" +
            "                                            <option value=\"2\">二</option>\n" +
            "                                            <option value=\"3\">三</option>\n" +
            "                                            <option value=\"4\">四</option>\n" +
            "                                            <option value=\"5\">五</option>\n" +
            "                                            <option value=\"6\">六</option>\n" +
            "                                            <option value=\"7\">日</option>\n" +
            "                                        </select>\n" +
            "                                        <div id=\"content-valid\" class=\"valid-feedback\">\n" +
            "                                            OK\n" +
            "                                        </div>\n" +
            "                                        <div id=\"content-invalid\" class=\"invalid-feedback\">\n" +
            "                                            ERROR\n" +
            "                                        </div>\n" +
            "                                    </div>\n" +
            "                                    <div class=\"form-group col-2\">\n" +
            "                                        <label for=\"plan_result\">大节</label>\n" +
            "                                        <select class=\"class_number form-control is-valid\" id=\"class_number\" name=\"class_number\">\n" +
            "                                            <option value=\"1\">1</option>\n" +
            "                                            <option value=\"2\">2</option>\n" +
            "                                            <option value=\"3\">3</option>\n" +
            "                                            <option value=\"4\">4</option>\n" +
            "                                            <option value=\"5\">5</option>\n" +
            "                                        </select>\n" +
            "                                        <div id=\"content-valid\" class=\"valid-feedback\">\n" +
            "                                            OK\n" +
            "                                        </div>\n" +
            "                                        <div id=\"content-invalid\" class=\"invalid-feedback\">\n" +
            "                                            ERROR\n" +
            "                                        </div>\n" +
            "                                    </div>\n" +
            "                                    <div class=\"form-group col-2\">\n" +
            "                                        <label for=\"plan_result\">地点</label>\n" +
            "                                        <input type=\"text\" class=\"class_location form-control\" id=\"class_location\" name=\"class_location\" required>\n" +
            "                                        <div id=\"content-valid\" class=\"valid-feedback\">\n" +
            "                                            OK\n" +
            "                                        </div>\n" +
            "                                        <div id=\"content-invalid\" class=\"invalid-feedback\">\n" +
            "                                            ERROR\n" +
            "                                        </div>\n" +
            "                                    </div>\n" +
            "                                </div>\n" +
            "                            </div>");
        var target_id = $("#target_id").val();
        $("#class_name").val($("tr[title=" + target_id + "]").find("td").eq(0).text());
        $("#teacher_name").val($("tr[title=" + target_id + "]").find("td").eq(1).text());
        $("#week_start").val($("tr[title=" + target_id + "]").find("td").eq(2).text());
        $("#week_end").val($("tr[title=" + target_id + "]").find("td").eq(3).text());
        $("#day").val($("tr[title=" + target_id + "]").find("td").eq(4).text());
        $("#class_number").val($("tr[title=" + target_id + "]").find("td").eq(5).text());
        $("#class_location").val($("tr[title=" + target_id + "]").find("td").eq(6).text());
    });
    /* 提交按钮相关功能实现 */
    $("#submitForm").click(function () {
        var class_name = $("#class_name").val();
        var teacher_name = $("#teacher_name").val();
        var week_start = $("#week_start").val();
        var week_end = $("#week_end").val();
        var day = $("#day").val();
        var class_number = $("#class_number").val();
        var class_location = $("#class_location").val();
        csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        var data = {
            "target_id": $("#target_id").val(),
            'class_name': class_name,
            'teacher_name': teacher_name,
            "week_start": week_start,
            "week_end": week_end,
            "day": day,
            "class_number": class_number,
            "class_location": class_location,
            csrfmiddlewaretoken: csrftoken,
            "btn": ""
        }
        $.post("/info/time_table_list", data, function (response, status) {
            if (status == "success") {
                window.location.reload(true);
            }
        });
    });

    /* 点击添加按钮 */
    $("#addForm").click(function () {
        $("submitForm").attr("disabled", true);
        $("#single_form").replaceWith("   <div id=\"single_form\">\n" +
            "                                <div class=\"form-group\">\n" +
            "                                    <label for=\"plan_name\">课程名称</label>\n" +
            "                                    <input type=\"text\" class=\"class_name form-control\" id=\"class_name\" name=\"class_name\" required>\n" +
            "                                    <div id=\"content-valid\" class=\"valid-feedback\">\n" +
            "                                        OK\n" +
            "                                    </div>\n" +
            "                                    <div id=\"content-invalid\" class=\"invalid-feedback\">\n" +
            "                                        ERROR\n" +
            "                                    </div>\n" +
            "                                </div>\n" +
            "                                <div class=\"row\">\n" +
            "                                    <div class=\"form-group col-2\">\n" +
            "                                        <label for=\"plan_result\">教师名称</label>\n" +
            "                                        <input type=\"text\" class=\"teacher_name form-control\" id=\"teacher_name\" name=\"teacher_name\" required>\n" +
            "                                        <div id=\"content-valid\" class=\"valid-feedback\">\n" +
            "                                            OK\n" +
            "                                        </div>\n" +
            "                                        <div id=\"content-invalid\" class=\"invalid-feedback\">\n" +
            "                                            ERROR\n" +
            "                                        </div>\n" +
            "                                    </div>\n" +
            "                                    <div class=\"form-group col-2\">\n" +
            "                                        <label for=\"plan_result\">开始周</label>\n" +
            "                                        <input type=\"text\" class=\"week_start form-control\" id=\"week_start\" name=\"week_start\" required>\n" +
            "                                        <div id=\"content-valid\" class=\"valid-feedback\">\n" +
            "                                            OK\n" +
            "                                        </div>\n" +
            "                                        <div id=\"content-invalid\" class=\"invalid-feedback\">\n" +
            "                                            ERROR\n" +
            "                                        </div>\n" +
            "                                    </div>\n" +
            "                                    <div class=\"form-group col-2\">\n" +
            "                                        <label for=\"plan_result\">结束周</label>\n" +
            "                                        <input type=\"text\" class=\"week_end form-control\" id=\"week_end\" name=\"week_end\" required>\n" +
            "                                        <div id=\"content-valid\" class=\"valid-feedback\">\n" +
            "                                            OK\n" +
            "                                        </div>\n" +
            "                                        <div id=\"content-invalid\" class=\"invalid-feedback\">\n" +
            "                                            ERROR\n" +
            "                                        </div>\n" +
            "                                    </div>\n" +
            "                                    <div class=\"form-group col-2\">\n" +
            "                                        <label for=\"plan_result\">星期</label>\n" +
            "                                        <select class=\"day form-control is-valid\" id=\"day\" name=\"day\">\n" +
            "                                            <option value=\"1\">一</option>\n" +
            "                                            <option value=\"2\">二</option>\n" +
            "                                            <option value=\"3\">三</option>\n" +
            "                                            <option value=\"4\">四</option>\n" +
            "                                            <option value=\"5\">五</option>\n" +
            "                                            <option value=\"6\">六</option>\n" +
            "                                            <option value=\"7\">日</option>\n" +
            "                                        </select>\n" +
            "                                        <div id=\"content-valid\" class=\"valid-feedback\">\n" +
            "                                            OK\n" +
            "                                        </div>\n" +
            "                                        <div id=\"content-invalid\" class=\"invalid-feedback\">\n" +
            "                                            ERROR\n" +
            "                                        </div>\n" +
            "                                    </div>\n" +
            "                                    <div class=\"form-group col-2\">\n" +
            "                                        <label for=\"plan_result\">大节</label>\n" +
            "                                        <select class=\"class_number form-control is-valid\" id=\"class_number\" name=\"class_number\">\n" +
            "                                            <option value=\"1\">1</option>\n" +
            "                                            <option value=\"2\">2</option>\n" +
            "                                            <option value=\"3\">3</option>\n" +
            "                                            <option value=\"4\">4</option>\n" +
            "                                            <option value=\"5\">5</option>\n" +
            "                                        </select>\n" +
            "                                        <div id=\"content-valid\" class=\"valid-feedback\">\n" +
            "                                            OK\n" +
            "                                        </div>\n" +
            "                                        <div id=\"content-invalid\" class=\"invalid-feedback\">\n" +
            "                                            ERROR\n" +
            "                                        </div>\n" +
            "                                    </div>\n" +
            "                                    <div class=\"form-group col-2\">\n" +
            "                                        <label for=\"plan_result\">地点</label>\n" +
            "                                        <input type=\"text\" class=\"class_location form-control\" id=\"class_location\" name=\"class_location\" required>\n" +
            "                                        <div id=\"content-valid\" class=\"valid-feedback\">\n" +
            "                                            OK\n" +
            "                                        </div>\n" +
            "                                        <div id=\"content-invalid\" class=\"invalid-feedback\">\n" +
            "                                            ERROR\n" +
            "                                        </div>\n" +
            "                                    </div>\n" +
            "                                </div>\n" +
            "                            </div>");
    });

    /* 点击某一行启用修改和删除按钮 */
    $("tbody tr").click(function () {
        $("#target_id").val(this.title);
        $("#deleteForm").attr("disabled", false);
        $("#modifyForm").attr("disabled", false);
        if ($("tr").hasClass("table-active")) {
            $("tr").removeClass("table-active");
        }
        $(this).addClass("table-active");
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
        $.post('/info/valid', data, function (result) {

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
        $("input").each(function () {

            if (($(this).val() == "")) {
                if ($(this).attr("id") != "target_id") {
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