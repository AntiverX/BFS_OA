$(document).ready(function () {

    /* 对json进行处理，分行显示本周和下周工作 */
    $("tr").each(function () {
        if ($(this).find("td").length != 0) {
            var array_ = JSON.parse($(this).find("td").eq(-4).text());
            new_text = "";
            for (var i = 0; i < array_.length - 1; i++) {
                new_text = new_text + array_[i] + "\n\n";
            }
            new_text = new_text + array_[array_.length - 1];
            $(this).find("td").eq(-4).text(new_text);
        }
    });
    $("tr").each(function () {
        if ($(this).find("td").length != 0) {
            var array_ = JSON.parse($(this).find("td").eq(-5).text());
            new_text = "";
            for (var i = 0; i < array_.length - 1; i++) {
                new_text = new_text + array_[i] + "\n\n";
            }
            new_text = new_text + array_[array_.length - 1];
            $(this).find("td").eq(-5).text(new_text);
        }
    });

    /* 点击某一行启用修改和删除按钮并增加选中效果 */
    $("tbody tr").click(function () {
        $("#target_id").val(this.title);
        $("#deleteForm").attr("disabled", false);
        $("#modifyForm").attr("disabled", false);
        if ($("tr").hasClass("table-active")) {
            $("tr").removeClass("table-active");
        }
        $(this).addClass("table-active");
    });

    /* 点击空白处失去选中，并清空id记录 */
    $(document).on("click", function (e) {
        if (e.target.tagName == "HTML" || e.target.tagName == "DIV") {
            $("#target_id").val();
            $("#deleteForm").attr("disabled", true);
            $("#modifyForm").attr("disabled", true);
            if ($("tr").hasClass("table-active")) {
                $("tr").removeClass("table-active");
            }
        }
    });
});