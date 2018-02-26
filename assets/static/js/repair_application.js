function onceRenderer(hot) {
    for (var y=0;y<hot.countRows();y++) {
        var types = hot.getDataAtCell(y, 0);
        var pn = hot.getDataAtCell(y, 1);
        var data = requestAjax(getPnFromListCaUrl, {"ca": types});
        data = JSON.parse(data);
        hot.setCellMeta(y, 1, 'selectOptions', data);
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

function customSettings(hot) {

    hot.updateSettings({

        afterChange: function (changes, source) {
            if (!changes) {
                return;
            }
            for (var i = 0; i < changes.length; i++) {
                if (changes[i][1] === 0) {
                    var types = hot.getDataAtCell(changes[i][0], 0);
                    var data = requestAjax(getPnFromListCaUrl, {"ca": types});
                    data = JSON.parse(data);
                    hot.setCellMeta(changes[i][0], 1, 'selectOptions', data);
                    for (var y=1;y<hot.countCols();y++) {
                        if (isInArray(types) && y === 4) {
                            hot.setDataAtCell(changes[i][0], 4, 1);
                        } else {
                            hot.setDataAtCell(changes[i][0], y, null);
                        }
                    }
                    hot.setDataAtCell(changes[i][0], 10, 'Y5D(B)');
                }

                if (changes[i][1] === 1) {
                    // 根据pn获取相关数据
                    setDataByPnChanged(hot, getPnUrl, 4, changes, i, { "3": 2 });
                    hotRemoveExistSn(hot, changes[i][0], changes[i][1] + 1, getSnFormListPn,
                    {"act": "out"});
                    hot.setDataAtCell(changes[i][0], 10, 'Y5D(B)');
                }

                if (changes[i][1] === 2) {
                    var types = hot.getDataAtCell(changes[i][0], 0);
                    var pn = hot.getDataAtCell(changes[i][0], 1);
                    var sn = changes[i][3];
                    // 根据sn获取相关数据
                    setDataBySnChanged(hot, getFromListSn, [3, 4], changes, i,
                        { '3': 3, '5': 4, '6': 12, '7': 9, '8': 10, '15': 6, '16': 7, '17': 8 },
                        {'pn': pn});
                    // 对消耗品类型的航材如果已经制定序号，则数量必须为一
                    consumSnNumSet(hot, changes, i, 4, types, sn);
                    hot.setDataAtCell(changes[i][0], 10, 'Y5D(B)');
                }

                if (changes[i][1] === 4) {
                    putOutStorageListQuantity(hot, changes, i);
                }
            }
        },

        beforeOnCellMouseDown: function (event, coords, TD) {
            var column = coords.col;
            var row = coords.row;
            if (column === 2) {
                hotRemoveExistSn(hot, row, column, getSnFormListPn, { "act": "out" });
            }
            if (column === 6) {
                clickGetSpecialTime(hot, 1, 2, 8, 6, row, column, 'effect');
            }
            if (column === 8) {
                clickGetSpecialTime(hot, 1, 2, 8, 6, row, column, 'nextcheck');
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

// 动态获取维修厂商的信息
$(function () {
    $("#repairCompany").change(function () {
        var name = $(this).val();
        var data = requestAjax(getRepairSupplierDataFromName, { 'name': name });
        data = JSON.parse(data);
        $("#contactPerson").val(data[0]);
        $("#telephone").val(data[1]);
        $("#fax").val(data[2]);
        $("#mailbox").val(data[3]);
    });
});