function customSettings(hot) {
    hot.updateSettings({
        afterChange: function (changes, source) {
            if (!changes) {
                return;
            }
            for (var i=0; i<changes.length; i++) {

                if (changes[i][1] === 0) {
                    getPnSelecteOption(hot, getPnFromCaUrl, 4, changes, i);
                }

                if (changes[i][1] === 1) {
                    setDataByPnChanged(hot, getPnUrl, 4, changes, i, {"3": 2, "5": 3})
                }

                if (changes[i][1] === 2 && changes[i][3]) {
                    var types = hot.getDataAtCell(changes[i][0], 0);
                    var pn = hot.getDataAtCell(changes[i][0], 1);
                    var sn = changes[i][3];
                    if (uniqueInputSn(hot, pn, 1, sn, 2, changes[i][0])) {
                        alert(sn + '已经输入了');
                        hot.setDataAtCell(changes[i][0], changes[i][1], null);
                    }
                    var data = requestAjax(getSnFormListPn, { "pn": pn, "act": "in"});
                    data = JSON.parse(data);
                    if ($.inArray(sn, data) > -1) {
                        alert(sn + '已经存在在库存列表中');
                        hot.setDataAtCell(changes[i][0], changes[i][1], null);
                    }
                    consumSnNumSet(hot, changes, i, 4, types, sn);
                }
            }
        },

        beforeRenderer: function (TD, row, col, prop, value, cellProperties) {
            if (col === 4) {
                var types = hot.getDataAtCell(row, 0);
                if (isInArray(types)) {
                    cellProperties.readOnly = true;
                }
                else {
                    var sn = hot.getDataAtCell(row, 2);
                    // 对消耗品类型的航材如果已经制定序号，不可更改
                    consumSnNumReadOnly(sn, cellProperties);
                }
            }
        },
    })
}

function onceRenderer(hot) {
}

function customNotNull(hot, row, col) {
    return true;
}