/* 对json进行处理，分行显示本周和下周工作 */
$(document).ready(function () {
    $("tr").each(function () {
        if ($(this).find("td").length != 0) {
            var array_ = JSON.parse($(this).find("td").eq(1).text());
            new_text = "";
            for (var i = 0; i < array_.length - 1; i++) {
                new_text = new_text + array_[i] + "\n";
            }
            new_text = new_text + array_[array_.length - 1];
            $(this).find("td").eq(1).text(new_text);
        }
    });
    $("tr").each(function () {
        if ($(this).find("td").length != 0) {
            var array_ = JSON.parse($(this).find("td").eq(2).text());
            new_text = "";
            for (var i = 0; i < array_.length - 1; i++) {
                new_text = new_text + array_[i] + "\n";
            }
            new_text = new_text + array_[array_.length - 1];
            $(this).find("td").eq(2).text(new_text);
        }
    });
});