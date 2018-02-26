var FormValidation = function () {

    var handleValidation = function() {

            var form = $(".admin-form,.form-horizontal");
            var error = $('.alert-danger', form);
            var success = $('.alert-success', form);

            form.validate({
                errorElement: 'span', 
                errorClass: 'help-block help-block-error', 
                focusInvalid: false,
                ignore: "",  
                rules: editRules,
                messages: {
                    interval: {
                        minlength: "至少选择一个间隔类型",
                    },
                    id: {
                        unchangedID : "不能更改ID",
                    },
                    startTracking: {
                        typeSame: "间隔类型应该和开始跟踪时间点类型一致",
                    },
                    'interval-date-type': {
                        typeCheck: "日历时间类型不正确",
                    },
                },

                errorPlacement: function(error, element) {  
                    if (element.attr('name')=='interval'){
                        element.parents('.form-group').addClass('has-error');
                        error.appendTo(element.parents('.inline-form-field'));
                    }
                    else if (element.attr('name')=='startTracking') {
                        element.parents('.form-group').addClass('has-error')
                        error.appendTo(element.parents('.inline-form-field'));  
                    }
                    else if (element.attr('name')=='interval-date-type') {
                        error.appendTo(element.parents("#interval-date"));
                    }
                    else if (element.attr('name').substring(0,4) =='acce') {
                        var n = element.attr('name').slice(-1);
                        var findClass = ".list-group-item.filename" + n;
                        element.parents('.form-group').addClass('has-error');
                        error.appendTo(element.parents().find(findClass));
                    }
                    else{
                        error.appendTo(element.parent());
                    }
                    
                },
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
                    $("input.btn-primary").attr('disabled', 'disabled')
                    form.submit();
                }
            });

    }


    return {
        
        init: function () {
            handleValidation();
        }
    };

}();