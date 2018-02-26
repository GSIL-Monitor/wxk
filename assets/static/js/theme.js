var setColor = function(color) {
    var color_ = (Metronic.isRTL() ? color + '-rtl' : color);
    $("#style_color").attr("href", '/static/css/' + color_ + ".css");
};

var Theme = function() {

    var handleTheme = function() {
        var panel = $('.theme-panel');

        $('.theme-colors > li', panel).click(function() {
            var color = $(this).attr("data-theme");
            setColor(color);
            $.cookie('color', color, {path:'/admin'});
            $('ul > li', panel).removeClass("active");
            $(this).addClass("active");

            if (color === 'dark') {
                $('.page-actions .btn').removeClass('red-haze').addClass('btn-default btn-transparent');
            } else {
                $('.page-actions .btn').removeClass('btn-default btn-transparent').addClass('red-haze');
            }
        });
    };

    return {
        init: function() {
            handleTheme();
            if ($.cookie && $.cookie('color')) {
                setColor($.cookie('color'));
            }
        }
    };

}();
