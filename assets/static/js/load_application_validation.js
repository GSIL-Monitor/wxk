var rules = {
    number : {
        required: true,
    },
    applicationDate : {
        required: true,
    },
    date : {
        required: true,
    },
}

$(function () {
    FormValidation.init(rules);
});
