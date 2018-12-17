$(document).ready(function () {
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

    /* 对json进行处理，分行显示本周和下周工作 */
    $("tr").each(function () {
        if ($(this).find("td").length != 0) {
            var array_ = JSON.parse($(this).find("td").eq(-1).text());
            new_text = "";
            for (var i = 0; i < array_.length - 1; i++) {
                new_text = new_text + array_[i] + "\n\n";
            }
            new_text = new_text + array_[array_.length - 1];
            $(this).find("td").eq(-1).text(new_text);
        }

        if ($(this).find("td").length != 0) {
            var array_ = JSON.parse($(this).find("td").eq(-2).text());
            new_text = "";
            for (var i = 0; i < array_.length - 1; i++) {
                new_text = new_text + array_[i] + "\n\n";
            }
            new_text = new_text + array_[array_.length - 1];
            $(this).find("td").eq(-2).text(new_text);
        }

        if ($(this).find("td").length != 0) {
            var array_ = JSON.parse($(this).find("td").eq(-3).text());
            new_text = "";
            for (var i = 0; i < array_.length - 1; i++) {
                new_text = new_text + array_[i] + "\n\n";
            }
            new_text = new_text + array_[array_.length - 1];
            $(this).find("td").eq(-3).text(new_text);
        }
    });

    /* 禁用修改和删除按钮 */
    $("#deleteForm").attr("disabled", true);
    $("#modifyForm").attr("disabled", true);
    $("#submitForm").attr("disabled", true);

    /* 删除按钮相关功能实现 */
    $("#deleteForm").click(function () {
        csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        data = {
            "target_id": $("#target_id").val(),
            'date': "",
            'time': "",
            'cost_time': "",
            'place': "",
            "theme": "",
            "theme_content": "",
            "remark": "",
            csrfmiddlewaretoken: csrftoken,
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
        $(".all_record").replaceWith("                                <div class=\"all_record\">\n" +
            "                                    <div class=\"record\">\n" +
            "                                        <hr>\n" +
            "                                        <div class=\"row\">\n" +
            "                                            <div class=\"col-6\">\n" +
            "                                                <div class=\"form-group\">\n" +
            "                                                    <label for=\"theme\">主题</label>\n" +
            "                                                    <input class=\"theme input form-control\" required>\n" +
            "                                                    <div id=\"content-valid\" class=\"valid-feedback\">\n" +
            "                                                        OK\n" +
            "                                                    </div>\n" +
            "                                                    <div id=\"content-invalid\" class=\"invalid-feedback\">\n" +
            "                                                        ERROR\n" +
            "                                                    </div>\n" +
            "                                                </div>\n" +
            "                                                <div class=\"form-group\">\n" +
            "                                                    <label for=\"remark\">备注</label>\n" +
            "                                                    <input class=\"remark input form-control\" rows=\"1\"></input>\n" +
            "                                                    <div id=\"content-valid\" class=\"valid-feedback\">\n" +
            "                                                        OK\n" +
            "                                                    </div>\n" +
            "                                                    <div id=\"content-invalid\" class=\"invalid-feedback\">\n" +
            "                                                        ERROR\n" +
            "                                                    </div>\n" +
            "                                                </div>\n" +
            "                                            </div>\n" +
            "                                            <div class=\" col-6\">\n" +
            "                                                <div class=\"form-group\">\n" +
            "                                                    <label for=\"theme_content\">主题内容说明</label>\n" +
            "                                                    <textarea class=\"theme_content input form-control\" rows=\"5\" required></textarea>\n" +
            "                                                    <div id=\"content-valid\" class=\"valid-feedback\">\n" +
            "                                                        OK\n" +
            "                                                    </div>\n" +
            "                                                    <div id=\"content-invalid\" class=\"invalid-feedback\">\n" +
            "                                                        ERROR\n" +
            "                                                    </div>\n" +
            "                                                </div>\n" +
            "                                            </div>\n" +
            "                                        </div>\n" +
            "                                    </div>\n" +
            "                                </div>");
        var target_id = $("#target_id").val();
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
    });

    /* 点击添加按钮 */
    $("#addForm").click(function () {
        $("#target_id").val("");
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
        $(".all_record").replaceWith("                                <div class=\"all_record\">\n" +
            "                                    <div class=\"record\">\n" +
            "                                        <hr>\n" +
            "                                        <div class=\"row\">\n" +
            "                                            <div class=\"col-6\">\n" +
            "                                                <div class=\"form-group\">\n" +
            "                                                    <label for=\"theme\">主题</label>\n" +
            "                                                    <input class=\"theme input form-control\" required>\n" +
            "                                                    <div id=\"content-valid\" class=\"valid-feedback\">\n" +
            "                                                        OK\n" +
            "                                                    </div>\n" +
            "                                                    <div id=\"content-invalid\" class=\"invalid-feedback\">\n" +
            "                                                        ERROR\n" +
            "                                                    </div>\n" +
            "                                                </div>\n" +
            "                                                <div class=\"form-group\">\n" +
            "                                                    <label for=\"remark\">备注</label>\n" +
            "                                                    <input class=\"remark input form-control\" rows=\"1\"></input>\n" +
            "                                                    <div id=\"content-valid\" class=\"valid-feedback\">\n" +
            "                                                        OK\n" +
            "                                                    </div>\n" +
            "                                                    <div id=\"content-invalid\" class=\"invalid-feedback\">\n" +
            "                                                        ERROR\n" +
            "                                                    </div>\n" +
            "                                                </div>\n" +
            "                                            </div>\n" +
            "                                            <div class=\" col-6\">\n" +
            "                                                <div class=\"form-group\">\n" +
            "                                                    <label for=\"theme_content\">主题内容说明</label>\n" +
            "                                                    <textarea class=\"theme_content input form-control\" rows=\"5\" required></textarea>\n" +
            "                                                    <div id=\"content-valid\" class=\"valid-feedback\">\n" +
            "                                                        OK\n" +
            "                                                    </div>\n" +
            "                                                    <div id=\"content-invalid\" class=\"invalid-feedback\">\n" +
            "                                                        ERROR\n" +
            "                                                    </div>\n" +
            "                                                </div>\n" +
            "                                            </div>\n" +
            "                                        </div>\n" +
            "                                    </div>\n" +
            "                                </div>");
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
            "target_id": $("#target_id").val(),
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

    /* 点击某一行启用修改和删除按钮并增加选中效果 */
    $("tbody tr").click(function () {
        $("#target_id").val(this.title);
        $("#deleteForm").attr("disabled", false);
        $("#modifyForm").attr("disabled", false);
        if ($("tr").hasClass("table-active")) {
            $("tr").removeClass("table-active");
        }
        $(this).addClass("table-active");
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
            }
            else {
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