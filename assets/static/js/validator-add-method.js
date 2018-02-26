function getUniqueValue(field, value) {
    var result = false;
    $.ajax({
        url: getUniqueValueURL() + "?field=" + field + "&value=" + value + '&sub=' + getSub(),
        type: "get",
        dataType: "json",
        async: false,
        success: function(data){
            if (data.message == 'Ok'){
                result = true;
            }else{
                result = false;
            }
        },
        error: function(){
            result = false;
        },
    });
    return result;
}

$.validator.addMethod("checkID", function(value){
    return getUniqueValue('id', value);
});

$.validator.addMethod("checkPieceNo", function(value){
    var old_value = $('.form-control#pieceNo').attr('value');
    if (old_value != value) {
        return getUniqueValue('pieceNo', value);
    }
    return true;
});

$.validator.addMethod("checkPN", function(value){
    var old_value = $('.form-control#pn').attr('value');
    if (old_value != value) {
        return getUniqueValue('pn', value)
    }
    return true;
});

$.validator.addMethod("typeSame", function(value){
    if (value == 'on'){
        for(var i=0; i<3; i++){
            start = $(":input[name='startTracking']")[i].checked;
            if (start == true ){
                inter = $(":input[name='interval']")[i].checked;
                if (inter == true) {
                    if (i == 2){
                        sVal = $("select[name='startTracking-date-type']").val();
                        iVal = $("select[name='interval-date-type']").val();
                        if (sVal != iVal){
                            return false;    
                        }
                    }
                    return true;
                }
                return false;
            }
        }
    } 
    else{
        return true;
    }
});

$.validator.addMethod('typeCheck', function(value){
    var offsetType = $("select[name=interval-date-offsetType]").val();
    if (value < offsetType) {
        return false;
    }
    return true;
});

$.validator.addMethod("unchangedID", function(value){
    var old_value = $('.form-control#id').attr('value')
    if (old_value != value) {
        return false;
    }
    return true;
});

$.extend($.validator.messages, {
    required: "字段不能为空",
    maxlength: jQuery.validator.format("长度最多是 {0} 个字符"), 
    minlength: jQuery.validator.format("长度最少是 {0} 个字符"), 
    number: "只能输入数字",
    checkPlus: "数字只能为正数",
    checkPN: "该型号已经存在",
    checkPieceNo: "该件号已经存在",
    fileSizeCheck: "附件大小不能超过10M",
    greaterThan0: "基准值需大于0",
    comStandard: "不能大于等于基准值",
    comDateStandard: "不能大于等于基准值",
    unitCheck: "不能选择该部件号"
});

$.validator.addMethod("checkPlus", function(value) {
    if (value != ""){
        if (value >= 0) {
            return true;
        } else {
            return false;
        }
    } else {
        return true;
    }
});

$.validator.addMethod("greaterThan0", function(value) {
  return value > 0;
});

$.validator.addMethod("fileSizeCheck", function(value, element) {
    var f = element.files[0]
    if (f != undefined) {
        size = f.size/1024/1024
        if (size > 10) {
            return false;
        }
    }
    return true;
});

$.validator.addMethod("comStandard", function(value, element) {
    stand = element.name.split('-');
    stand[2] = 'value';
    stand = stand.join('-')
    selector = "input[name="+stand+"]";
    sValue = $(selector).val();
    if (parseFloat(value) >= parseFloat(sValue)) {
        return false;
    }
    return true;
});

$.validator.addMethod("comDateStandard", function(value, element) {
    var dateType = $("select[name=interval-date-type]").val()
    var offsetType = $("select[name=interval-date-offsetType]").val();
    var dateValue = $("input[name=interval-date-value]").val()

    if (getdays(dateType, dateValue) <= getdays(offsetType, value)) {
        return false;
    }

    return true;
});

function getdays(dateType, values) {
    if (parseInt(dateType) == 4) {
        return parseFloat(values) * 365;
    }
    if (parseInt(dateType) == 3) {
        return parseFloat(values) * 30;
    }
    if (parseInt(dateType) == 2) {
        return parseFloat(values);
    }
}

$.validator.addMethod("unitCheck", function(value) {
    var pn = $("#pn").val();
    if (value == pn) {
        if (value === ''){
            return true;
        }
        return false;
    } else {
        return true;
    }
});
