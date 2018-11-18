$(document).ready(function () {

    /* 禁用所有按钮 */
    $("#deleteForm").attr("disabled", true);
    $("#modifyForm").attr("disabled", true);
    // $("#submitForm").attr("disabled", true);


    $("#modifyForm").click(function () {
        $("#UserForm").replaceWith("                  <div id=\"UserForm\">\n" +
            "                            <div class=\"row\">\n" +
            "                                <div class=\"form-group col-3\">\n" +
            "                                    <label for=\"plan_name\">账户名</label>\n" +
            "                                    <input type=\"text\" class=\"form-control\" id=\"username\" required>\n" +
            "                                </div>\n" +
            "                                <div class=\"form-group col-3\">\n" +
            "                                    <label for=\"plan_name\">姓名</label>\n" +
            "                                    <input type=\"text\" class=\"form-control\" id=\"real_name\" required>\n" +
            "                                </div>\n" +
            "                            </div>\n" +
            "                            <div class=\"row\">\n" +
            "                                <div class=\"form-group col-2\">\n" +
            "                                    <label for=\"plan_name\">管理员</label>\n" +
            "                                    <select type=\"text\" class=\"form-control\" id=\"is_admin\" required>\n" +
            "                                        <option value=\"1\">是</option>\n" +
            "                                        <option value=\"0\">否</option>\n" +
            "                                    </select>\n" +
            "                                </div>\n" +
            "                                <div class=\"form-group col-2\">\n" +
            "                                    <label for=\"plan_name\">学生</label>\n" +
            "                                    <select type=\"text\" class=\"form-control\" id=\"is_student\" required>\n" +
            "                                        <option value=\"1\">是</option>\n" +
            "                                        <option value=\"0\">否</option>\n" +
            "                                    </select>\n" +
            "                                </div>\n" +
            "                                <div class=\"form-group col-2\">\n" +
            "                                    <label for=\"plan_name\">教师</label>\n" +
            "                                    <select type=\"text\" class=\"form-control\" id=\"is_teacher\" required>\n" +
            "                                        <option value=\"1\">是</option>\n" +
            "                                        <option value=\"0\">否</option>\n" +
            "                                    </select>\n" +
            "                                </div>\n" +
            "                            </div>\n" +
            "                        </div>");
        var target_id = $("#target_id").val();
        var username = $("tr[title=" + target_id + "]").find("td").eq(0).text();
        var real_name = $("tr[title=" + target_id + "]").find("td").eq(1).text();
        var is_admin = $("tr[title=" + target_id + "]").find("td").eq(2).text();
        var is_student = $("tr[title=" + target_id + "]").find("td").eq(3).text();
        var is_teacher = $("tr[title=" + target_id + "]").find("td").eq(4).text();
        $("#username").val(username);
        $("#real_name").val(real_name);
        $("#is_admin").val(is_admin == "是" ? 1 : 0);
        $("#is_student").val(is_student == "是" ? 1 : 0);
        $("#is_teacher").val(is_teacher == "是" ? 1 : 0);
    });

    /* 删除按钮 */
    $("#deleteForm").click(function () {
        csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        var data = {
            "target_id": $("#target_id").val(),
            csrfmiddlewaretoken: csrftoken,
            "btn": "delete"
        }
        $.post("/system/users_management", data, function (response, status) {
            if (status == "success") {
                window.location.reload(true);
            }
        });
    });

    /*  提交按钮 */
    $("#submitForm").click(function () {
        csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        var data = {
            "target_id": $("#target_id").val(),
            'username': $("#username").val(),
            'real_name': $("#real_name").val(),
            "is_admin": $("#is_admin").val(),
            "is_student": $("#is_student").val(),
            "is_teacher": $("#is_teacher").val(),
            csrfmiddlewaretoken: csrftoken,
            "btn": ""
        }
        $.post("/system/users_management", data, function (response, status) {
            if (status == "success") {
                window.location.reload(true);
            }
        });
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