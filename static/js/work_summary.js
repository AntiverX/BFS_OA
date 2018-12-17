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

    /* 禁用修改和删除按钮 */
    $("#deleteForm").attr("disabled", true);
    $("#modifyForm").attr("disabled", true);
    $("#submitForm").attr("disabled", true);
    /* 保存一份未经修改过的表单 */
    var originalForm = $("form").clone(true);

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

            var array_ = JSON.parse($(this).find("td").eq(-2).text());
            new_text = "";
            for (var i = 0; i < array_.length - 1; i++) {
                new_text = new_text + array_[i] + "\n";
            }
            new_text = new_text + array_[array_.length - 1];
            $(this).find("td").eq(-2).text(new_text);

            var array_ = JSON.parse($(this).find("td").eq(-3).text());
            new_text = "";
            for (var i = 0; i < array_.length - 1; i++) {
                new_text = new_text + array_[i] + "\n";
            }
            new_text = new_text + array_[array_.length - 1];
            $(this).find("td").eq(-3).text(new_text);

            var array_ = JSON.parse($(this).find("td").eq(-4).text());
            new_text = "";
            for (var i = 0; i < array_.length - 1; i++) {
                new_text = new_text + array_[i] + "\n";
            }
            new_text = new_text + array_[array_.length - 1];
            $(this).find("td").eq(-4).text(new_text);
        }
    });

    /* 修改按钮相关实现 */
    $("#modifyForm").click(function () {
        $(".all_plan").replaceWith("                                <div class=\"all_plan\">\n" +
            "                                    <div class=\"plan\">\n" +
            "                                        <hr>\n" +
            "                                        <div class=\"form-group\">\n" +
            "                                            <label for=\"summary\">工作总结</label>\n" +
            "                                            <input type=\"text\" class=\"summary form-control\" id=\"summary\" name=\"summary\" required>\n" +
            "                                            <div id=\"summary-valid\" class=\"valid-feedback\">\n" +
            "                                                OK\n" +
            "                                            </div>\n" +
            "                                            <div id=\"summary-invalid\" class=\"invalid-feedback\">\n" +
            "                                                ERROR\n" +
            "                                            </div>\n" +
            "                                        </div>\n" +
            "                                        <div class=\"row\">\n" +
            "                                            <div class=\"form-group col-2\">\n" +
            "                                                <label for=\"man_day\">人日数（天）</label>\n" +
            "                                                <input type=\"text\" class=\"man_day form-control\" id=\"\" required>\n" +
            "                                                <div id=\"man_day-valid\" class=\"valid-feedback\">\n" +
            "                                                    OK\n" +
            "                                                </div>\n" +
            "                                                <div id=\"man_day-invalid\" class=\"invalid-feedback\">\n" +
            "                                                    ERROR\n" +
            "                                                </div>\n" +
            "                                            </div>\n" +
            "                                            <div class=\"form-group col-2\">\n" +
            "                                                <label for=\"natural_day\">自然日（天）</label>\n" +
            "                                                <input type=\"text\" class=\"natural_day form-control\" id=\"natural_day\" name=\"natural_day\" required>\n" +
            "                                                <div id=\"natural_day-valid\" class=\"valid-feedback\">\n" +
            "                                                    OK\n" +
            "                                                </div>\n" +
            "                                                <div id=\"natural_day-invalid\" class=\"invalid-feedback\">\n" +
            "                                                    ERROR\n" +
            "                                                </div>\n" +
            "                                            </div>\n" +
            "                                            <div class=\"form-group col-8\">\n" +
            "                                                <label for=\"remark\">计划执行情况和工作效果说明</label>\n" +
            "                                                <input type=\"text\" class=\"remark form-control\" id=\"remark\" name=\"remark\">\n" +
            "                                                <div id=\"remark-valid\" class=\"valid-feedback\">\n" +
            "                                                    OK\n" +
            "                                                </div>\n" +
            "                                                <div id=\"remark-invalid\" class=\"invalid-feedback\">\n" +
            "                                                    ERROR\n" +
            "                                                </div>\n" +
            "                                            </div>\n" +
            "                                        </div>\n" +
            "                                    </div>\n" +
            "                                </div>");
        var target_id = $("#target_id").val();
        var type = $("tr[title=" + target_id + "]").find("td").eq(0).text();
        var date = $("tr[title=" + target_id + "]").find("td").eq(1).text();
        var average_time = $("tr[title=" + target_id + "]").find("td").eq(2).text();
        var all_days = $("tr[title=" + target_id + "]").find("td").eq(3).text();
        var summary = $("tr[title=" + target_id + "]").find("td").eq(4).text();
        var man_day = $("tr[title=" + target_id + "]").find("td").eq(5).text();
        var natural_day = $("tr[title=" + target_id + "]").find("td").eq(6).text();
        var remark = $("tr[title=" + target_id + "]").find("td").eq(7).text();
        var summary_split = summary.split("\n");
        var man_day_split = man_day.split("\n");
        var natural_day_split = natural_day.split("\n");
        var remark_split = remark.split("\n");
        console.log(summary_split.length);
        for (var i = 0; i < summary_split.length - 1; i++) {
            element_ = $(".plan:first").clone(true);
            $(element_).find("input").val("");
            element_.appendTo(".all_plan");
        }
        /* 赋值 */
        $("#type").val(type);
        $("#date").val(date);
        $("#average_time").val(average_time);
        $("#all_days").val(all_days);
        for (var i = 0; i < summary_split.length; i++) {
            $(".summary").eq(i).val(summary_split[i]);
            $(".man_day").eq(i).val(man_day_split[i]);
            $(".natural_day").eq(i).val(natural_day_split[i]);
            $(".remark").eq(i).val(remark_split[i]);
        }
    });

    /* 删除按钮相关功能实现 */
    $("#deleteForm").click(function () {
        csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        data = {
            "target_id": $("#target_id").val(),
            'type': "",
            'date': "",
            'average_time': "",
            'all_days': "",
            "summary": "",
            "man_day": "",
            "natural_day": "",
            "remark": "",
            csrfmiddlewaretoken: csrftoken,
            "btn": "delete"
        }
        $.post("/topic_manager/work_summary", data, function (response, status) {
            if (status == "success") {
                window.location.reload(true);
            }
        });
    });

    /* 提交按钮相关功能实现 */
    $("#submitForm").click(function () {
        /* 获取所有工作总结 */
        var summary = [];
        $(".summary").each(function () {
            item = {};
            item['summary'] = $(this).val();
            summary.push($(this).val());
        });
        /* 获取所有人日数 */
        var man_day = [];
        $(".man_day").each(function () {
            item = {};
            item['man_day'] = $(this).val();
            man_day.push($(this).val());
        });
        /* 获取所有自然日日数 */
        var natural_day = [];
        $(".natural_day").each(function () {
            item = {};
            item['natural_day'] = $(this).val();
            natural_day.push($(this).val());
        });
        /* 获取所有计划执行情况和工作效果说明 */
        var remark = [];
        $(".remark").each(function () {
            item = {};
            item['remark'] = $(this).val();
            remark.push($(this).val());
        });
        var jsonString_summary = JSON.stringify(summary);
        var jsonString_man_day = JSON.stringify(man_day);
        var jsonString_natural_day = JSON.stringify(natural_day);
        var jsonString_remark = JSON.stringify(remark);
        csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        var data = {
            "target_id": $("#target_id").val(),
            'type': $("#type").val(),
            'date': $("#date").val(),
            'average_time': $("#average_time").val(),
            'all_days': $("#all_days").val(),
            "summary": jsonString_summary,
            "man_day": jsonString_man_day,
            "natural_day": jsonString_natural_day,
            "remark": jsonString_remark,
            csrfmiddlewaretoken: csrftoken,
            "btn": ""
        }
        $.post("/topic_manager/work_summary", data, function (response, status) {
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
    $("#add_plan").click(function () {
        element_ = $(".plan:first").clone(true);
        $(element_).find("input").val("");
        $(element_).find("input").removeClass("is-valid");
        $(element_).find("input").removeClass("is-invalid");
        element_.appendTo(".all_plan");
        $("#submitForm").attr("disabled", true);
    });

    $(document).on('change', ".man_day", function () {
        var all_days = Number(0);
        $(".man_day").each(function () {
            all_days = Number(all_days) + Number($(this).val());
        });
        $("#all_days").val(all_days);
    });

    /* 点击添加按钮 */
    $("#addForm").click(function () {
        $("#form").find("input").val("");
        $("#average_time").val("8.0/7.0");
        $("#average_time").addClass("is-valid");
        /* 设置日期时间 */
        var date = new Date();
        var year = date.getFullYear();
        var month = date.getMonth() + 1;
        var day = date.getDate();
        $("#date").val(year + "-" + month + "-" + day);
        $("#date").addClass("is-valid");
        $("#type").addClass("is-valid");
        $(".all_plan").replaceWith("                                <div class=\"all_plan\">\n" +
            "                                    <div class=\"plan\">\n" +
            "                                        <hr>\n" +
            "                                        <div class=\"form-group\">\n" +
            "                                            <label for=\"summary\">工作总结</label>\n" +
            "                                            <input type=\"text\" class=\"summary form-control\" id=\"summary\" name=\"summary\" required>\n" +
            "                                            <div id=\"summary-valid\" class=\"valid-feedback\">\n" +
            "                                                OK\n" +
            "                                            </div>\n" +
            "                                            <div id=\"summary-invalid\" class=\"invalid-feedback\">\n" +
            "                                                ERROR\n" +
            "                                            </div>\n" +
            "                                        </div>\n" +
            "                                        <div class=\"row\">\n" +
            "                                            <div class=\"form-group col-2\">\n" +
            "                                                <label for=\"man_day\">人日数（天）</label>\n" +
            "                                                <input type=\"text\" class=\"man_day form-control\" id=\"\" required>\n" +
            "                                                <div id=\"man_day-valid\" class=\"valid-feedback\">\n" +
            "                                                    OK\n" +
            "                                                </div>\n" +
            "                                                <div id=\"man_day-invalid\" class=\"invalid-feedback\">\n" +
            "                                                    ERROR\n" +
            "                                                </div>\n" +
            "                                            </div>\n" +
            "                                            <div class=\"form-group col-2\">\n" +
            "                                                <label for=\"natural_day\">自然日（天）</label>\n" +
            "                                                <input type=\"text\" class=\"natural_day form-control\" id=\"natural_day\" name=\"natural_day\" required>\n" +
            "                                                <div id=\"natural_day-valid\" class=\"valid-feedback\">\n" +
            "                                                    OK\n" +
            "                                                </div>\n" +
            "                                                <div id=\"natural_day-invalid\" class=\"invalid-feedback\">\n" +
            "                                                    ERROR\n" +
            "                                                </div>\n" +
            "                                            </div>\n" +
            "                                            <div class=\"form-group col-8\">\n" +
            "                                                <label for=\"remark\">计划执行情况和工作效果说明</label>\n" +
            "                                                <input type=\"text\" class=\"remark form-control\" id=\"remark\" name=\"remark\">\n" +
            "                                                <div id=\"remark-valid\" class=\"valid-feedback\">\n" +
            "                                                    OK\n" +
            "                                                </div>\n" +
            "                                                <div id=\"remark-invalid\" class=\"invalid-feedback\">\n" +
            "                                                    ERROR\n" +
            "                                                </div>\n" +
            "                                            </div>\n" +
            "                                        </div>\n" +
            "                                    </div>\n" +
            "                                </div>");
        if ($("tr").hasClass("table-active")) {
            $("tr").removeClass("table-active");
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