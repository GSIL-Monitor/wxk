var ids = ["hours", "times", "date", 
           "retire", "torque", "gasifier", 
           "turbo", "engine"];

function selected_check(id_list) {
    for (var i in id_list) {
        var id = "#interval-" + id_list[i];
        check(id);
    }
}

function check_can_input(ps) {
    ps.find(':text').removeAttr('disabled');
    if (ps.find('select').length != 0) {
        ps.find('select').removeAttr('disabled');
        var type_value = $("select[name='interval-date-type']").attr("value");
        var offsetType_value = $("select[name='interval-date-offsetType']").attr("value");
        if (type_value && offsetType_value) {
            $("select[name='interval-date-type']").val(type_value);
            $("select[name='interval-date-offsetType']").val(offsetType_value);
        }
    }
};

function check(id) {
    ps = $(id);
    p = ps.find(".form-control.check-group");
    if (ps.find(":text").val() != '') {
      p.attr('checked',true);
      check_can_input(ps);
    }
};

function interval_canot_input(ps) {
    ps.find(":text").val("");
    ps.find(":text").attr('disabled', 'disabled');
    if (ps.find('select').length != 0) {
        ps.find('select').attr('disabled', 'disabled');
    }

}
function intervals_canot_input(not_this) {
    for (var i = 0; i < not_this.length; i++) {
        radio_id = "#" + not_this[i].id;
        not_this_ps = $(radio_id);
        interval_canot_input(not_this_ps);
    }
};

$(function checkclick() {
    $(".form-control.check-group").click(function() {
        check_id = "#" + $(this).attr('id');
        ps = $(this).parents(check_id);
        if ($(this).attr('type') === 'checkbox') {
            if ($(this).is(':checked')) {
                check_can_input(ps);
            } 
            else {
                interval_canot_input(ps);
            }
        }
        else {
            if ($(this).is(':checked')) {
                check_can_input(ps);
            }
            not_this = $(".form-control.check-group").not(this);
            intervals_canot_input(not_this); 
        }
    });

    selected_check(ids);

});
