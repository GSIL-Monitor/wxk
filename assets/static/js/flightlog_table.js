var flightlogTable = function() {
  var edited = false;
  var handleTable = function(opt) {

    var headers = process(opt.headers);
    var saveBtn = $('#flightlog_save');
    var newLineBtn = $('#flightlog_table_new');
    var commitBtn = $('#flightlog_commit');
    commitBtn.hide();

    var data =  opt.datas.slice();
    for (var idx=0; idx < data.length; idx++) {
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
//       columns: [
//         {
//           // type: 'date',
//           // dateFormat: 'YYYY-MM-DD',
//           data: 'flightDate',
//           readOnly: true,
//           default: opt.flightDay,
//           // datePickerConfig: {
// //             firstDay: 1,
// //             i18n: {
// //               previousMonth : '上个月',
// //               nextMonth     : '下个月',
// //               months        : ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月 ','12月'],
// //               weekdays      : ['星期日','星期一','星期二','星期三','星期四','星期五','星期六'],
// //               weekdaysShort : ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
// // }
// //           },
//         },
//       ],
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
      afterInit: function() {
        if (data && data.length != 0) {
          if (data[0].status != '已完成') {
            commitBtn.show();
          }
        }
      },
      afterBeginEditing: function(row, col) {
        // 如果时间对应的数据不为空
        if (opt.timeColumns.indexOf(col) != -1) {
          if (!this.getDataAtCell(row, col)) {
            this.setDataAtCell(row, col, moment().format('HH:mm'));
          }
        }
      },
    });

    var dirty = function() {
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

    var updateBtnWhenDirty = function() {
      if (dirty()) {
        saveBtn.removeClass('disabled');
        commitBtn.addClass('disabled');
        return;
      }
      saveBtn.addClass('disabled');
      commitBtn.removeClass('disabled');
    };

    newLineBtn.click(function(e) {
      e.preventDefault();

      hot.alter('insert_row', 0);
    });

    // 解决高度的问题
    var resizeFunc = function() {
      hot.updateSettings({
        height: $(window).height() - $("#flightlog_table").offset().top - 150,
      });
    };

    resizeFunc();
    $(window).resize(resizeFunc);

    // TODO: 根据权限决定是否可以新增或删除，或整个界面只读
    hot.updateSettings({
      contextMenu: opt.contextMenu,
      afterChange: function(changes) {
        // 特殊的cell发生变化时，对应的飞行小时和发动机时间要变化
        var indexes = [opt.calcIndex.typeProp, opt.calcIndex.startProp, opt.calcIndex.endProp];
        for (var idx = 0; idx < changes.length; idx++) {
          // 如果变化的内容是与计算时间相关的内容
          var row = changes[idx][0];
          // 第二个元素为prop，通常为数据的字段名
          if (indexes.indexOf(changes[idx][1]) != -1) {
            // 先推算飞行小时的自动值
            var cellData = this.getDataAtCell(row, opt.calcIndex.startIndex);
            if (cellData == null) return;
            var startTime = moment(cellData, 'HH:mm');

            cellData = this.getDataAtCell(row, opt.calcIndex.endIndex);
            if (cellData == null) return;
            var endTime = moment(cellData, 'HH:mm');

            if (endTime < startTime) return;

            var diff = (endTime-startTime);
            this.setDataAtCell(row, opt.calcIndex.flightTimeIndex, moment.duration(diff).format('HH:mm', {trim: false}));

            // 再推算可能的发动机时间的自动值
            cellData = this.getDataAtCell(row, opt.calcIndex.typeIndex);
            if (cellData == null) return;
            var offset = cellData == '正常任务' ? 2 : 6;
            diff += offset * 60000;
            this.setDataAtCell(row, opt.calcIndex.engineTimeIndex, moment.duration(diff).format('HH:mm', {trim: false}));
          }
        }

        updateBtnWhenDirty();
      },
      afterRemoveRow: updateBtnWhenDirty,
      afterCreateRow: updateBtnWhenDirty,
    });

    saveBtn.click(function(e) {
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
      $.each(data, function(ids, obj){
        if(!obj[18])obj[18] = ''         
        
        if(!obj[20])obj[20] = ''
      })

      $.ajax({
        type: 'POST',
        url: opt.saveUrl+'?timestamp='+opt.flightDay,
        contentType: 'application/json',
        data: JSON.stringify({
          count: data.length,
          datas: data,
        }),
        dataType: 'json',
      })
        .done(function(data) {
          console.log(data)
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
        .fail(function(err) {
          toastr.error('发生错误，错误内容: ' + err);
        });
    });

    commitBtn.click(function(e) {

      e.preventDefault();
      if ($(this).hasClass('disabled')) {
        return;
      }
      $(this).addClass("disabled");
      $.ajax({
        type: 'POST',
        url: opt.commitUrl+'?timestamp='+opt.flightDay,
      })
        .done(function(data) {
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
        .fail(function(err) {
          toastr.error('发生错误，错误内容: ' + err);
          commitBtn.addClass("disabled");
        });
    });
  };

  return {

    //main function to initiate the module
    init: function(options) {
      numbro.culture('zh-CN');
      handleTable(options);
    }
  };
}();


function process(columns) {
    requires = ['滑出时间', '起飞时间', '降落时间', '停止时间', '任务类型', '起落次数'];
    for (var i = 0; i < columns.length; i++) {
        if ($.inArray(columns[i], requires) > -1) {
            columns[i] = '<em class="need">* </em>' + columns[i];
        }
    }
    return columns
}
