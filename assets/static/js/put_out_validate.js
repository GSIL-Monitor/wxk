var rules = {
    outDate : {
        required: true,
    },
    date : {
        required: true,
    },
    // remark : {
    //     required: true,
    // },
}

$(function () {
    FormValidation.init(rules);
});
