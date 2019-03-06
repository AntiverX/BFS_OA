$(document).ready(function () {
    $("#change_current_user").click(function () {
        var data = {
            current_user: $("[name=current_user]").val(),
            csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
        };
        $.post("/", data, function (status, data) {
            window.location.reload();
        });
    });

    $.get("/get_current_week", function (data) {
        $("#current_week").text("第" + data + "周");
        $("#week").val(data);
    });
});