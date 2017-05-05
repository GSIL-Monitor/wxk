$(function() {
  $(".check-group")
    .click(function() {
      p = $(this)
        .parent();
      check_id = "#" + $(this)
        .attr('name');
      ps = $(this)
        .parents(check_id);
      if (p.attr('class') === '') {
        p.attr('class', 'checked');
        ps.find(':text')
          .removeAttr('disabled');
        if (ps.find('select')
          .length != 0) {
          ps.find('select')
            .removeAttr('disabled');
        }
      } else {
        p.attr('class', '');
        ps.find(':text')
          .attr('disabled', true);
        if (ps.find('select')
          .length != 0) {
          ps.find('select')
            .attr('disabled', true);
        }
      }
    });
});
