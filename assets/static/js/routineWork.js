$(function(){
    ComponentsDropdowns.init();
    $("#user").select2({})
    if(location.href.indexOf('/new/') > 0){
        if(!$("#mxId").val()){
            startBlock();
            get_bounded_status($("#jihao").val()).then(function(msg){
                render_jcType(msg);
                render_mxpId(msg, $("#jcType").val());
                $.unblockUI();
            })
        }else{
            startBlock();
            get_bounded_status($("#jihao").val()).then(function(msg){
                render_jcType(msg, $("#jcType").val());
                render_mxpId(msg, $("#jcType").val(), $("#mxId").val());
                $.unblockUI();
            })
        }
    }else if(location.href.indexOf('/approve-edit-view/') > 0){

        startBlock();
        get_bounded_status($("#jihao").val()).then(function(msg){
            render_jcType(msg, $("#jcType").val());
            if(typeof(localStorage['submit']) == "undefined"){
                render_mxpId(msg, $("#jcType").val(), $('#mxId').val());
            }else{
                render_mxpId(msg, $("#jcType").val(), localStorage['submit']);
            }
            aggregate_sn($("#jcType").val(), $('#mxId').val(), msg, $("#serialNumber").val());
            $.unblockUI();
            
        })
        localStorage.removeItem('submit')
    }

    if($("#jcType").val() == '时控件' || $("#jcType").val() == '时寿件'){
        $("[for='aircraftPn'],[for='serialNumber']").parent().show()
    }else{
        $("[for='aircraftPn'],[for='serialNumber']").parent().hide()
    }
    
    //更改元素位置
    $($("[for='planeType']").parent()).insertAfter($("[for='lxgzNum']").parent())
    $($("[for='jihao']").parent()).insertAfter($("[for='planeType']").parent())
    $($("[for='jcType']").parent()).insertAfter($("[for='jihao']").parent())
    $($("[for='mxId']").parent()).insertAfter($("[for='jcType']").parent())
    $($("[for='serialNumber']").parent()).insertAfter($("[for='aircraftPn']").parent())

    /*
        机型更改事件
    */
    $(document).on('change', '#planeType', function(){
        var value = $(this).val()
        $("#jihao").val('')
        $("#jihao [data-type='"+ value +"'").show()
        $("#jihao :not([data-type='"+ value +"'])").hide()
    })

    /*
        飞机注册号更改事件
    */
    $(document).on('change', '#jihao', function(){
        var value = $(this).val()
        var type = $("[value='"+ value +"']").attr('data-type')
        $("#planeType").val(type)
        $("#jcType,#aircraftPn,#description,#mxId,#serialNumber").val('')
        // $(".child-sn").remove()

        startBlock()

        get_bounded_status(value).then(function(msg){
            render_jcType(msg);
            render_mxpId(msg, $("#jcType").val());
            $.unblockUI();
        })

    })

   $("[name='jcTime']").attr('readonly','readonly')
   
    //获取维修方案编号
    // mxId($('#jcType').val())
    //检查类别更改事件
    $(document).on('change', "#jcType", function(){
        var mx_type = $(this).val()
        var plane_id = $("#jihao").val()
        startBlock()

        get_bounded_status(plane_id).then(function(msg){
            $.unblockUI();
            render_mxpId(msg, mx_type)
        })

        /*显示/隐藏Pn件号*/
        pn_toggle(mx_type)
  
    })

    /*
        维修方案编号更改事件
    */
    $(document).on('change', '#mxId',function(){
        var value = $(this).val();
        if($("#jcType").val() != '时控件' && $("#jcType").val() != '时寿件'){
            var id = $("#mxId option[value='"+value+"']").attr('boundedid')
            if(id){
                $("#boundedid").val(id)
            }
        }
        console.log(id)
        description(value)  /*找对应的描述信息*/
        startBlock();
        get_bounded_status($("#jihao").val()).then(function(msg){
            $.unblockUI();
            return aggregate_sn($("#jcType").val(), value, msg);
        })
        
    })

})

function startBlock(){
    $.blockUI({ css:{ backgroundColor:'none','color':'#fff'},message: '<h1>正在加载<img src="/static/img/loading-spinner-blue.gif" .>' });
    $(".blockUI").css('z-index','100511');
}

function render_mxpId(msg, mx_type, value){
    var str = '<select class="form-control" id="mxId" name="mxId">';
    jQuery.each(msg, function(i, val){
        if(i == mx_type){
            jQuery.each(val, function(k, v){
                if(v){
                    var boundedId = v[0]
                    var pn = v[1]
                    var sn = v[2]
                    var mxpId = v[3]
                    var mxpType = v[4]
                    var description = v[5]
                    str += '<option sn="'+sn+'" boundedId="'+boundedId+'" description="'+description+'" pn="'+pn+'" value="'+mxpId+'">'+mxpId+'</option>'
                }
            })
            str += '</select>'
            $("#mxId").parent().html(str)
            if(value){
                $("#mxId").val(value)
                if($("#serialNumber").val()){
                    aggregate_sn(mx_type, $("#mxId").val(), msg, $("#serialNumber").val())
                }else{
                  aggregate_sn(mx_type, $("#mxId").val(), msg)  
                }
            }else{
                aggregate_sn(mx_type, $("#mxId").val(), msg)
            }
            if($("#jcType").val() != '时控件' && $("#jcType").val() != '时寿件'){
                var id = $("#mxId option[value='"+$("#mxId").val()+"']").attr('boundedid')
                if(id){
                    $("#boundedid").val(id)
                }
            }
        }
        
    })
    description($("#mxId").val())
}

function aggregate_sn(mx_type, mxp_id, data, value) {
    if (mx_type != '时控件' && mx_type != '时寿件') return;
    var allowed_bounded_status = data[mx_type];
    if(value){
        get_subsidiary_work($("#jihao").val(), mxp_id).then(function(msg){
            if(msg.code == 200){
                if(msg.subsidiaries.length > 0){
                    var arr = []
                    for(var i = 0; i < msg.subsidiaries.length; i++)
                    {
                        arr.push(msg.subsidiaries[i]['boundedId'])
                    }
                    arr = arr.join(',')
                    if($("#boundedid").val().indexOf(arr) >= 0 && (!$(".child-sn").html())){
                        var str = '<div class="form-group child-sn"><label class="col-md-2 control-label">子件</label><div class="col-md-10"><table class="table table-hover table-bordered table-striped basic_infomation profile-desc-text"> <thead>'
                        str += '<tr><td class="col-md-3">维修方案编号</td><td class="col-md-3">型号</td><td>序号</td><td>维修方案描述</td></tr>'
                        var boundedids = new Array()
                        for(var i = 0; i < msg.subsidiaries.length; i++){
                            boundedids.push(msg.subsidiaries[i]['boundedId'])
                            j = parseInt(i) + 1
                            str += ' <tr><td class="col-md-2">'+msg.subsidiaries[i]['id']+' </td>  <td class="col-md-2">'+msg.subsidiaries[i]['pn']+' </td><td>'+msg.subsidiaries[i]['sn']+' </td><td>'+msg.subsidiaries[i]['description']+' </td> </tr> '
                        }
                        str += '<input type="hidden" id="child">'
                        str += '</thead> </table></div></div>'

                        if(str){
                            $(".form-body").append(str)
                            $("#child").val(boundedids)
                        }
                    }
                }
            }
            var sn_str = '<select class="form-control" multiple="multiple" id="SN" name="SN">';
            jQuery.each(allowed_bounded_status, function(k, v) {
                if(v){
                    var boundedId = v[0]
                    var sn = v[2]
                    if(v[3] == mxp_id){
                        if(v['sn'].length > 0){
                            for(x in v['sn']){
                                if(v['sn'][x]['sn']){
                                    sn_str += '<option b_id="'+v['sn'][x]['boundedid']+'" value="'+v['sn'][x]['sn']+'">'+v['sn'][x]['sn']+'</option>'
                                }
                            }
                        }else if(sn){
                            sn_str += '<option b_id="'+boundedId+'" selected="selected" value="'+sn+'">'+sn+'</option>'
                        }
                    }
                }
                
            })
            sn_str += '</select>'
            $("#serialNumber").parent().html(sn_str)
            $("#SN").parent().append('<input type="hidden" name="serialNumber" id="serialNumber" value="'+value+'">')

            pn_toggle(mx_type)
            arr = value.split(',');
            $("#SN").select2()
            $("#SN").select2('val', arr)
        })
    }else{
        get_subsidiary_work($("#jihao").val(), mxp_id).then(function(msg){
            if(msg.code == 200){
                if(msg.subsidiaries.length > 0){
                    if(window.confirm('该方案下有已跟踪的子方案，是否同时创建？')){
                        var str = '<div class="form-group child-sn"><label class="col-md-2 control-label">子件</label><div class="col-md-10"><table class="table table-hover table-bordered table-striped basic_infomation profile-desc-text"> <thead>'
                        str += '<tr><td class="col-md-3">维修方案编号</td><td class="col-md-3">型号</td><td>序号</td><td>维修方案描述</td></tr>'
                        var boundedids = new Array()
                        for(var i = 0; i < msg.subsidiaries.length; i++){
                            boundedids.push(msg.subsidiaries[i]['boundedId'])
                            j = parseInt(i) + 1
                            str += ' <tr><td class="col-md-2">'+msg.subsidiaries[i]['id']+' </td>  <td class="col-md-2">'+msg.subsidiaries[i]['pn']+' </td><td>'+msg.subsidiaries[i]['sn']+' </td><td>'+msg.subsidiaries[i]['description']+' </td> </tr> '
                        }
                        str += '<input type="hidden" id="child">'
                        str += '</thead> </table></div></div>'

                        if(str){
                            $(".form-body").append(str)
                            $("#boundedid, #child").val(boundedids)
                        }
                    }
                }else{
                    $(".child-sn").remove()
                }
            }
            var sn_str = '<select class="form-control" multiple="multiple" id="SN" name="SN">';
            jQuery.each(allowed_bounded_status, function(k, v) {
                if(v){
                    var boundedId = v[0]
                    var sn = v[2]

                    if(v[3] == mxp_id){
                        if(v['sn'].length > 0){
                            for(x in v['sn']){
                                if(v['sn'][x]['sn']){
                                    sn_str += '<option b_id="'+v['sn'][x]['boundedid']+'" value="'+v['sn'][x]['sn']+'">'+v['sn'][x]['sn']+'</option>'
                                }
                            }
                        }else if(sn){
                            sn_str += '<option b_id="'+boundedId+'" value="'+sn+'">'+sn+'</option>'
                        }
                    }
                }
            })
            sn_str += '</select>'
            $("#serialNumber").parent().html(sn_str)
            $("#SN").parent().append('<input type="hidden" name="serialNumber" id="serialNumber">')
            pn_toggle(mx_type)
            $("#SN").select2({});
        })


    }
    
     $(document).on('change', "#SN", function(e){
        var serialNumberVal = $(this).val()
        var ids = []
        for(x in serialNumberVal){
            ids[x] = $("#SN option[value='"+serialNumberVal[x]+"']").attr('b_id')
        }
            $('#serialNumber').val(serialNumberVal)
            if($('.table').html()){
                // concat()
                var oldArr = $("#child").val()
                oldArr = oldArr.split(',')
                $('#boundedid').val(oldArr.concat(ids))
                
                
            }else{
                $('#boundedid').val(ids)
            }
    })
}

function get_subsidiary_work(planeId, mxId){
    var action = new Promise(function(resolve,reject){
        $.get('/admin/aircraft_informationview/get-subsidiary-work/', 
            {
                plane:planeId,
                mxid:mxId,
            }, 
            function(msg){
                resolve(msg);
            });
    });
    return action;
}
//在数组中获取指定值的元素索引  
Array.prototype.getIndexByValue= function(value)  
{  
    var index = -1; 
    for (var i = 0; i < this.length; i++) 
    { 
        if (this[i] == value)  
        {
            index = i;
            break;
        }
    }  
    return index;    
} 

function render_jcType(msg, value){
    var str = '<select class="form-control" id="jcType" name="jcType">';
    jQuery.each(msg, function(i, val){
        str += '<option value="'+ i +'">'+ i +'</option>'
    })
    str += '</select>'
    $("#jcType").parent().html(str)
    if(value){
        $("#jcType").val(value)
    }
    $(".child-sn").remove()

}

function pn_toggle(mx_type){
    if(mx_type == '时控件' || mx_type == '时寿件'){
        $("[for='aircraftPn'],[for='serialNumber']").parent().show()
        $("[for='serialNumber']").find("strong").remove()
        $("[for='serialNumber']").append('<strong style="color: red">*</strong>')

    }else{
        $("[for='aircraftPn'],[for='serialNumber']").parent().hide()
    }
}

function description(value){
    var mx_type = $("#jcType").val()
    if(mx_type == '时控件' || mx_type == '时寿件'){
        var pn = $("#mxId [value='"+value+"']").attr('pn')
        $("#aircraftPn").val(pn)
    }else{
        $("#aircraftPn").val('')
    }
    var description = $("#mxId [value='"+value+"']").attr('description')
    $("#description").val(description).removeAttr('disabled')
}

function in_array(search, array){for(var i in array){if(array[i] == search){return true; } } return false; }
/*
    选中飞机后获取对应的绑定状态
*/
function get_bounded_status(value){
    var action = new Promise(function(resolve,reject){
        $.get('/admin/routinework/get-bounded-status/', {planeId:value}, function(msg){
            var list = []
            var sn_arr = []
            var i = 0;
            jQuery.each(msg.data, function(k, v) {
                if (k == '时控件' || k == '时寿件') {
                    /*以下作用是遍历维修方案编号,去掉重复,把序号组成数组加到编号data里*/
                    jQuery.each(v, function(k1, v1){
                        if(v1){
                           if(!in_array(v1[3], list)){
                               list.push(v1[3])
                               if(typeof(v1['sn']) != 'object'){
                                v1['sn'] = []
                               }
                           }else{
                            //如果有重复的
                            var boundedid = v1[0]
                            
                            jQuery.each(v, function(k2, v2){
                                if(v2 && v2[0] == boundedid){
                                     delete msg.data[k][k1]
                                    jQuery.each(v, function(k3, v3) {
                                        if(v3 && v3[3] == v1[3] && typeof(v3['sn']) == 'object'){
                                            var self_arr = []
                                            self_arr['boundedid'] = v3[0]
                                            self_arr['sn'] = v3[2]
                                            v3['sn'][0] = self_arr

                                            i++;
                                            v3['sn'][i] = []
                                            v3['sn'][i]['boundedid'] = v1[0]
                                            v3['sn'][i]['sn'] = v1[2]
                                        }
                                    })
                                }
                            })
                           }
                        }
                    })
                }
            })
            resolve(msg.data);
        });
    });
    return action;
}
function boundedid_validate(){
    if(!localStorage['submit']){
        localStorage.submit = $("#mxId").val()
    }
    var result = true
    if($("#jcType").val() == '时控件' || $("#jcType").val() == '时寿件'){
        if(!$("#serialNumber").val()){
            var str = '<ul style="color: #a94442" class="help-block input-errors"> <li>该字段是必填字段。</li> </ul>'
            $("#serialNumber").parent().find('.input-errors').remove()
            $("#s2id_SN").parent().append(str)
            $("input.btn-circle, input.btn-primary").removeAttr('disabled')
            result = false
        }
        if($("#serialNumber").val() && !$("#boundedid").val()){
            alert('发现未知错误，请重新选择序号')
            $("input.btn-circle, input.btn-primary").removeAttr('disabled')
            result = false
        }
    }
    return result
}

if(location.href.indexOf("/action-view/") > 0){
    $("b").each(function(){
        if($(this).html() == 'Boundedid'){
            $(this).parent().parent().hide()
        }
    })
}
if(location.href.indexOf("/details/") > 0){
    $("b").each(function(){
        if($(this).html() == '维修方案编号'){
           mxp_id =  $.trim($(this).parent().next().html());
        }
        if($(this).html() == '飞机注册号'){
           plane_id =  $.trim($(this).parent().next().html());
        }
        if($(this).html() == '单据编号'){
           routine_number = $(this).parent().parent();
        }
        if($(this).html() == '状态'){
           routine_status = $(this).parent().parent();
        }
        if($(this).html() == '机型'){

           $(this).parent().parent().insertAfter($(routine_number));
        }
        if($(this).html() == '检查类型'){

           type = $.trim($(this).parent().next().html())
           if(in_array(type, ['停放检查', '航线检查', '定期维修检查'])){
                $("b").each(function(){
                    if($(this).html() == '型号' || $(this).html() == '序号'){
                       $(this).parent().parent().hide();
                    }
                })
           }
        }

        if($(this).html() == 'Boundedid'){
            $(this).parent().parent().hide()
            var oldArr = $.trim($(this).parent().next().html());
            get_subsidiary_work(plane_id, mxp_id).then(function(msg){
                if(msg.code == 200){
                    if(msg.subsidiaries.length > 0){
                        var arr = []
                        for(var i = 0; i < msg.subsidiaries.length; i++)
                        {
                            arr.push(msg.subsidiaries[i]['boundedId'])
                        }
                        arr = arr.join(',')
                        if(oldArr.indexOf(arr) >= 0 && (!$(".child-sn").html()))
                        {

                            var str = '<td style="min-width: 150px;"><b>子件</b></td><td><table class="table table-hover table-bordered table-striped basic_infomation profile-desc-text"> <thead>'
                            // var str = '<div class="form-group child-sn"><label class="col-md-2 control-label">子件</label><div class="col-md-10"><table class="table table-hover table-bordered table-striped basic_infomation profile-desc-text"> <thead>'
                            str += '<tr><td class="col-md-3">维修方案编号</td><td class="col-md-3">型号</td><td>序号</td><td>维修方案描述</td></tr>'
                            var boundedids = new Array()
                            for(var i = 0; i < msg.subsidiaries.length; i++){
                                boundedids.push(msg.subsidiaries[i]['boundedId'])
                                j = parseInt(i) + 1
                                str += ' <tr><td class="col-md-2">'+msg.subsidiaries[i]['id']+' </td>  <td class="col-md-2">'+msg.subsidiaries[i]['pn']+' </td><td>'+msg.subsidiaries[i]['sn']+' </td><td>'+msg.subsidiaries[i]['description']+' </td> </tr> '
                            }
                            str += '</thead> </table></td>'
                            var element = $("<tr></tr>").html(str)
                            if(str){
                                element.insertAfter(routine_status)
                            }
                        }
                    }else{
                        $(".child-sn").remove()
                    }
                }
            })
        }
    })
}