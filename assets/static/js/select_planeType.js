$(function(){
    $(document).on('change', '#planeType', function(){
        var value = $(this).val()
        $("#jihao").val('')
        $("#jihao [data-type='"+ value +"'").show()
        $("#jihao :not([data-type='"+ value +"'])").hide()
        if(location.href.indexOf('airworthiness') > 0){
            $("#jihao [data-type='"+ value +"'").prop("disabled", false);
            $("#jihao :not([data-type='"+ value +"'])").prop("disabled", true);
        }
    })

    if(location.href.indexOf('maintenancerecord') > 0){
        if(location.href.indexOf('id') > 0){
            $("#faultReports, #jihao").attr('disabled', 'disabled')
        }
    }
    if(location.href.indexOf('repairreturnorder') > 0){
        if(location.href.indexOf('id') > 0){
            $("#repairApplication").attr('disabled', 'disabled')
        }
    }

    if(location.href.indexOf('loanreturnorder') > 0){
        if(location.href.indexOf('id') > 0){
            $("#loanApplication").attr('disabled', 'disabled')
        }
    }

    if(location.href.indexOf('troubleshooting') >  0){
            $("#faultReports, #jihao").attr('disabled', 'disabled')  
    }
    if(location.href.indexOf('examinerepairrecord') > 0){
        if(location.href.indexOf('troubleshooting') > 0){
            $("#troubleShooting, #jihao").attr('disabled', 'disabled')
        }
    }


    if(location.href.indexOf('engineeringorder') > 0){
        if(location.href.indexOf('id') > 0){
            if($("#airworthiness").val()!='__None'){
                $("#airworthiness").attr('disabled', 'disabled')
            }
        }
    }

    if(location.href.indexOf('engineeringorder/approve-edit-view') > 0){
        var value = $("[name='repeatePeriod-type']").attr('for')
        if(value){
            $("[name='repeatePeriod-type'] option[value='"+value+"']").attr('selected', 'selected')
        }
    }
})

$(".admin-form").submit(function(){
    if(location.href.indexOf('examinerepairrecord') > 0){
        if(location.href.indexOf('troubleshooting') > 0){
            if($("[name='faultDate']").val()){
                $("#troubleShooting, #jihao").removeAttr("disabled")
            }
        }

    }
    if(location.href.indexOf('engineeringorder') > 0){
        if(location.href.indexOf('id') > 0){
            if($("#insTitle").val() && $("[name='repeatePeriod-value']").val() && $("#ataCode").val()){
                $("#airworthiness").removeAttr("disabled")
            }
        }
        
    }
    if(location.href.indexOf('troubleshooting') >  0){
        if($("[name='formulateDate']").val()&&$("#description").val() && $("#maintainStep").val() && $("[name='enforceDate']").val() && $("#enforceStaff").val()){
            $("#faultReports, #jihao").removeAttr("disabled")
        }
    }

    if(location.href.indexOf('maintenancerecord') > 0){
        if(location.href.indexOf('id') > 0 && $("#checkContent").val()){
            $("#faultReports, #jihao").removeAttr('disabled', 'disabled')
        }

    }
})
