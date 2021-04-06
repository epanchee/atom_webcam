$(function () {
    "use strict";

    $(".popup img").click(function () {
        var $src = $(this).attr("src");
        $(".show").fadeIn();
        $(".img-show img").attr("src", $src);
    });

    $("span, .overlay").click(function () {
        $(".show").fadeOut();
    });

    $(document).on('keydown', function(e) {
        if (e.keyCode === 27)
            $("span, .overlay").click();
    });

});
