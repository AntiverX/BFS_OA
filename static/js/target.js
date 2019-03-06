/*
初始时保存一份空白的表
初始时禁用提交按钮
点击主界面左下角添加按钮
表格项目被右击后，记录被右击的表格id
右键菜单的相关实现
对json进行处理
删除按钮实现
修改按钮实现
添加按钮实现
提交按钮实现
点击加号增加表单
表单验证（服务端验证和本地验证）
*/
$(document).ready(function () {
    column_name = []
    column_type = []
    $("th").each(function () {
        if ($(this).attr('class') == undefined) {

        } else {
            column_name.push($(this).attr('class'));
            column_type.push($(this).attr('type'));
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
                    $("#add").click();
                }
            },
            modify: {
                name: "修改",
                icon: "edit",
                callback: function (key, opt) {
                    $("#form").html(empty_form);
                    var is_sub_form_constructed = 0;
                    for (var i = 0; i < column_name.length; i++) {
                        if (column_type[i] == "json") {
                            var data = $("tr[title=" + active_table + "]").find("." + column_name[i]).text().split("\n");
                            if (is_sub_form_constructed == 0) {
                                element_ = $(".target:first").clone(true);
                                for (var j = 0; j < data.length; j++) {
                                    $(element_).find("input").val("");
                                    element_.appendTo(".all_record");
                                }
                                is_sub_form_constructed = 1;
                            }
                            console.log(column_name[i]);
                            for (var j = 0; j < data.length; j++) {
                                console.log(column_name[i]);
                                $("#form").find("." + column_name[i]).eq(j).val(data[j]);

                            }
                        } else {
                            $("." + column_name[i]).val($("tr[title=" + active_table + "]").find("." + column_name[i]).text());
                        }
                    }
                    $("input").addClass("is-valid");
                    $("#modal").modal('show');
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
                    $.post("", data, function (response, status) {
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
    /* 右键菜单的相关实现结束 */

    /* 修改按钮相关实现 */
    function modifyForm() {
        $("#form").html(empty_form);
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
            element_.appendTo(".all_record");
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
        $("#modal").modal('show');
    }
    /* 修改按钮相关实现结束 */

    /* 提交按钮相关功能实现 */
    $("#submit_form").click(function () {
        /* 获取输入的预期有型成果 */
        var expected_result = [];
        $("#form").find(".expected_result").each(function () {
            expected_result.push($(this).val());
        });
        /* 获取输入的用时 */
        var time_consumed = [];
        $("#form").find(".time_consumed").each(function () {
            time_consumed.push($(this).val());
        });
        /* 获取输入的目标说明 */
        var content = [];
        $("#form").find(".content").each(function () {
            content.push($(this).val());
        });
        /* 获取输入的期末总结 */
        var end_of_term_summary = [];
        $("#form").find(".end_of_term_summary").each(function () {
            end_of_term_summary.push($(this).val());
        });
        var jsonString_expected_result = JSON.stringify(expected_result);
        var jsonString_time_consumed = JSON.stringify(time_consumed);
        var jsonString_content = JSON.stringify(content);
        var jsonString_end_of_term_summary = JSON.stringify(end_of_term_summary);
        csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        var data = {
            "target_id": active_table,
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


});
