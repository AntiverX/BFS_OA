$(document).ready(function () {
    /* 对json进行处理，分行显示主题和主题内容说明 */
    $("tr").each(function () {
        if ($(this).find("td").length != 0) {
            var array_ = JSON.parse($(this).find("td").eq(-1).text());
            theme_content = "";
            for (var i = 0; i < array_.length - 1; i++) {
                theme_content = theme_content + array_[i] + "\n\n";
            }
            theme_content = theme_content + array_[array_.length - 1];
            $(this).find("td").eq(-1).text(theme_content);
        }
        /* 对主题内容说明进行处理 */
        var theme_content_length = new Array();
        if ($(this).find("td").length != 0) {
            var array_ = JSON.parse($(this).find("td").eq(-2).text());
            new_text = "";
            for (var i = 0; i < array_.length - 1; i++) {
                new_text = new_text + array_[i].trim() + "\n\n";
                console.log(array_[i].trim());
                theme_content_length[i] = array_[i].trim().split("\n").length;
            }
            new_text = new_text + array_[array_.length - 1].trim();
            theme_content_length[array_.length - 1] = array_[array_.length - 1].trim().split("\n").length;
            $(this).find("td").eq(-2).text(new_text);
            console.log(theme_content_length);
        }

        if ($(this).find("td").length != 0) {
            var array_ = JSON.parse($(this).find("td").eq(-3).text());
            new_text = "";
            for (var i = 0; i < array_.length - 1; i++) {
                new_text = new_text + array_[i] + "\n\n";
                for (var j = 0; j < theme_content_length[i] - 1; j++) {
                    new_text = new_text + "\n";
                }
            }
            new_text = new_text + array_[array_.length - 1];
            $(this).find("td").eq(-3).text(new_text);
        }
    });
    /* 对json进行处理，分行显示主题和主题内容说明结束 */
});