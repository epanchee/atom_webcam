$(function () {
    "use strict";

    $(".popup img").click(function () {
        let src = $(this).attr("src");
        $(".show").fadeIn();
        $(".img-show img").attr("src", src);
    });

    $(".next-image").click(function (){
        let cur_src = $(".img-show img").attr("src")
        $(".img_container img[src='"+cur_src+"']").parent().next().find('img').click()
    })

    $(".prev-image").click(function (){
        let cur_src = $(".img-show img").attr("src")
        $(".img_container img[src='"+cur_src+"']").parent().prev().find('img').click()
    })

    $(".close-image, .overlay").click(function () {
        $(".show").fadeOut();
    });

    $(document).on('keydown', function(e) {
        let image_controls = {
            27: '.close-image',
            37: '.prev-image',
            39: '.next-image'
        }
        if (Object.keys(image_controls).includes(e.keyCode + "") && $(".show").is(":visible"))
            $(image_controls[e.keyCode]).click()
    });

});
