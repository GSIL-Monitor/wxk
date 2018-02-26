var formulaStat = function() {

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
          var peifangArray = new Array()
          for(i in data){
            if(data[i][8]){
              if(data[i][7] > 0){
                var thisArray = new Array()
                thisArray[data[i][8]] = data[i][7]
                peifangArray.push(thisArray)
              }
            }
          }
          var json = {};
          $.each(peifangArray, function(i,n){
            for(x in n){
              if(!json[x]){
                json[x] = n[x]
              }else{
                json[x] = json[x] + n[x]
              }
            }
          })
          $.get('/admin/forumula-stat/get-name/', json, function(msg){
            if(msg.code == 200){
              var obj = {}
              for(x in msg.data){
                if(!obj[msg.data[x]['name']]){
                  obj[msg.data[x]['name']] = msg.data[x]['weight']
                }else{
                  obj[msg.data[x]['name']] += msg.data[x]['weight']
                }
              }

              var name_str =  ''
              var weight_str = ''
              for(x in obj){
                name_str += '<h3>' + x + '</h3>'
                weight_str += '<h3>' + obj[x] + '</h3>'
              }
              $("#hours h3,#engine h3").remove()
              $('#hours').append(name_str)
              $('#engine').append(weight_str)
            }
          })
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

$(function(){

})
