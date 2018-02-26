var rules = {
    number : {
        required: true,
    },
    applicationDate : {
        required: true,
    },
}

$(function () {
    FormValidation.init(rules);
});