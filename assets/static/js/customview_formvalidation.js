var FormValidation = function () {
    var validation = function (rules) {
        var form = $('.admin-form');
        var error = $('.alert-danger', form);
        var success = $('.alert-success', form);

        form.validate({
            errorElement: 'span',
            errorClass: 'help-block help-block-error',
            focusInvalid: false,
            ignore: "",
            message: {},
            rules: rules,

            invalidHandler: function (event, validator) {
                success.hide();
                error.show();
                Metronic.scrollTo(error, -200);
            },
            highlight: function (element) {
                $(element).closest('.form-group').addClass('has-error');
            },
            unhighlight: function (element) {
                $(element).closest('.form-group').removeClass('has-error');
            },
            success: function (label) {
                label.closest('.form-group').removeClass('has-error');
            },
            submitHandler: function (form) {
                success.show();
                error.hide();
                var tableVali;
                try {
                    tableVali = inLineTable.func()
                } catch (error) {
                    tableVali = true;
                }
                var result = true

                if (tableVali) {
                    $("input.btn-circle, input.btn-primary").attr('disabled', 'disabled')
                    if (location.href.indexOf('loanreturnorder') > 0) {
                        $("#loanApplication").removeAttr('disabled')
                    }
                    if (location.href.indexOf('repairreturnorder') > 0) {
                        $("#repairApplication").removeAttr('disabled')
                    }
                    if (location.href.indexOf('routinework') > 0) {
                        result = boundedid_validate()
                    }
                    if(result){
                        form.submit();
                    }
                }
            },
        });
    };

    return {
        init: function (rules) {
            validation(rules);
        }
    };
}();

$.extend($.validator.messages, {
    required: "字段不能为空",
    checkPlus: "只能输入数字",
    checkDate: "结束时间必须大于开始时间",
});

$.validator.addMethod("checkPlus", function (value) {
    if (value != "") {
        if (value >= 0) {
            return true;
        } else {
            return false;
        }
    } else {
        return true;
    }
});

$.validator.addMethod("checkDate", function (end) {
    start = getStartDate();
    if (start && end) {
        start = Date.parse(new Date(getStartDate()));
        end = Date.parse(new Date(end));
        if (end > start) {
            return true;
        } else {
            return false;
        }
    } else {
        return false;
    }
});