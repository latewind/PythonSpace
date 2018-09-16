$(document).ready(function(){
    $(".side-img").hover(function(){
        $(this).siblings().removeClass("img-active");
        $(this).addClass("img-active");
        var sideImgSrc = $(this).prop("src");
        console.log(sideImgSrc);

        $(this).parent().siblings(".main-img").find("img").prop("src", sideImgSrc);
    })

});

/*跳转到页面位置*/
function jumpPage(id) {
    $("html,body").animate({scrollTop: $("#"+id).offset().top - 150}, 500);//定位到《静夜思》
}