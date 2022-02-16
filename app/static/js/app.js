$(function () {
    // toggle show cart
    $(".cart").on("click", function () {
        console.log('kkk');
        $(".shopping-cart").toggleClass("d-none");
    });
    hideCartOnClickAway('.shopping-cart')
})

function hideCartOnClickAway(selector) {
    $(document).on('mouseup',function (e) {
        var container = $(selector);

        // if the target of the click isn't the container nor a descendant of the container
        if (!container.is(e.target) && container.has(e.target).length === 0 && container.css('display') != 'none') {
            container.addClass("d-none")
        }
    });
}