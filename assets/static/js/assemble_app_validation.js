var rules = {
    number: {
        required: true,
    },
    date: {
        required: true,
    },
    applyDate: {
        required: true,
    },
}

$(function () {
    FormValidation.init(rules);
});