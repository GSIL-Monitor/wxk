var rules = {
    number: {
        required: true,
    },
    date: {
        required: true,
    },
    assembleDate: {
        required: true,
    },
}

$(function () {
    FormValidation.init(rules);
});