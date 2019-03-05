
$(document).ready(function () {
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
                    $.post("/topic_manager/target", data, function (response, status) {
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


    /* 对json进行处理 */
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
        $(".all_target").replaceWith(empty_form);
        var target_id = active_table;
        var semester = $("tr[title=" + target_id + "]").find("td").eq(0).text();
        var time = $("tr[title=" + target_id + "]").find("td").eq(1).text();
        var expected_result = $("tr[title=" + target_id + "]").find("td").eq(2).text();
        var time_consumed = $("tr[title=" + target_id + "]").find("td").eq(3).text();
        var content = $("tr[title=" + target_id + "]").find("td").eq(4).text();
        var end_of_term_summary = $("tr[title=" + target_id + "]").find("td").eq(5).text();
        var expected_result_split = expected_result.split("\n");
        var time_consumed_split = time_consumed.split("\n");
        var content_split = content.split("\n");
        var end_of_term_summary_split = end_of_term_summary.split("\n");
        for (var i = 0; i < expected_result_split.length - 1; i++) {
            element_ = $(".target:first").clone(true);
            $(element_).find("input").val("");
            element_.appendTo(".all_target");
        }
        /* 赋值 */
        var date = new Date();
        var year = date.getFullYear();
        var month = date.getMonth() + 1;
        var day = date.getDate();
        $("#date").val(year + "-" + month + "-" + day);
        $("#date").addClass("is-valid");

        $("#semester").val(semester);
        $("#semester").addClass("is-valid");
        $("#time").val(time);
        for (var i = 0; i < expected_result_split.length; i++) {
            $(".expected_result").eq(i).val(expected_result_split[i]);
            $(".time_consumed").eq(i).val(time_consumed_split[i]);
            $(".content").eq(i).val(content_split[i]);
            $(".end_of_term_summary").eq(i).val(end_of_term_summary_split[i]);
            $(".expected_result").eq(i).addClass("is-valid");
            $(".time_consumed").eq(i).addClass("is-valid");
            $(".content").eq(i).addClass("is-valid");
            $(".end_of_term_summary").eq(i).addClass("is-valid");
        }
    });

    /* 点击添加按钮 */
    $("#addForm").click(function () {
        $("#form").find("input").val("");
        /* 设置日期时间 */
        var date = new Date();
        var year = date.getFullYear();
        var month = date.getMonth() + 1;
        var day = date.getDate();
        $("#date").val(year + "-" + month + "-" + day);
        $("#date").addClass("is-valid");
        $(".all_target").replaceWith(empty_form);
        if ($("tr").hasClass("table-active")) {
            $("tr").removeClass("table-active");
        }
    });


    /* 提交按钮相关功能实现 */
    $("#submitForm").click(function () {
        /* 获取输入的预期有型成果 */
        var expected_result = [];
        $(".expected_result").each(function () {
            expected_result.push($(this).val());
        });
        /* 获取输入的用时 */
        var time_consumed = [];
        $(".time_consumed").each(function () {
            time_consumed.push($(this).val());
        });
        /* 获取输入的目标说明 */
        var content = [];
        $(".content").each(function () {
            content.push($(this).val());
        });
        /* 获取输入的期末总结 */
        var end_of_term_summary = [];
        $(".end_of_term_summary").each(function () {
            end_of_term_summary.push($(this).val());
        });
        var jsonString_expected_result = JSON.stringify(expected_result);
        var jsonString_time_consumed = JSON.stringify(time_consumed);
        var jsonString_content = JSON.stringify(content);
        var jsonString_end_of_term_summary = JSON.stringify(end_of_term_summary);
        csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        var data = {
            "target_id": $("#target_id").val(),
            'date': $("#date").val(),
            'semester': $("#semester").val(),
            "expected_result": jsonString_expected_result,
            "time_consumed": jsonString_time_consumed,
            "content": jsonString_content,
            "end_of_term_summary": jsonString_end_of_term_summary,
            csrfmiddlewaretoken: csrftoken,
            "btn": ""
        }
        $.post("/topic_manager/target", data, function (response, status) {
            if (status == "success") {
                window.location.reload(true);
            }
        });
    });

    /* 点击某一行启用修改和删除按钮 */
    $("tbody tr").click(function () {
        $("#target_id").val(this.title);
        $("#deleteForm").attr("disabled", false);
        // $("#modifyForm").attr("disabled", false);
        if ($("tr").hasClass("table-active")) {
            $("tr").removeClass("table-active");
        }
        $(this).addClass("table-active");
    });

    /* 点击加号按钮，会自动增加并恢复表单的初始状态 */
    $("#add_target").click(function () {
        element_ = $(".target:first").clone(true);
        $(element_).find("input").val("");
        $(element_).find("input").removeClass("is-valid");
        $(element_).find("input").removeClass("is-invalid");
        element_.appendTo(".all_target");
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
    /* 点击空白处失去选中，并清空id记录 */
    $(document).on("click", function (e) {
        if (e.target.tagName != "TH" && e.target.tagName !== "TD") {
            $("#target_id").val();
            $("#deleteForm").attr("disabled", true);
            // $("#modifyForm").attr("disabled", true);
            if ($("tr").hasClass("table-active")) {
                $("tr").removeClass("table-active");
            }
        }
    });
});

empty_form = "                            <div class=\"all_target\">\n" +
    "                                <div class=\"target\">\n" +
    "                                    <hr>\n" +
    "                                    <div class=\"row\">\n" +
    "                                        <div class=\"form-group col-10\">\n" +
    "                                            <label for=\"expected_result\">预期有型成果</label>\n" +
    "                                            <input type=\"text\" class=\"expected_result form-control\" required></input>\n" +
    "                                            <div id=\"expected_result-valid\" class=\"valid-feedback\">\n" +
    "                                                OK\n" +
    "                                            </div>\n" +
    "                                            <div id=\"expected_result-invalid\" class=\"invalid-feedback\">\n" +
    "                                                ERROR\n" +
    "                                            </div>\n" +
    "                                        </div>\n" +
    "                                        <div class=\"form-group col-2\">\n" +
    "                                            <label for=\"content\">用时（天）</label>\n" +
    "                                            <input type=\"text\" class=\"time_consumed form-control\" placeholder=\"例：10\" required>\n" +
    "                                            <div id=\"time_consumed-valid\" class=\"valid-feedback\">\n" +
    "                                                OK\n" +
    "                                            </div>\n" +
    "                                            <div id=\"time_consumed-invalid\" class=\"invalid-feedback\">\n" +
    "                                                ERROR\n" +
    "                                            </div>\n" +
    "                                        </div>\n" +
    "                                    </div>\n" +
    "                                    <div class=\"row\">\n" +
    "                                        <div class=\"form-group col-12\">\n" +
    "                                            <label for=\"content\">目标说明</label>\n" +
    "                                            <input type=\"text\" class=\"content form-control\" required></input>\n" +
    "                                            <div id=\"content-valid\" class=\"valid-feedback\">\n" +
    "                                                OK\n" +
    "                                            </div>\n" +
    "                                            <div id=\"content-invalid\" class=\"invalid-feedback\">\n" +
    "                                                ERROR\n" +
    "                                            </div>\n" +
    "                                        </div>\n" +
    "                                    </div>\n" +
    "\n" +
    "                                    <div class=\"row\">\n" +
    "                                        <div class=\"form-group col-12\">\n" +
    "                                            <label for=\"end_of_term_summary\">期末总结</label>\n" +
    "                                            <input type=\"text\" class=\"end_of_term_summary form-control\"></input>\n" +
    "                                            <div id=\"end_of_term_summary-valid\" class=\"valid-feedback\">\n" +
    "                                                OK\n" +
    "                                            </div>\n" +
    "                                            <div id=\"end_of_term_summary-invalid\" class=\"invalid-feedback\">\n" +
    "                                                ERROR\n" +
    "                                            </div>\n" +
    "                                        </div>\n" +
    "                                    </div>\n" +
    "                                </div>\n" +
    "                            </div>"
