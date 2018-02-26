var rules = {
    number: {
        required: true,
    },
    scrapCategory: {
        required: true,
    },
}

$(function () {
    FormValidation.init(rules);
});