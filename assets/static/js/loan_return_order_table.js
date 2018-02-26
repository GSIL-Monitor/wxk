function onceRenderer(hot) {
    for (var y=0;y<hot.countRows();y++) {
        var types = hot.getDataAtCell(y, 0);
        var pn = hot.getDataAtCell(y, 1);
        var num = getLoanAppNum();
        var data = requestAjax(getPnFromLoanCa, {"ca": types, "num": num});
        data = JSON.parse(data);
        hot.setCellMeta(y, 1, 'selectOptions', data);
    }
}

function customNotNull(hot, row, col) {
    return true;
}

function customSettings(hot) {
    hot.updateSettings({
        afterChange: function (changes, source) {
            if (!changes) {
                return;
            }
            for (var i = 0; i < changes.length; i++) {
                if (changes[i][1] === 0) {
                    var num = getLoanAppNum();
                    getPnSelecteOption(hot, getPnFromLoanCa, 5, changes, i, {"num": num})
                }

                if (changes[i][1] === 1) {
                    var num = getLoanAppNum();
                    setDataByPnChanged(hot, getFromLoanPn, 5, changes, i,
                        { "3": 3, "4": 4, "5": 5, "6": 9, "7": 6, "8": 7, "9": 8},
                        { "num": num })
                }
                if (changes[i][1] === 2) {
                    var pn = hot.getDataAtCell(changes[i][0], 1);
                    var sn = changes[i][3];
                    if (uniqueInputSn(hot, pn, 1, sn, 2, changes[i][0])) {
                        alert(sn + '已经输入了');
                        hot.setDataAtCell(changes[i][0], changes[i][1], null);
                    }
                }
            }
        },

        beforeRenderer: function (TD, row, col, prop, value, cellProperties) {
            if (col === 2 ) {
                var types = hot.getDataAtCell(row, 0);
                if (isInArray(types)) {
                    cellProperties.readOnly = false;
                }
                else {
                    cellProperties.readOnly = true;
                }
            }
            if (col === 5) {
                var types = hot.getDataAtCell(row, 0);
                if (isInArray(types)) {
                    cellProperties.readOnly = true;
                }
                else {
                    cellProperties.readOnly = false;
                }
            }
        },
    })
}

function getLoanAppNum() {
    return $("#loanApplication option:selected").text();
}
