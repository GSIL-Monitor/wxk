function dateDifftoHS(start, end){
    if(start){
        if(end){
            start = start.replace(/-/g,'/')
            start = new Date(start)
            end = end.replace(/-/g,'/')
            end = new Date(end)
            minutes = Math.floor(parseInt(start - end)/1000/60)
            return minutes
        }
    }
    return ''
}

function minutesToHS(minutes){
    if(minutes < 60){
        if(minutes < 10){
            if(minutes >=0){
                minutes = '0' + minutes
                str = '00:' + minutes
            }else{
                str = '00:00' 
            }
            
        }else{
            str = '00:' + minutes
        }
        
    }else{
        hour = Math.floor(parseInt(minutes/60))
        if(hour < 10){
          hour = '0'+hour
        }
        minutes = minutes % 60
        if(minutes < 10){
          minutes = '0' + minutes
        }
        str = hour + ':' + minutes
    }
    return str
}

function strToMinutes(str){
    if(str){
        var hour = parseInt(str.split(':')[0])
        var minutes = parseInt(str.split(":")[1])
        minutes = hour * 60 + minutes
        return minutes
    }else{
        return ''
    }

}

function getNowFormatDate() {
    var date = new Date();
    var seperator1 = "-";
    var seperator2 = ":";
    var month = date.getMonth() + 1;
    var strDate = date.getDate();
    if (month >= 1 && month <= 9) {
      month = "0" + month;
    }
    if (strDate >= 0 && strDate <= 9) {
      strDate = "0" + strDate;
    }
    var currentdate = date.getFullYear() + seperator1 + month + seperator1 + strDate
          + " " + date.getHours() + seperator2 + date.getMinutes()
          + seperator2 + date.getSeconds();
    return currentdate;
}

$("#flightTime").click(function(){
    if(!$(this).val()){
        var stopTime = $("[name='stopTime']").val()
        var skidoffTime = $("[name='skidoffTime']").val()
        minutes = dateDifftoHS(stopTime, skidoffTime)
        hiddenStr = '<input id="hidden_flightTime" type="hidden" value="'+minutes+'">'
        $("#hidden_flightTime").remove()
        $(this).parent().append(hiddenStr)
        str = minutesToHS(minutes)
        $(this).val(str)

        if($("#missionType").val() == '正常任务'){
        e_minutes = minutes + 2
        }else if($("#missionType").val() == '惯导任务'){
        e_minutes = minutes + 6
        }
        e_str =  minutesToHS(e_minutes) 
        e_hiddenStr = '<input id="hidden_engineTime" type="hidden" value="'+e_minutes+'">'
        $('#hidden_engineTime').remove()
        $("#engineTime").parent().append(e_hiddenStr)
        $("#engineTime").val(e_str)
    }
})

$("#flightTime").blur(function(){
  var upd_minutes = strToMinutes($(this).val())
  $("#hidden_flightTime").val(upd_minutes)
})
$("#engineTime").blur(function(){
  var upd_minutes = strToMinutes($(this).val())
  $("#hidden_engineTime").val(upd_minutes)
})



if(location.href.indexOf('edit') > 0){
    var minutes = parseInt($("#flightTime").val())
    hiddenStr = '<input id="hidden_flightTime" type="hidden" value="'+minutes+'">'
    $("#flightTime").parent().append(hiddenStr)
    str = minutesToHS(minutes)
    $("#flightTime").val(str)

    var e_minutes = parseInt($("#engineTime").val())
    e_hiddenStr = '<input id="hidden_engineTime" type="hidden" value="'+e_minutes+'">'
    $("#engineTime").parent().append(e_hiddenStr)
    e_str =  minutesToHS(e_minutes)
    $("#engineTime").val(e_str)

}

$(".admin-form").submit(function(){
    if($("#hidden_flightTime").val()){
        $("#flightTime").val($("#hidden_flightTime").val())
        $("#engineTime").val($("#hidden_engineTime").val())
    } 
})
