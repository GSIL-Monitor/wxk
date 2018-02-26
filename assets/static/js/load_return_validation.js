var rules = {
    loanApplication : {
        required: true,
    },
    number : {
        required: true,
    },
}

$(function () {
    FormValidation.init(rules);
});