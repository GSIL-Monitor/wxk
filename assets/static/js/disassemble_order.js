function customSettings(hot) {
    hot.updateSettings({
        afterChange: function (changes, source) {
            if (!changes) {
                return;
            }
            for (var i = 0; i < changes.length; i++) {

                if (changes[i][1] === 0) {
                    for (var y = 1; y < hot.countCols(); y++) {
                        hot.setDataAtCell(changes[i][0], y, null);
                    }
                }

                if (changes[i][1] === 1) {
                    var types = changes[i][3];
                    hot.setDataAtCell(changes[i][0], 2, '');
                    for (var y = 3;y < hot.countCols(); y++) {
                        if (isInArray(types) && (y == 5)) {
                            hot.setDataAtCell(changes[i][0], y, 1);
                        } else {
                            hot.setDataAtCell(changes[i][0], y, null);
                        }
                    }
                    if ($.inArray(types, ["时控件", "时寿件"]) >= 0) {
                        hot.setCellMeta(changes[i][0], 3, 'editor', 'select');
                    } else {
                        var meta = hot.getCellMeta(changes[i][0], 3);
                        if (meta.editor === 'select') {
                            hot.setCellMeta(changes[i][0], 3, 'editor', undefined);
                        }
                    }
                }

                if (changes[i][1] === 2) {
                    var pn = hot.getDataAtCell(changes[i][0], 2);
                    var data = requestAjax(getPnUrl, {"pn": pn});
                    for (var y = 3; y < hot.countCols(); y++) {
                        if (y != 5) {
                            hot.setDataAtCell(changes[i][0], y, null);
                        }
                    }
                    data = JSON.parse(data);
                    if (data) {
                        setData(hot, changes, i, data, {'4': 2, '6': 3});
                    }
                }

                if (changes[i][1] === 3 && changes[i][3]) {
                    var planeNum = hot.getDataAtCell(changes[i][0], 0);
                    var ca = hot.getDataAtCell(changes[i][0], 1);
                    var pn = hot.getDataAtCell(changes[i][0], 2);
                    var sn = hot.getDataAtCell(changes[i][0], 3);
                    for (var y = 7; y < hot.countCols(); y++) {
                        hot.setDataAtCell(changes[i][0], y, null);
                    }
                    if ($.inArray(ca, ["时控件", "时寿件"]) >= 0) {
                        var data = requestAjax(getPlaneInfosFromPn,
                            { 'planeNum': planeNum, 'ca': ca, 'pn': pn });
                        data = JSON.parse(data);
                        data = getInfoFromSn(data, sn);
                        if (data != false) {
                            setData(hot, changes, i, data, {'10': 5, '11': 3, '12': 4, '13': 2,'9': 1});
                        }
                    } else {
                        if (uniqueSnInTable(hot, pn, sn, changes[i][0]) || uniqueSnInDB(hot, pn, sn)) {
                            alert('该序号已经存在了');
                            hot.setDataAtCell(changes[i][0], 3, null);
                        }
                    }
                    consumSnNumSet(hot, changes, i, 5, ca, sn);
                }

            }
        },

        beforeOnCellMouseDown: function (event, coords, TD) {
            var column = coords.col;
            var row = coords.row;
            if (column === 0) {
                var data = requestAjax(get_bounded_aircraft, {"bounded": null});
                data = JSON.parse(data);
                hot.setCellMeta(row, column, 'selectOptions', data);
            }
            if (column === 2) {
                var ca = hot.getDataAtCell(row, 1);
                if (ca) {
                    if ($.inArray(ca, ["时控件", "时寿件"]) >= 0) {
                        var data = requestAjax(getPnFromBoundedCategory, {'ca': ca})
                    } else {
                        var data = requestAjax(getPnFromCaUrl, {'ca': ca})
                    }
                    data = JSON.parse(data);
                    if (data.length != 0) {
                        hot.setCellMeta(row, column, 'readOnly', false);
                        hot.setCellMeta(row, column, 'source', data);
                    } else {
                        hot.setCellMeta(row, column, 'readOnly', true);
                    }
                }
            }
            if (column === 3) {
                var planeNum = hot.getDataAtCell(row, 0);
                var ca = hot.getDataAtCell(row, 1);
                var pn = hot.getDataAtCell(row, 2);
                var sn = hot.getDataAtCell(row, column);
                if ($.inArray(ca, ["时控件", "时寿件"]) >= 0) {
                    var data = requestAjax(getPlaneInfosFromPn,
                        { 'planeNum': planeNum, 'ca': ca, 'pn': pn });
                    data = JSON.parse(data);
                    data = getSnOption(data);
                    if (data) {
                        data = removeExistSn(hot, sn, column, data, pn, 2);
                    } else {
                        data = [''];
                    }
                    hot.setCellMeta(row, column, 'selectOptions', data);
                }
            }
        },

        beforeRenderer: function (TD, row, col, prop, value, cellProperties) {
            if (col === 5) {
                var types = hot.getDataAtCell(row, 1);
                var sn = hot.getDataAtCell(row, 3);
                if (types) {
                    if (isInArray(types)) {
                        cellProperties.readOnly = true;
                    }
                    else {
                        cellProperties.readOnly = false;
                        consumSnNumReadOnly(sn, cellProperties);
                    }
                } else {
                    cellProperties.readOnly = true;
                }
            }
        },
    })
}

function formatDate(time)   {
  if(time > 0){
    time = time * 1000
    var date= new Date(time);
    var year=date.getYear() + 1900;
    var month=date.getMonth() + 1;
    var date=date.getDate();
    if (month < 10) {
        month = "0" + month;
    }
    if (date < 10) {
        date = "0" + date;
    }
    return year+"-"+month+"-"+date;
  }else{
    return 'Empty'
  }
}

function onceRenderer(hot) {
}

function customNotNull(hot, row, col) {
    return true;
}

function getSnOption(data) {
    var res = new Array();
    for (var i = 0; i < data.length; i++) {
        res.push(data[i][0]);
    }
    return res
}

function getInfoFromSn(data, sn) {
    if (sn) {
        for (var i = 0; i < data.length; i++) {
            if (data[i][0] === sn.toString()) {
                var res = data[i];
                res[1] = formatDate(res[1]);
                return res;
            }
        }
    }
    return false;
}

function uniqueSnInTable(hot, pn, sn, row) {
    for (var i = 0; i < hot.countRows(); i++) {
        if (i != row) {
            var otherPn = hot.getDataAtCell(i, 2);
            if (otherPn === pn) {
                otherSn = hot.getDataAtCell(i, 3);
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
    var data = requestAjax(getUniqueSerialnum, { 'pn': pn, 'sn': sn });
    if (data != true) {
        return true;
    }
    return false;
}