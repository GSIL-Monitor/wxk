function addhover(selector) {
    selector.each(function() {
        $(this).addClass('popovers')
               .attr({'data-container':'body',
                      'data-trigger':'hover',
                      'data-placement':'bottom',
                     });
        $(this).attr('data-content', $.trim($(this).html()));
    });
}

function colAddHover() {
    var desc = $("td.col-description");
    var remark = $("td.col-remark");
    var pn_col = $("td.col-pn");
    var name_col = $("td.col-name");

    var col_list = new Array(desc, remark, pn_col, name_col);
    for (var i=0;i<col_list.length;i++) {
        addhover(col_list[i]);
    } 
}

$(colAddHover());