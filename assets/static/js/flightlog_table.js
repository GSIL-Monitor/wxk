var flightlogTable = function () {

    var edited = false;

    var handleTable = function (opt) {
        var requiresIndex = getRequireIndex(opt.headers);
        var headers = process(opt.headers);
        var saveBtn = $('#flightlog_save');
        var newLineBtn = $('#flightlog_table_new');
        var commitBtn = $('#flightlog_commit');

        commitBtn.hide();

        var data = opt.datas.slice();
        for (var idx = 0; idx < data.length; idx++) {
            data[idx] = jQuery.extend({}, data[idx]);
        }

        var colWidth = [];
        for (idx = 0; idx < headers.length; idx++) {
            colWidth.push(100);
        }

        var container = document.getElementById('flightlog_table');

        var hot = new Handsontable(container, {
            data: data,
            colHeaders: headers,
            colWidths: colWidth,
            manualColumnResize: true,
            columns: opt.columns,
            stretchH: 'all',
            className: 'table-scrollable htCenter',
            rowHeaders: true,
            fillHandle: {
                autoInsertRow: false,
                direction: 'vertical',
            },
            dataSchema: {
                flightDate: opt.flightDay,
            },
            afterInit: function () {
                if (data && data.length != 0) {
                    if (data[0].status != '已完成') {
                        commitBtn.show();
                    }
                }
                var calc = opt.calcIndex;
                var result = sumTotalEngineData(this.countRows(), this.getDataAtCell,
                    calc.typeIndex, calc.aircraftIdIndex, calc.engineTimeIndex);
                renderSumEngineTime(result);
            },
            afterBeginEditing: function (row, col) {
                if (opt.timeColumns.indexOf(col) != -1) {
                    if (!this.getDataAtCell(row, col)) {
                        this.setDataAtCell(row, col, moment().format('HH:mm'));
                    }
                }
            },
            beforeRenderer: function (TD, row, col, prop, value, cellProperties) {
                TD.style.color = "black";
                if (row % 2 != 0) {
                    TD.style.background = '#f3f3f3';
                }
            }
        });

        var dirty = function () {
            // source_data是一个object的array
            // cur_data是个2D的array
            // columns_cfg是按顺序描述的格式，用于从cur_data中提取输入，然后与对应的source_data对比
            var cur_data = hot.getData();
            var source_data = opt.datas;
            var columns_cfg = opt.columns;

            if (cur_data == null) {
                return source_data == null;
            }

            if (source_data == null) {
                return true;
            }

            if (cur_data.length != source_data.length) {
                return true;
            }

            for (var outer = 0; outer < cur_data.length; outer++) {
                var cur = cur_data[outer];
                var exp = source_data[outer];
                for (var idx = 0; idx < columns_cfg.length; idx++) {
                    var name = columns_cfg[idx].data;
                    if (cur[idx] != exp[name]) {
                        return true;
                    }
                }
            }

            return false;
        };

        var updateBtnWhenDirty = function () {
            if (dirty()) {
                saveBtn.removeClass('disabled');
                commitBtn.addClass('disabled');
                return;
            }
            saveBtn.addClass('disabled');
            commitBtn.removeClass('disabled');
        };

        newLineBtn.click(function (e) {
            e.preventDefault();
            hot.alter('insert_row');
            var n = hot.countRows();
            hot.selectCell(n - 1, 0, n - 1, 0);
        });

        // 解决高度的问题
        var resizeFunc = function () {
            hot.updateSettings({
                height: $(window).height() - $("#flightlog_table").offset().top - 150,
            });
        };

        resizeFunc();
        $(window).resize(resizeFunc);

        hot.updateSettings({
            contextMenu: opt.contextMenu,
            afterChange: function (changes) {

                var calc = opt.calcIndex;
                var flyProp = [calc.startProp, calc.endProp];
                var allEngineTimeProp = [calc.typeProp, calc.aircraftIdProp, calc.engineTimeProp];

                for (var idx = 0; idx < changes.length; idx++) {

                    var row = changes[idx][0];
                    var prop = changes[idx][1];

                    if (flyProp.indexOf(prop) != -1 && changes[idx][3] && changes[idx][3] != changes[idx][4]) {

                        var start = this.getDataAtCell(row, calc.startIndex);
                        var end = this.getDataAtCell(row, calc.endIndex);
                        var fly = this.getDataAtCell(row, calc.flightTimeIndex);
                        var engine = this.getDataAtCell(row, calc.engineTimeIndex);

                        if (validateTime(start) && validateTime(end)) {
                            var startTime = moment(start, 'HH:mm');
                            var endTime = moment(end, 'HH:mm');
                            if (endTime > startTime) {
                                var flyTime = moment.duration(endTime - startTime).format('HH:mm', {
                                    trim: false
                                })
                                this.setDataAtCell(row, calc.flightTimeIndex, flyTime);
                                this.setDataAtCell(row, calc.engineTimeIndex, flyTime);
                            } else {
                                if (fly || engine) {
                                    this.setDataAtCell(row, calc.flightTimeIndex, null);
                                    this.setDataAtCell(row, calc.engineTimeIndex, null);
                                }
                            }
                        } else {
                            if (fly || engine) {
                                this.setDataAtCell(row, calc.flightTimeIndex, null);
                                this.setDataAtCell(row, calc.engineTimeIndex, null);
                            }
                        }
                    }

                    if (allEngineTimeProp.indexOf(prop) != -1 && changes[idx][3]) {
                        var result = sumTotalEngineData(this.countRows(), this.getDataAtCell,
                            calc.typeIndex, calc.aircraftIdIndex, calc.engineTimeIndex);
                        renderSumEngineTime(result);
                    }
                }

                updateBtnWhenDirty();
            },
            afterCreateRow: updateBtnWhenDirty,
            afterRemoveRow: function (index, amount) {
                updateBtnWhenDirty();
                var calc = opt.calcIndex;
                var result = sumTotalEngineData(this.countRows(), this.getDataAtCell,
                    calc.typeIndex, calc.aircraftIdIndex, calc.engineTimeIndex);
                renderSumEngineTime(result);
            },
        });

        saveBtn.click(function (e) {
            e.preventDefault();
            if ($(this).hasClass('disabled')) {
                return;
            }

            var data = hot.getData();
            if (data.length == 0) {
                // TODO: 是否未编辑的时候也给用户提示？

                toastr.error('没有任何需要暂存的内容。');
                return;
            }
            //加药量，作业亩数 允许为空
            $.each(data, function (ids, obj) {
                if (!obj[18]) obj[18] = ''

                if (!obj[20]) obj[20] = ''
            })

            $.ajax({
                    type: 'POST',
                    url: opt.saveUrl + '?timestamp=' + opt.flightDay,
                    contentType: 'application/json',
                    data: JSON.stringify({
                        count: data.length,
                        datas: data,
                    }),
                    dataType: 'json',
                })
                .done(function (data) {
                    if (data.code == 400) {
                        toastr.error(data.message);
                        return;
                    }

                    // 状态信息更新
                    $('#status_info').attr('style', 'display: block;');
                    $('#creator').attr('style', 'display: block;');
                    $('#creator h3').html(data.username);
                    $('#createTime').attr('style', 'display: block;');
                    $('#createTime h3').html(data.timestamp);

                    saveBtn.addClass("disabled");
                    commitBtn.removeClass("disabled");
                    commitBtn.show();
                    toastr.success('飞行日志暂存成功。');
                })
                .fail(function (err) {
                    toastr.error('发生错误，错误内容: ' + err);
                });
        });

        commitBtn.click(function (e) {

            var checked = requiresCheck(hot, requiresIndex, toastr);
            if (!checked) {
                toastr.error('请填写必填项！');
                return;
            }
            e.preventDefault();
            if ($(this).hasClass('disabled')) {
                return;
            }
            $(this).addClass("disabled");
            $.ajax({
                    type: 'POST',
                    url: opt.commitUrl + '?timestamp=' + opt.flightDay,
                })
                .done(function (data) {
                    if (data.code == 400) {
                        toastr.error(data.message);
                        commitBtn.addClass("disabled");

                        return;
                    }

                    $(this).addClass("disabled");
                    commitBtn.hide();
                    saveBtn.hide();
                    newLineBtn.hide();

                    $('#commiter').attr('style', 'display: block;');
                    $('#commiter h3').html(data.username);
                    $('#commitTime').attr('style', 'display: block;');
                    $('#commitTime h3').html(data.timestamp);

                    var columns = opt.columns.slice();
                    for (var idx = 0; idx < columns.length; idx++) {
                        columns[idx].readOnly = true;
                    }

                    // 更新表格状态
                    hot.updateSettings({
                        columns: columns,
                    });

                    toastr.success('飞行日志提交成功，飞行器状态相应更新。');
                })
                .fail(function (err) {
                    toastr.error('发生错误，错误内容: ' + err);
                    commitBtn.addClass("disabled");
                });
        });
    };

    return {
        init: function (options) {
            numbro.culture('zh-CN');
            handleTable(options);
        }
    };
}();

var requires = ['滑出时间', '起飞时间', '降落时间', '停止时间', '任务类型', '起落次数'];

function process(columns) {

    for (var i = 0; i < columns.length; i++) {
        if ($.inArray(columns[i], requires) > -1) {
            columns[i] = '<em class="need">* </em>' + columns[i];
        }
    }
    return columns
}

function getRequireIndex(columns) {
    var indexs = new Array();
    for (var i = 0; i < columns.length; i++) {
        if ($.inArray(columns[i], requires) > -1) {
            indexs.push(i);
        }
    }
    return indexs;
}


function requiresCheck(hot, requiresIndex) {
    var check = true;
    for (var i = 0; i < hot.countRows(); i++) {
        for (var y = 0; y < requiresIndex.length; y++) {
            var value = hot.getDataAtCell(i, requiresIndex[y]);
            if (!value) {
                check = false;
                break;
            }
        }
    }
    return check;
}


function validateTime(time) {
    var timeReg = /^([01][0-9]|2[0-3])(\:[0-5][0-9]){2}$/;
    if (!time) {
        return false;
    }
    if (!timeReg.test(time)) {
        return false;
    }
    return true;
}

function FlyData(flyType, flyArn, engineTime) {

    var flyType = flyType;
    var flyArn = flyArn;
    var engineTime = engineTime;

    var validate = function () {
        var timeReg = /^([01][0-9]|2[0-3])\:[0-5][0-9]$/;
        if (!(flyType && flyArn && engineTime)) {
            return false;
        }
        if (!timeReg.test(engineTime)) {
            return false;
        }
        return true;
    };

    var getArn = function () {
        return flyArn;
    };

    var getFlyType = function () {
        return flyType;
    }
    var getEngineTime = function () {
        return engineTime;
    }

    return {
        "getArn": getArn,
        "getFlyType": getFlyType,
        "getEngineTime": getEngineTime,
        "validate": validate,
    }
}

function PlaneData(flyData) {

    var flyArn = flyData.getArn();
    var totallTime = new Array();
    var normalMark = false;
    var specialMark = false;

    var getID = function () {
        return flyArn;
    }

    var arnTest = function (arn) {
        if (arn === flyArn) {
            return true;
        } else {
            return false;
        }
    };

    var addTime = function (flyData) {
        if (flyData.getFlyType() === "正常任务") {
            normalMark = true;
        } else {
            specialMark = true;
        }
        totallTime.push(flyData.getEngineTime());
    };

    var sumTime = function () {
        var offset;
        var initTime = moment("00:00", "HH:mm");
        var result = moment("00:00", "HH:mm");
        if (specialMark) {
            offset = "00:06";
        } else if (normalMark) {
            offset = "00:02";
        } else {
            offset = "00:00";
            toastr.error('发生错误: 任务类型有误！');
        }
        totallTime.forEach(function (value, index, arr) {
            if (index === 0) {
                result.add(moment.duration(offset, "HH:mm"))
            }
            result.add(moment.duration(value, "HH:mm"));
        });
        result = moment.duration(result - initTime).format('HH:mm', {
            trim: false
        });
        return result;
    };

    return {
        "getID": getID,
        "arnTest": arnTest,
        "addTime": addTime,
        "sumTime": sumTime,
    }
}


function sumTotalEngineData(rows, getCellFunc, typeIndex, aircraftIdIndex, engineTimeIndex) {

    var sumFlyData = new Array();

    for (var i = 0; i < rows; i++) {

        var flyType = getCellFunc(i, typeIndex);
        var aircraftId = getCellFunc(i, aircraftIdIndex);
        var engine = getCellFunc(i, engineTimeIndex);
        var flyData = new FlyData(flyType, aircraftId, engine);
        var hasPlane = -1;

        if (flyData.validate()) {
            for (var y = 0; y < sumFlyData.length; y++) {
                if (sumFlyData[y].arnTest(aircraftId)) {
                    hasPlane = y;
                    break;
                }
            }
            if (hasPlane === -1) {
                var planeData = new PlaneData(flyData);
                planeData.addTime(flyData);
                sumFlyData.push(planeData);
            } else {
                sumFlyData[hasPlane].addTime(flyData);
            }
        }
    }
    return sumFlyData;
}

function renderSumEngineTime(data) {

    function render(body) {
        $render = $('<div class="row"></div>');
        $row1 = $('<div class="col-md-6"></div>');
        $row2 = $row1.clone();
        $table = $('<table class="table"></table>');
        $head = '<thead><tr><th>飞行器编号</th><th>发动机时间/日</th ></tr></thead>';
        $body = $('<tbody></tbody>');
        $body.append(body);
        $table.append($head);
        $table.append($body);
        $row1.append($table);
        $render.append($row1);
        $render.append($row2);
        return $render;
    }

    function body(arn, time) {
        var trBody = ["<tr>", "<td>", arn, "</td>", "<td>", time, "</td>", "</tr>"];
        return trBody.join("");
    }

    if (data.length > 0) {
        var bodyRender = "";
        for (var i = 0; i < data.length; i++) {
            bodyRender += body(data[i].getID(), data[i].sumTime());
        }
        $("#totall_engine").empty();
        if ($("#status_info").css("display") === "none") {
            $("#status_info").css("display", "block");
        }
        $("#totall_engine").append(render(bodyRender));
    } else {
        if ($("#creator h3").html() === "None") {
            $("#status_info").css("display", "none");
        }
        $("#totall_engine").empty();
    }
}