var rules = {
    trainPlanStartTime : {
        required: true,
    },
    trainPlanEndTime : {
        checkDate: true,
    },
    
}

function getStartDate(){
	return $("[name='trainPlanStartTime']").val();
}

$(function(){
    FormValidation.init(rules);
});