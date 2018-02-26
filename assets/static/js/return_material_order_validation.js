var rules = {
    date : {
        required: true,
    },
    returnDate : {
        required: true,
    },
}

$(function () {
    FormValidation.init(rules);
});