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


});