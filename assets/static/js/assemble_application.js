function onceRenderer(hot) {
    for (var y=0; y<hot.countRows(); y++) {
        var types = hot.getDataAtCell(y, 0);
        var data = requestAjax(getPnFromListCaUrl, { "ca": types });
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
                    getPnSelecteOption(hot, getPnFromListCaUrl, 4, changes, i);
                }
                if (changes[i][1] === 1) {
                    // 根据pn获取相关数据
                    setDataByPnChanged(hot, getPnUrl, 4, changes, i, { "3": 2, "6": 3});
                    hotRemoveExistSn(hot, changes[i][0], changes[i][1] + 1, getSnFormListPn,
                        {"act": "out"})
                }
                if (changes[i][1] === 2) {
                    var types = hot.getDataAtCell(changes[i][0], 0);
                    var pn = hot.getDataAtCell(changes[i][0], 1);
                    var sn = changes[i][3];
                    // 根据sn获取相关数据
                    setDataBySnChanged(hot, getFromListSn, [3, 4, 6], changes, i,
                        {'5': 4, '8': 12, '9': 9, '10': 10, '11': 6, '12': 7, '13': 8 },
                        { 'pn': pn });
                    // 对消耗品类型的航材如果已经制定序号，则数量必须为一
                    consumSnNumSet(hot, changes, i, 4, types, sn);
                }
                if (changes[i][1] === 4 && changes[i][2]) {
                    putOutStorageListQuantity(hot, changes, i);
                }
            }

        },

        beforeOnCellMouseDown: function (event, coords, TD) {
            var column = coords.col;
            var row = coords.row;
            if (column === 2) {
                hotRemoveExistSn(hot, row, column, getSnFormListPn, {"act": "out"});
            }
            if (column === 8) {
                clickGetSpecialTime(hot, 1, 2, 10, 8, row, column, 'effect');
            }
            if (column === 10) {
                clickGetSpecialTime(hot, 1, 2, 10, 8, row, column, 'nextcheck');
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