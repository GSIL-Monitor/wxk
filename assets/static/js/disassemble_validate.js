var rules = {
    number: {
        required: true,
    },
    date: {
        required: true,
    },
    disassembleDate: {
        required: true,
    },
}

$(function () {
    FormValidation.init(rules);
});