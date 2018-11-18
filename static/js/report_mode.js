$(document).ready(function () {
    $("tr").click(function () {
        $("#target_id").val(this.title);
        $(this).addClass("table-active");
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