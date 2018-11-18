$(document).ready(function () {
    /* 表单验证 */
    $(document).on('change', 'input', function () {
        /* 在线验证表单内容 */
        text = $(this).val();
        class_name = $(this).attr('id');
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
});