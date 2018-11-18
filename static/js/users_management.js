$(document).ready(function () {

    /* 禁用按钮 */
    $("#deleteForm").attr("disabled", true);
    $("#modifyForm").attr("disabled", true);
    $("#submitForm").attr("disabled", true);

    /* 点击某一行启用修改和删除按钮 */
    $("tr").click(function () {
        $("#target_id").val(this.title);
        $("#deleteForm").attr("disabled", false);
        $("#modifyForm").attr("disabled", false);
        if ($("tr").hasClass("table-active")) {
            $("tr").removeClass("table-active");
        }
        $(this).addClass("table-active");
    });

    /* 点击空白处失去选中 */
    $(document).on("click", function (e) {
        console.log(e.target);
        console.log(e.target.tagName);
        if (e.target.tagName != "TH" && e.target.tagName === "TD") {

        }
    });
});