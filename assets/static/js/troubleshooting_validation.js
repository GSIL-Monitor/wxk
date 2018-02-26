var rules = {
    formulateDate : {
        required: true,
    },
    description: {
        required: true,
    },
    maintainStep: {
        required: true,
    },
    enforceDate: {
        required: true,
    },
    enforceStaff: {
        required: true,
    },
}

$(function () {
    FormValidation.init(rules);
});