var baseRules = {
    environmentCategory: {
        required: true,
    },
    ataCode: {
        required: false,
        checkPlus: true
    },
    description: {
        required: true,
        maxlength: 100
    },
    interval: {
        required: true,
        minlength: 1,
    },
    startTracking: {
        typeSame: true,
    },
    adapt: {
        maxlength: 250,
    },
    name: {
        required: true,
        maxlength:10,
    },
    'startTracking-date-value': { 
        required: true, 
        number: true,
        checkPlus: true,
    },
    'startTracking-date-type': { 
        required: true, 
        number: true,
        checkPlus: true,
    },
    'startTracking-time-value': { 
        required: true, 
        number: true,
        checkPlus: true,
    },
    'startTracking-count-value': { 
        required: true, 
        number: true,
        checkPlus: true,
    },
    'interval-hours-value': {
        required: true,
        number: true,
        greaterThan0: true,
    },
    'interval-hours-min': {
        number: true,
        checkPlus: true,
        comStandard: true,
    },
    'interval-hours-max': {
        number: true,
        checkPlus: true,
        comStandard: true,        
    },
    'interval-times-value': {
        required: true,
        number: true,
        greaterThan0: true,
    },
    'interval-times-min': {
        number: true,
        checkPlus: true,
        comStandard: true,  
    },
    'interval-times-max': {
        number: true,
        checkPlus: true,
        comStandard: true,  
    },
    'interval-date-type': {
        typeCheck: true,
    },
    'interval-date-value': {
        required: true,
        number: true,
        greaterThan0: true,
    },
    'interval-date-min': {
        number: true,
        checkPlus: true,
        comDateStandard: true,
    },
    'interval-date-max': {
        number: true,
        checkPlus: true,
        comDateStandard: true,
    },
    'interval-turbo-value': {
        required: true,
        number: true,
        greaterThan0: true,
    },
    'interval-turbo-min': {
        number: true,
        checkPlus: true,
        comStandard: true,  
    },
    'interval-turbo-max': {
        number: true,
        checkPlus: true,
        comStandard: true,  
    },
    'interval-gasifier-value': {
        required: true,
        number: true,
        greaterThan0: true,
    },
    'interval-gasifier-min': {
        number: true,
        checkPlus: true,
        comStandard: true,  
    },
    'interval-gasifier-max': {
        number:true,
        checkPlus: true,
        comStandard: true,  
    },
    'interval-torque-value': {
        required: true,
        number: true,
        greaterThan0: true,
    },
    'interval-torque-min': {
        number: true,
        checkPlus: true,
        comStandard: true,  
    },
    'interval-torque-max': {
        number: true,
        checkPlus: true,
        comStandard: true,  
    },
    'interval-engine-value': {
        required: true,
        number: true,
        greaterThan0: true,
    },
    'interval-engine-min': {
        number:true,
        checkPlus: true,
        comStandard: true,  
    },
    'interval-engine-max': {
        number:true,
        checkPlus: true,
        comStandard: true, 
    },
    relateDoc: {
        required: true,
    },
    remark: {
        required: false,
        maxlength: 100
    },
    reference: {
        required:false
    },
    unitNo:{
        unitCheck: true
    },
    pieceNo: {
        required: true,
        maxlength: 25,
        checkPieceNo : true,
    },
    pn: {
        required: true,
        maxlength: 25,
        checkPN: true,
    },
}

function extendCopy(p) {
　　　　var c = {};
　　　　for (var i in p) { 
　　　　　　c[i] = p[i];
　　　　}
　　　　c.uber = p;
　　　　return c;
　}

var createId= {
    required: true,
    maxlength: 20,
    checkID: true,
}

var createBaseRules = extendCopy(baseRules);
createBaseRules.id = createId;
var createRules = createBaseRules;

var editId = {
    required: true,
    unchangedID: true,
}

var editBaseRules = extendCopy(baseRules);
editBaseRules.id = editId;
var editRules = editBaseRules;
