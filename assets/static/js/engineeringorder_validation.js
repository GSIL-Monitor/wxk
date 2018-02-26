var rules = {
    insTitle : {
        required: true,
    },
    'repeatePeriod-value': {
        required: true,
        checkPlus: true,
    },
}

$(function(){
    FormValidation.init(rules);
});