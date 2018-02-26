function radio_can_input(ps) {
    ps.find(':text').removeAttr('disabled');
    if (ps.find('select').length != 0) {
        ps.find('select').removeAttr('disabled');
        var type_value = $("select[name='startTracking-date-type']").attr("value");
        if (type_value) {
            $("select[name='startTracking-date-type']").val(type_value);    
        }
    }
};

function radio_canot_input(ps){
    ps.find(':text').val("");
    ps.find(':text').attr('disabled', 'disabled');
    if (ps.find('select').length != 0) {
        ps.find('select').attr('disabled', 'disabled');
    }    
}

function radios_canot_input(not_this) {
    for (var i = 0; i < not_this.length; i++) {
        not_radio_id = "#" + not_this[i].id;
        not_this_ps = $(not_radio_id);
        radio_canot_input(not_this_ps);
    }
};

function radio(id) {
    ps = $(id);
    if (ps.find(":text").val() != '') {
        ps.find(".form-control.radio-group").attr("checked",true);
        radio_can_input(ps);
    }
};

function usual_do(ps, not_this){
    radio_can_input(ps);
    radios_canot_input(not_this);
}

$(function radioclick() {
    var check_id = '';
    var hasCheck = 0;
    $(".form-control.radio-group").click(function() {
        radio_id = "#" + $(this).attr("id");
        ps = $(this).parents(radio_id);
        not_this = $(".form-control.radio-group").not(this);
        if ( check_id === '' ){
            usual_do(ps, not_this);
            hasCheck = 1;
        }
        else {
            if (check_id === radio_id) {
                if (hasCheck == 0 ) {
                    usual_do(ps, not_this);        
                    hasCheck = 1;    
                }
                else{
                    $(this)[0].checked = false;
                    radio_canot_input(ps);
                    hasCheck = 0;
                }
            }
            else{
                usual_do(ps, not_this);
                hasCheck = 1;
            }
        }

        check_id = radio_id;
    });

    radio("#startTracking-time")
    radio("#startTracking-count")
    radio("#startTracking-date")
});
