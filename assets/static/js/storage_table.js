function customSettings(hot) {

    hot.updateSettings({
        afterChange: function (changes, source) {
            if (!changes) {
                return;
            }
            for (var i = 0; i < changes.length; i++) {
                if (changes[i][1] === 0) {
                    var data = getPnData();
                    var types = hot.getDataAtCell(changes[i][0], 0);
                    pnData = data[types];
                    hot.setCellMeta(changes[i][0], 1, 'selectOptions', pnData);
                    for (var y=1;y<hot.countCols();y++) {
                        if (y === 4 && isInArray(types)) {
                            hot.setDataAtCell(changes[i][0], y, 1);
                        } else {
                            hot.setDataAtCell(changes[i][0], y, null);
                        }
                    }
                }
                if (changes[i][1] === 1) {
                    setDataByPnChanged(hot, getPnUrl, 4, changes, i, {'3': 2, '6': 3})
                }
                if (changes[i][1] === 2) {
                    var types = hot.getDataAtCell(changes[i][0], 0);
                    var pn = hot.getDataAtCell(changes[i][0], 1);
                    var sn = hot.getDataAtCell(changes[i][0], 2);
                    if (pn && sn) {
                        if (uniqueSnInTable(hot, pn, sn, changes[i][0]) || uniqueSnInDB(hot, pn, sn)){
                            alert('该序号已经存在了');
                            hot.setDataAtCell(changes[i][0], 2, null);
                        }
                    } else {
                        if (sn) {
                            alert('请先填写pn号');
                            hot.setDataAtCell(changes[i][0], 2, null);
                        }
                    }
                    // 对消耗品类型的航材如果已经制定序号，则数量必须为一
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
                    sn = hot.getDataAtCell(row, 2);
                    // 对消耗品类型的航材如果已经制定序号，不可更改
                    consumSnNumReadOnly(sn, cellProperties);
                }
            }
        },
    })
}

function onceRenderer(hot) {
    var data = getPnData();
    for (var y=0;y<hot.countRows();y++) {
        var types = hot.getDataAtCell(y, 0);
        pn_data = data[types]
        hot.setCellMeta(y, 1, 'selectOptions', pn_data);
    }
}

function uniqueSnInTable(hot, pn, sn, row) {
    for (var i=0;i<hot.countRows();i++) {
        if (i != row) {
            var otherPn = hot.getDataAtCell(i, 1);
            if (otherPn === pn) {
                otherSn = hot.getDataAtCell(i, 2);
                if (otherSn === sn) {
                    return true;
                    break;
                }
            }
        }
    }
    return false;
}

function uniqueSnInDB(hot, pn, sn) {
    var data = requestAjax(getUniqueSerialnum, {'pn':pn, 'sn': sn});
    if (data != true) {
        return true;
    }
    return false;
}

function getPnData() {
    if (createOrEdit('/new/')) {
        var storage_type = getQueryString('model');
        var data = requestAjax(getPnFromTypes, {'storage_type': storage_type});
        return JSON.parse(data);
    } else {
        var id = getQueryString('id');
        var data = requestAjax(getPnFromId, {'id': id});
        return JSON.parse(data);
    }
}

function customNotNull(hot, row, col) {
    if (hot.getColHeader(col) === "序号") {
        var types = hot.getDataAtCell(row, 0);
        if (isInArray(types)) {
            alert(types +'序号不能为空');
            return false;
        }
    }
    return true;
}