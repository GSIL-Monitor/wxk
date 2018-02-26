var rules = {
    borrow: {
        required: true,
    },
    returnDate: {
        required: true,
    },
    number: {
        required: true,
    },
    lendCategory: {
        required: true,
    },
    returnDate: {
        required: true,
    }
}

$(function () {
    FormValidation.init(rules);
});
