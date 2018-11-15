$(document).ready(function () {
    $("tr").click(function () {
        $("#target_id").val(this.title);
        $(this).addClass("table-active");
    });
});