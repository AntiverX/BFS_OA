/*
表格项目被右击后，记录被右击的表格id
右键菜单的相关实现
添加按钮
提交按钮
 */
$(document).ready(function () {
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
    /* 右键菜单的相关实现结束 */

    /* 添加按钮 */
    $("#addForm").click(function () {
        active_table = "";
    });

    /* 提交按钮 */
    $("#submitForm").click(function () {
        alert("fuck");
        var data = {
            "target_id": active_table,
            'semester_name': $("#semester_name").val(),
            "start_date": $("#start_date").val(),
            "end_date": $("#end_date").val(),
            csrfmiddlewaretoken: jQuery("[name=csrfmiddlewaretoken]").val(),
            "btn": "",
        }
        $.post("/system/semester", data, function (response, status) {
            if (status == "success") {
                // window.location.reload(true);
            }
        });
    });
});