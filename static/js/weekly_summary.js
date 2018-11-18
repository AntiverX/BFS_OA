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
    /* 删除按钮相关功能实现 */
    $("#deleteForm").click(function () {
        csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        data = {
            "target_id": $("#target_id").val(),
            "btn": "delete",
            "average_work_hour": "",
            "absent_hour": "",
            "this_week_task": "",
            "next_week_task": "",
            "week": "",
            csrfmiddlewaretoken: csrftoken
        }
        $.post("/topic_manager/weekly_summary", data, function (response, status) {
            if (status == "success") {
                window.location.reload(true);
            }
        });
    });
    /* 修改按钮相关实现 */
    $("#modifyForm").click(function () {
        $(".all_this_week_work").replaceWith("                            <div id=\"form\">\n" +
            "                                <div class=\"row\" id=\"replace_form\">\n" +
            "                                    <div class=\"col-6\">\n" +
            "                                        <div class=\"all_this_week_work\">\n" +
            "                                            <div class=\"this_week_work\">\n" +
            "                                                <div class=\"form-group\">\n" +
            "                                                    <label for=\"this_week_task\">本周工作</label>\n" +
            "                                                    <input class=\"this_week_task form-control\" required></input>\n" +
            "                                                </div>\n" +
            "                                            </div>\n" +
            "                                        </div>\n" +
            "                                    </div>\n" +
            "                                    <div class=\"col-6\">\n" +
            "                                        <div class=\"all_next_week_work\">\n" +
            "                                            <div class=\"next_week_work\">\n" +
            "                                                <div class=\"form-group\">\n" +
            "                                                    <label for=\"this_week_task\">下周工作</label>\n" +
            "                                                    <input class=\"next_week_task form-control\" required></input>\n" +
            "                                                </div>\n" +
            "                                            </div>\n" +
            "                                        </div>\n" +
            "                                    </div>\n" +
            "                                </div>\n" +
            "                            </div>");
        var target_id = $("#target_id").val();
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
    });

    /* 点击添加按钮 */
    $("#addForm").click(function () {
        $("#week").addClass("is-valid");
        $("#absent_hour").addClass("is-valid");
        $(".form").replaceWith("                            <div id=\"form\">\n" +
            "                                <div class=\"row\" id=\"replace_form\">\n" +
            "                                    <div class=\"col-6\">\n" +
            "                                        <div class=\"all_this_week_work\">\n" +
            "                                            <div class=\"this_week_work\">\n" +
            "                                                <div class=\"form-group\">\n" +
            "                                                    <label for=\"this_week_task\">本周工作</label>\n" +
            "                                                    <input class=\"this_week_task form-control\" required></input>\n" +
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
            "                                    <div class=\"col-6\">\n" +
            "                                        <div class=\"all_next_week_work\">\n" +
            "                                            <div class=\"next_week_work\">\n" +
            "                                                <div class=\"form-group\">\n" +
            "                                                    <label for=\"this_week_task\">下周工作</label>\n" +
            "                                                    <input class=\"next_week_task form-control\" required></input>\n" +
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
            "                                </div>\n" +
            "                            </div>");
        if ($("tr").hasClass("table-active")) {
            $("tr").removeClass("table-active");
        }
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
            "target_id": $("#target_id").val(),
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
        $("input").each(function () {

            if (($(this).val() == "")) {
                if ($(this).attr("id") != "target_id") {
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