$(function(){
    $(".col-warningLevel").each(function(){
        var level = $.trim($(this).html());
        var tr = $(this).parent();
        if(level == '严重超时' || level == '3级预警'){
            tr.addClass('bg-red-intense');
        }else if(level == '1级预警'){
            tr.addClass('bg-yellow-crusta');
        }else if(level == '2级预警'){
            tr.addClass('bg-yellow-casablanca');
        }else if(level == '未知'){
            tr.addClass('bg-grey-silver');
        }
    });
});