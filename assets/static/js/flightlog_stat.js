$(".pull-right .btn-default").click(function(){
  $(this).attr('href', 'javascript:;')
  $(".remove-filter").click()
})

var flightlogStat = function() {

  var calTotalTimeWithFormat = function(datas) {  
    // 每个数据应该都是HH:mm的格式
    var total = 0;
    for (var idx = 0; idx < datas.length; ++idx) {
  
      if (!datas[idx]) continue;

      var parts = datas[idx].split(':');

      total += (parseFloat(parts[0]) * 60) + parseFloat(parts[1]);
    }

    var hours_part = parseInt(parseInt(total) / 60);

    var minute_parts = parseInt(total - (hours_part * 60) );

    if(hours_part < 10){
      hours_part = '0' + hours_part
    }

    if(minute_parts < 10){
      minute_parts = '0' + minute_parts
    }

    return hours_part + ":" + minute_parts;
  };

  var calcLandingsWithFormat = function(datas) {

    var total = 0;
    for (var idx = 0; idx < datas.length; ++idx) {

      if (!datas[idx]) continue;

      total += parseInt(datas[idx]);
    }

    return '' + total;
  };

  var handleTable = function(opt) {

    var headers = opt.headers;

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
      columns: opt.columns,
      stretchH: 'all',
      className: 'table-scrollable htCenter',
      rowHeaders: true,
      dataSchema: {
        flightDate: opt.flightDay
      },
      fillHandle: false,
      afterBeginEditing: function(row, col) {
        // 如果时间对应的数据不为空
        if (opt.timeColumns.indexOf(col) != -1) {
          if (!this.getDataAtCell(row, col)) {
            this.setDataAtCell(row, col, moment().format('HH:mm'));
          }
        }
      },
      // 根据数据的状态决定是否显示统计信息
      afterInit: function() {

        // 下面的逻辑主要适用于通过前端来统计飞行信息
        var data = this.getData();
        var stat_ele = $("#status_info");
        var print_ele = $('#printer');
        if (data.length > 0) {

          var _flighttime_data = [];
          var _enginetime_data = [];
          var _landings_data = [];
          for (var idx = 0; idx < data.length; idx++) {
            _flighttime_data.push(data[idx][10]);
            _enginetime_data.push(data[idx][11]);
            _landings_data.push(data[idx][16]);
          }
          $('#hours h3').html(calTotalTimeWithFormat(_flighttime_data));
          $('#engine h3').html(calTotalTimeWithFormat(_enginetime_data));
          $('#landings h3').html(calcLandingsWithFormat(_landings_data));

          stat_ele.attr('style', 'display: block');
          print_ele.show();

          return;
        }

        stat_ele.attr('style', 'display: none');
        print_ele.hide();
      }
    });

    // 解决高度的问题
    var resizeFunc = function() {
      hot.updateSettings({
        height: $(window).height() - $("#flightlog_table").offset().top - 150
      });
    };

    resizeFunc();
    $(window).resize(resizeFunc);
  };

  return {

    //main function to initiate the module
    init: function(options) {
      handleTable(options);
    }
  };
}();
