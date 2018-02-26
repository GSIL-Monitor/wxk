var rules = {
    repairApplication : {
        required: true,
    },
    number : {
        required: true,
    },
}

$(function () {
    FormValidation.init(rules);
});
