/*
右键菜单的相关实现
获得列名和列类型
对json进行处理
初始时保存一份空白的表
初始时禁用提交按钮
添加按钮
加号按钮
表格项目被右击后，记录被右击的表格id
提交表单
表单验证
*/
$(document).ready(function () {
    var active_table;
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
                            for (var j = 0; j < data.length; j++) {
                                $("#form").find("." + column_name[i]).eq(j).val(data[j]);

                            }
                        } else if (column_type[i] == "select") {
                            $("." + column_name[i]).val($("tr[title=" + active_table + "]").find("." + column_name[i]).text() == "是" ? 1 : 0);
                        } else {
                            $("." + column_name[i]).val($("tr[title=" + active_table + "]").find("." + column_name[i]).text());
                        }
                    }
                    $("input,select,textarea").addClass("is-valid");
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

    /* 获得列名和列类型 */
    column_name = []
    column_type = []
    $("th").each(function () {
        if ($(this).attr('class') == undefined) {

        } else {
            column_name.push($(this).attr('class'));
            column_type.push($(this).attr('type'));
        }
    });
    /* 获得列名和列类型结束 */

    /* 对json进行处理 */
    $(".table_content").each(function () {
        for (i = 0; i <= $(this).find("td").length; i++) {
            if ($(this).find("td").eq(i).attr('type') == "json") {
                var array_ = JSON.parse($(this).find("td").eq(i).text());
                new_text = "";
                for (j = 0; j < array_.length - 1; j++) {
                    new_text = new_text + array_[j] + "\n\n";
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

    /* 添加按钮 */
    $("#add").click(function () {
        active_table = "";
        $('#form').html(empty_form);
        /* 设置日期时间 */
        var date = new Date();
        var year = date.getFullYear();
        var month = date.getMonth() + 1;
        var day = date.getDate();
        $("#date").val(year + "-" + month + "-" + day);
        $("#date,select").addClass("is-valid");
        $("#modal").modal('show');
    });

    /* 加号按钮 */
    $(document).on('click', '#add_target', function () {
        element_ = $(".record:first").clone(true);
        $(element_).find("input").val("");
        $(element_).find("input").removeClass("is-valid");
        $(element_).find("input").removeClass("is-invalid");
        element_.appendTo(".all_record");
        $("#submit_form").attr("disabled", true);
    });
    /* 加号按钮结束 */

    /* 表格项目被右击后，记录被右击的表格id */
    $('tr').mousedown(function (event) {
        if (event.which == 3) {
            active_table = this.title;
        }
    });

    /* 提交表单 */
    $("#submit_form").click(function () {
        console.log("submit form.");
        var data_test = {};
        data_test['target_id'] = active_table;
        data_test['btn'] = "";
        data_test['csrfmiddlewaretoken'] = jQuery("[name=csrfmiddlewaretoken]").val();
        for (var i = 0; i < column_name.length; i++) {
            if (column_type[i] == "json") {
                var array = [];
                $("#form").find("." + column_name[i]).each(function () {
                    array.push($(this).val());
                });
                var json_array = JSON.stringify(array);
                data_test[column_name[i]] = json_array;
            } else {
                data_test[column_name[i]] = $("#form").find("." + column_name[i]).val();
            }
        }
        console.log(data_test);
        /* 提交表单内容 */
        $.post("", data_test, function (response, status) {
            if (response == "success") {
                window.location.reload(true);
            }
        });
    });
    /* 提交表单结束 */

    /* 表单验证 */
    $(document).on('change', 'input,textarea', function () {
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
                if ($(this).hasClass("end_of_term_summary")) {

                } else {
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