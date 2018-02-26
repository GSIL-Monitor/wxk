var inLineTable = function () {

    var gHot;
    var gOpt;
    var fieldNull = true;
    var fieldVali = new Array();

    var handlTable = function (opt) {
        var saveButton = $("input.btn.btn-circle.blue");
        var newLineBtn = $('#table_new');
        var delLineBtn = $('#table_del');
        var columns, cHeaders;
        var processed = process(opt.table_columns);
        columns = processed[0];
        cHeaders = processed[1];
        var data = opt.table_datas;

        var container = $('#inline_table')[0];
        var hot = new Handsontable(container, {
            data: data,
            colHeaders: function (col) {
                return customHeader(cHeaders, col);
            },
            columns: columns,
            manualColumnResize: false,
            stretchH: 'all',
            className: 'table-scrollable htCenter',
            rowHeaders: true,
            renderAllRows: true,
            rowHeights: 30,
            minRows: 1,
            fillHandle: false,
            outsideClickDeselects: false,
            renderAllRows: true,
            height: 200,
            fixedColumnsLeft: 4,
            afterValidate: function (isValid, value, row, prop, source) {
                var item = row.toString() + prop.toString();
                if (isValid) {
                    if ($.inArray(item, fieldVali) > -1) {
                        arrayRemoveByValue(fieldVali, item);
                    }
                } else {
                    if ($.inArray(item, fieldVali) < 0) {
                        fieldVali.push(item);
                    }
                }
            },
            beforePaste: function (data, coords) {
                return false;
            }
        });

        gHot = hot;
        gOpt = opt;

        var justOnce = function (TD, row, col, prop, value, cellProperties) {
            onceRenderer(hot);
        }

        var nonnegative = function (value, callback) {
            if (value) {
                if (isNumber(value) && value > 0) {
                    callback(true);
                } else {
                    callback(false);
                }
            } else {
                callback(true);
            }
        };

        var hhmm = function (value, callback) {
            if (value) {
                var reg = /^([0-9][0-9]|[1-9][0-9][0-9]+)\:[0-5][0-9]$/;

                if (reg.test(value)) {
                    callback(true);
                } else {
                    callback(false);
                }
            } else {
                callback(true);
            }
        };

        Handsontable.hooks.once('beforeRenderer', justOnce, hot);
        Handsontable.validators.registerValidator('nonnegative', nonnegative);
        Handsontable.validators.registerValidator('hhmm', hhmm);
        customSettings(hot);

        newLineBtn.click(function (e) {
            hot.alter('insert_row');
        });

        delLineBtn.click(function (e) {
            var sel = hot.getSelected();
            if (sel[0] != sel[2]) {
                alert('指定唯一一行删除');
            } else {
                hot.alter('remove_row', sel[0]);
            }
        });

    };

    var extraVali = function () {
        var hot = gHot;
        if (location.href.indexOf('borrowinginreturnmodel') > 0) {
            var pns = getPn();
            if (pns === "noBorrow") {
                alert("请选择借入申请单号");
                return false
            }
            if (pns === "notCheck") {
                return true
            }
            var rows = hot.countRows();
            for (var i = 0; i < rows; i++) {
                var pn = hot.getDataAtCell(i, 1);
                if ($.inArray(pn, pns) < 0) {
                    alert(pn + "不在借入申请" + getBorrowAppNum() + "中!");
                    return false;
                }
            }
            return true;
        }
        else {
            return true;
        }
    }

    var formSubmit = function () {
        var hot = gHot;
        var opt = gOpt;
        var cols = hot.countCols();
        var rows = hot.countRows();
        fieldNull = true;
        for (var i = 0; i < rows; i++) {
            if (fieldNull != true) {
                break;
            }
            for (var y = 0; y < cols; y++) {
                var val = hot.getDataAtCell(i, y)
                if ((!val && parseInt(val) != 0) || val === null) {
                    if (opt.table_columns[y].need === true) {
                        fieldNull = false;
                        var strHeader = hot.getColHeader(y).split('<em class="need">*</em>')[0];
                        alert(strHeader + " 字段不能为空值！");
                        break;
                    } else if (opt.table_columns[y].checkNeed === true) {
                        // 对有库存效期，定期检查勾选非空的验证
                        if (location.href.indexOf('disassembleorder') > 0) {
                            var pn = hot.getDataAtCell(i, 2);
                        } else {
                            var pn = hot.getDataAtCell(i, 1);
                        }
                        var strHeader = hot.getColHeader(y);
                        var data = requestAjax(getPnUrl, {"pn": pn});
                        data = JSON.parse(data);
                        if (data) {
                            if (data[4] && strHeader === "库存有效期") {
                                fieldNull = false;
                                alert("必须填写"+ pn + "件号航材的" + strHeader);
                                break;
                            }
                            if (data[5] && strHeader === "下次检查日期") {
                                fieldNull = false;
                                alert("必须填写" + pn + "件号航材的" + strHeader);
                                break;
                            }
                        }
                    } else {
                        fieldNull = customNotNull(hot, i, y);
                        if (!fieldNull) {
                            fieldNull = false;
                            break;
                        }
                    }
                }
            }
        }
        if (extraVali() && fieldNull && fieldVali.length === 0) {
            var datas = hot.getData();
            datas = JSON.stringify(datas);
            $("input[name=table_datas]").val(datas);
            return true;
        }
        else if (fieldVali.length != 0) {
            alert('数据有误');
        }
        return false;
    }

    return {
        init: function (opt) {
            numbro.culture('zh-CN');
            handlTable(opt);
        },
        func: function () {
            return formSubmit();
        }
    };
}();

function requestAjax(urlFunc, args_dict) {
    var result = true;
    var url = "";
    var sign = "?";
    $.each(args_dict, function (i, val) {
        url = url + sign + i + "=" + val;
        sign = "&";
    });

    $.ajax({
        url: urlFunc() + url,
        type: "get",
        dataType: "json",
        async: false,
        success: function (data) {
            if (data.message === "Ok") {
                result = data.data;
            } else {
                result = false;
            }
        },
        error: function (data) {
            result = false;
        },
    });
    return result;
}

function isInArray(value) {
    var numObj = ["一般航材", "时控件", "时寿件"];
    var index = $.inArray(value, numObj);
    if (index >= 0) {
        return true;
    }
    return false;
}

function process(columns) {
    var cHeaders = new Array();
    for (var i = 0; i < columns.length; i++) {
        title = columns[i].title;
        delete columns[i].title;
        if (columns[i].need) {
            title = title + '<em class="need">*</em>';
        }
        cHeaders.push(title);
    }
    return [columns, cHeaders]
}

function customHeader(cHeaders, col) {
    return cHeaders[col]
}

function isNumber(value) {
    var patrn = /^(-)?\d+(\.\d+)?$/;
    if (patrn.exec(value) == null || value == "") {
        return false
    } else {
        return true
    }
}

function getQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) {
        return unescape(r[2]);
    } else {
        return null;
    }
}

function createOrEdit(params) {
    var path = window.location.pathname;
    if (path.search(params) > 0) {
        return true;
    }
    else {
        return false;
    }
}

function setData(hot, changes, i, data, values) {
    var valueKeys = Object.keys(values);
    var len = valueKeys.length;
    if (len > 0) {
        for (var key in values) {
            hot.setDataAtCell(changes[i][0], parseInt(key), data[values[key]])
        }
    }
}

function reSetTypes(hot, changes, i, numCol) {
    var types = hot.getDataAtCell(changes[i][0], 0);
    for (var y = 1; y < hot.countCols(); y++) {
        if (y === numCol) {
            hot.setDataAtCell(changes[i][0], numCol, 1);
        } else {
            hot.setDataAtCell(changes[i][0], y, null);
        }
    }
}

function getPnSelecteOption(hot, url, numCol, changes, i) {
    var extraData = arguments[5] ? arguments[5] : new Object();
    var types = hot.getDataAtCell(changes[i][0], 0);
    var args = { "ca": types };
    if (JSON.stringify(extraData) != "{}") {
        args = $.extend(args, extraData);
    }
    var data = requestAjax(url, args);
    data = JSON.parse(data);
    if (data) {
        hot.setCellMeta(changes[i][0], 1, 'selectOptions', data);
        for (var y = 1; y < hot.countCols(); y++) {
            if (y === numCol) {
                hot.setDataAtCell(changes[i][0], numCol, 1);
            } else {
                hot.setDataAtCell(changes[i][0], y, null);
            }
        }
    }
}

function setDataByPnChanged(hot, url, numCol, changes, i, values) {
    var extraData = arguments[6] ? arguments[6] : new Object();
    var types = hot.getDataAtCell(changes[i][0], 0);
    var pn = hot.getDataAtCell(changes[i][0], 1);
    var args = { 'pn': pn };
    if (JSON.stringify(extraData) != "{}") {
        args = $.extend(args, extraData);
    }
    var data = requestAjax(url, args);
    data = JSON.parse(data);
    if (data) {
        for (var y = 2; y < hot.countCols(); y++) {
            if (y != numCol) {
                hot.setDataAtCell(changes[i][0], y, null);
            }
        }
        setData(hot, changes, i, data, values);
    }
}

function setDataBySnChanged(hot, url, numCol, changes, i, values) {
    var extraData = arguments[6] ? arguments[6] : new Object();
    var types = hot.getDataAtCell(changes[i][0], 0);
    var pn = hot.getDataAtCell(changes[i][0], 1);
    var sn = hot.getDataAtCell(changes[i][0], 2);
    if (!sn) {
        sn = 'null';
    }
    var args = { "sn": sn }
    if (JSON.stringify(extraData) != "{}") {
        args = $.extend(args, extraData);
    }
    var data = requestAjax(url, args);
    data = JSON.parse(data);
    if (data) {
        for (var y = 3; y < hot.countCols(); y++) {
            if ($.inArray(y, numCol) < 0) {
                hot.setDataAtCell(changes[i][0], y, null);
            }
        }
        setData(hot, changes, i, data, values);
    }
}

function getSnSelecteOption(hot, url, numCol, changes, i) {
    var extraData = arguments[5] ? arguments[5] : new Object();
    var types = hot.getDataAtCell(changes[i][0], 0);
    var pn = hot.getDataAtCell(changes[i][0], 1);
    var args = { "pn": pn };
    if (JSON.stringify(extraData) != "{}") {
        args = $.extend(args, extraData);
    }
    var data = requestAjax(url, args);
    data = JSON.parse(data);
    if (data) {
        for (var y = 2; y < hot.countCols(); y++) {
            if (y != numCol) {
                hot.setDataAtCell(changes[i][0], y, null);
            }
        }
        hot.setCellMeta(changes[i][0], 2, 'selectOptions', data);
    }
}

function getPnInput(hot, types, typeCol, pnCol) {
    var res = new Array();
    for (var i = 0; i < hot.countRows(); i++) {
        var otherTypes = hot.getDataAtCell(i, typeCol);
        var otherPn = hot.getDataAtCell(i, pnCol);
        if ((otherTypes === types) && ($.inArray(otherPn, res) < 0)) {
            res.push(otherPn);
        }
    }
    return res;
}

function getSnInput(hot, snCol, sn, pnCol, pn) {
    var res = new Array();
    for (var i = 0; i < hot.countRows(); i++) {
        var otherSn = hot.getDataAtCell(i, snCol);
        var otherPn = hot.getDataAtCell(i, pnCol);
        if (otherSn && (otherPn === pn) && ($.inArray(otherSn, res) < 0)) {
            res.push(otherSn);
        }
    }
    return res;
}

function removeExistPn(hot, types, typeCol, pn, pnCol, data) {
    Array.prototype.minus = function (arr) {
        var result = new Array();
        var obj = {};
        for (var i = 0; i < arr.length; i++) {
            obj[arr[i]] = 1;
        }
        for (var j = 0; j < this.length; j++) {
            if (!obj[this[j]]) {
                obj[this[j]] = 1;
                result.push(this[j]);
            }
        }
        return result;
    };
    if (data) {
        var res = data.slice();
    } else {
        var res = [];
    }
    var exist = getPnInput(hot, types, typeCol, pnCol);
    res = res.minus(exist)
    if (pn) {
        res.push(pn);
    }
    return res;
}

function removeExistSn(hot, sn, snCol, data, pn, pnCol) {
    Array.prototype.minus = function (arr) {
        var result = new Array();
        var obj = {};
        for (var i = 0; i < arr.length; i++) {
            obj[arr[i]] = 1;
        }
        for (var j = 0; j < this.length; j++) {
            if (!obj[this[j]]) {
                obj[this[j]] = 1;
                result.push(this[j]);
            }
        }
        return result;
    };

    if (data) {
        var res = data.slice();
    } else {
        var res = [];
    }
    // 对空选项进行替换
    var nullIndex = $.inArray(null, res);
    if (nullIndex > -1) {
        res.splice(nullIndex, 1, "");
    }

    var exist = getSnInput(hot, snCol, sn, pnCol, pn);
    res = res.minus(exist)
    if (sn) {
        res.push(sn);
    }
    return res;
}

function arrayRemoveByValue(arr, val) {
    for (var i = 0; i < arr.length; i++) {
        if (arr[i] == val) {
            arr.splice(i, 1);
            break;
        }
    }
}

function hotRemoveExistPn(hot, row, column) {
    var types = hot.getDataAtCell(row, 0);
    if (types) {
        var pn = hot.getDataAtCell(row, column);
        var data = requestAjax(getPnFromCaUrl, { "ca": types });
        data = JSON.parse(data);
        data = removeExistPn(hot, types, 0, pn, 1, data);
        hot.setCellMeta(row, column, 'selectOptions', data);
    }
}

function hotRemoveExistSn(hot, row, column, url) {
    var extraData = arguments[4] ? arguments[4] : new Object();
    var types = hot.getDataAtCell(row, 0);
    var pn = hot.getDataAtCell(row, 1);
    var sn = hot.getDataAtCell(row, column);
    var args = { "pn": pn }
    if (JSON.stringify(extraData) != "{}") {
        args = $.extend(args, extraData);
    }
    var data = requestAjax(url, args);
    data = JSON.parse(data);
    data = removeExistSn(hot, sn, 2, data, pn, 1);
    hot.setCellMeta(row, 2, 'selectOptions', data);
}

function putOutStorageListQuantity(hot, changes, i) {
    var ca = hot.getDataAtCell(changes[i][0], 0);
    var pn = hot.getDataAtCell(changes[i][0], 1);
    // 添加对sn的获取
    var sn = hot.getDataAtCell(changes[i][0], 2);
    var data = requestAjax(getMaxQuantityFromList,
        { 'ca': ca, 'pn': pn, 'sn': sn })
    data = JSON.parse(data)
    if (data) {
        if (parseInt(changes[i][3]) > parseInt(data)) {
            alert('最大可使用库存数量为:' + data);
            hot.setDataAtCell(changes[i][0], changes[i][1], data);
        }
    }
}

// 对消耗品类型的航材如果已经制定序号，则数量必须为一
function consumSnNumSet(hot, changes, i, col, types, sn) {
    if (!isInArray(types) && sn) {
        hot.setDataAtCell(changes[i][0], col, 1);
    }
}

// 对消耗品类型的航材如果已经制定序号，不可更改
function consumSnNumReadOnly(sn, cellProperties) {
    if (sn) {
        cellProperties.readOnly = true;
    } else {
        cellProperties.readOnly = false;
    }
}

// 获取库存有效期和下次检查日期
function clickGetSpecialTime(hot, pnIndex, snIndex, ncIndex, edIndex, row, column, action) {
    var pn = hot.getDataAtCell(row, pnIndex);
    var sn = hot.getDataAtCell(row, snIndex);
    var nc = hot.getDataAtCell(row, ncIndex);
    var ed = hot.getDataAtCell(row, edIndex);
    var data = requestAjax(getDateFromList,
        { 'pn': pn, 'sn': sn, 'nc': nc, 'ed': ed, 'act': action });
    data = JSON.parse(data);
    if (JSON.stringify(data) != '[]') {
        hot.setCellMeta(row, column, 'selectOptions', data);
    }
}


function uniqueInputSn(hot, pn, pnCol, sn, snCol, curRow) {
    if (!sn) {
        return false;
    }
    for (var i = 0; i < hot.countRows(); i++) {
        if (i != curRow) {
            var otherPn = hot.getDataAtCell(i, pnCol);
            if (otherPn === pn) {
                otherSn = hot.getDataAtCell(i, snCol);
                if (otherSn === sn) {
                    return true;
                    break;
                }
            }
        }
    }
    return false;
}