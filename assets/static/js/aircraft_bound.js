$(function() {
  var body = document.body;
  body.setAttribute('class','page-header-fixed page-sidebar-closed-hide-logo page-sidebar-closed');
  $('.page-sidebar-menu').attr('class','page-sidebar-menu page-sidebar-menu-closed')
  // 当前选中的类别
  var boundTag = function(){return $(".bounded_ul .active a").attr('href').split('#')[1] }
  // 当前选中的ID
  var boundId = function(){var tag = boundTag(); return $("#"+tag+" .boundedId").html() }
  // 此方法用于检查指定的字符串是否在数组中
  function in_array(search, array){for(var i in array){if(array[i] == search){return true; } } return false; }

    $("#hours").editable({
      display: function(value, response) {
        return false; 
      }, 
      validate: function(value) {
        if($.trim(value) == '') {
          return '请输入有效的数字'; 
        }
        else{
          if(!/^\d+(?:\.\d{1,2})?$/.test(value)){
            return '请输入正确的格式'
          }
        }
      }, 
      success: function(response, newValue){
        if(response.status == '200'){
          $("#hours").html(newValue); 
        }else{return '格式错误'; } }, error: function(response, newValue){return '格式错误.'; } })

    $("#times").editable({
      validate: function(value) {
        if($.trim(value) == '') {
          return '请输入有效的数字'; 
        }else{
          if(!/^\d+$/.test(value)){
            return '请输入正确的格式'
          }
        }
      }, 
      error: function(response, newValue){
        return '请输入有效的数字'; 
      } 
    })
  function HHmm(value){
    if(value && typeof(value) == 'number'){
      value = value.toString()
      if(value){
        var hour = value.split(".")[0]
        var minute = Math.round(parseFloat('0.'+value.split(".")[1]) * 60)
        if(minute < 10){
          minute = '0'+minute
        }
        return hour+':'+minute;
      }else{
        return '00:00'
      }
    }else{
      return '00:00'
    }
  }
  //初始化插件
  function editable_init(){
    // 绑定方案里的一堆
    $(".mx_hour").editable({
      validate:function(value){
        if($.trim(value) == '') {
          return '请输入有效的时间,格式为00:00'; 
        }
        else{
          if(!/^(\d+):[0-5]\d$/.test(value)){
            return '请输入正确的格式,格式为00:00'
          }
        }
      }, 
      success:function(response, newValue){
        var ellapsedHours = newValue.valueOf(); 
        if(boundTag() == 'lifecontrol' || boundTag() == 'timecontrol'){
          var boundId = $(this).parent().parent().parent().parent().attr('id'); 
          if(!boundId){
            var boundId = $("#"+boundTag()+" .boundedId").html(); 
          } 
        }else{
          var boundId = $("#"+boundTag()+" .boundedId").html(); 
        } 
        return post_data(boundId, ellapsedHours, 'hour'); 
      } 
    })
    $(".mx_date").editable({success:function(response, newValue){if(boundTag() == 'lifecontrol' || boundTag() == 'timecontrol'){var boundId = $(this).parent().parent().parent().parent().attr('id'); if(!boundId){var boundId = $("#"+boundTag()+" .boundedId").html(); } }else{var boundId = $("#"+boundTag()+" .boundedId").html(); } var completeDate = newValue.valueOf()/1000; return post_data(boundId, completeDate, 'date') } })
    $(".mx_time").editable({validate:function(value){
      if(!/^[0-9]\d*$/.test(value)){
        return '请输入正确的格式'
      }
      value = parseInt(value); if(value < 0 || isNaN(value)){return '请输入有效的数字'; } }, success:function(response, newValue){if(boundTag() == 'lifecontrol' || boundTag() == 'timecontrol'){var boundId = $(this).parent().parent().parent().parent().attr('id'); if(!boundId){var boundId = $("#"+boundTag()+" .boundedId").html(); } }else{var boundId = $("#"+boundTag()+" .boundedId").html(); } var ellapsedTimes = newValue.valueOf(); ellapsedTimes = parseInt(ellapsedTimes); return post_data(boundId, ellapsedTimes, 'time'); } })
    $(".mx_tc").editable({success:function(response, newValue){if(boundTag() == 'lifecontrol' || boundTag() == 'timecontrol'){var boundId = $(this).parent().parent().parent().parent().attr('id'); if(!boundId){var boundId = $("#"+boundTag()+" .boundedId").html() } }else{var boundId = $("#"+boundTag()+" .boundedId").html() } var tc = newValue.valueOf(); tc = parseInt(tc); return post_data(boundId, tc, 'tc') } })
    $(".mx_ng").editable({success:function(response, newValue){if(boundTag() == 'lifecontrol' || boundTag() == 'timecontrol'){var boundId = $(this).parent().parent().parent().parent().attr('id'); if(!boundId){var boundId = $("#"+boundTag()+" .boundedId").html() } }else{var boundId = $("#"+boundTag()+" .boundedId").html() } var ng = newValue.valueOf(); ng = parseInt(ng); return post_data(boundId, ng, 'ng') } })
    $(".mx_nf").editable({
      success:function(response, newValue){
        if(boundTag() == 'lifecontrol' || boundTag() == 'timecontrol'){
          var boundId = $(this).parent().parent().parent().parent().attr('id'); 
          if(!boundId){
            var boundId = $("#"+boundTag()+" .boundedId").html(); 
          } 
        }else{
          var boundId = $("#"+boundTag()+" .boundedId").html(); 
        } 
        var nf = newValue.valueOf(); 
        nf = parseInt(nf); 
        return post_data(boundId, nf, 'nf') 
      } 
    })
    $(".mx_engineTime").editable({validate:function(value){
        if($.trim(value) == '') {
          return '请输入有效的时间,格式为00:00'; 
        }
        else{
          if(!/^(\d+):[0-5]\d$/.test(value)){
            return '请输入正确的格式,格式为00:00'
          }
        }
      }, success:function(response, newValue){if(boundTag() == 'lifecontrol' || boundTag() == 'timecontrol'){var boundId = $(this).parent().parent().parent().parent().attr('id'); if(!boundId){var boundId = $("#"+boundTag()+" .boundedId").html(); } }else{var boundId = $("#"+boundTag()+" .boundedId").html(); } var engineTime = newValue.valueOf(); return post_data(boundId, engineTime, 'engineTime') } })
    $(".mx_number").editable({success:function(response, newValue){if(boundTag() == 'lifecontrol' || boundTag() == 'timecontrol'){var boundId = $(this).parent().parent().parent().parent().attr('id'); if(!boundId){var boundId = $("#"+boundTag()+" .boundedId").html(); } }else{var boundId = $("#"+boundTag()+" .boundedId").html(); } var mx_number = newValue.valueOf(); return post_data(boundId, mx_number, 'number') } })
    $(".timecontrol").hide()  
  }
  editable_init();
  // ComponentsFormTools2.init();
  // FormEditable.init();
  localStorage.removeItem('source');
  // 以下是绑定维修方案相关操作 
  // 点击修改绑定信息按钮
  $(document).on('click','.col-md-offset-2 a',function(){
    /*获取默认的第一项*/ localStorage.removeItem('post_data'); 
    $("a[href='#scheduled']").click(); 
  });
  // 点击是否跟踪
  $(document).on('click', ".bottom .onoff", function(){
    if(boundTag() == 'lifecontrol' || boundTag() == 'timecontrol'){
      var boundId = $(this).parent().parent().parent().parent().parent().parent().attr('id'); 
      if(!boundId){
        var boundId = $("#"+boundTag()+" .boundedId").html(); 
      } 
    }else{
      var boundId = $("#"+boundTag()+" .boundedId").html(); 
    } 
    if($(this).parent().attr('class')){
      return post_data(boundId, false, 'trace'); 
    }else{
   
      return post_data(boundId, true, 'trace'); 
    } 
  })

  // 收集,提交数据
  function post_data(id, value, tag){
    var all_data_info = JSON.parse(localStorage['response']);
    var this_info;
    all_data_info.forEach(function(v, k ,arr){if(v.boundedId == id){this_info = v; return this_info; } });
    if(!this_info){
      var localSource = JSON.parse(localStorage['source']);
      for(x in localSource){
        if(localSource[x].boundedId == id){
          this_info = localSource[x]
        }else{
          for(j in localSource[x].other){
            if(localSource[x].other[j].boundedId == id){
              this_info = localSource[x].other[j]
            }
          }
        }
      }
    }

    /*如果localstorage中有数据,也就是说已经做过修改操作还没有提交到后台*/
    if(localStorage['post_data']){
      /*实例化localstorage数据*/
      var stored = JSON.parse(localStorage['post_data']);
      /*创建已存的id数组*/
      var stored_id = new Array();
      stored.forEach(function(v, k, arr){stored_id[k] = v.boundedId; });
      /*如果要修改的这条数据已经存在于localstorage*/
      if(in_array(id, stored_id)){
        stored.forEach(function(v, k, arr){
          if(v.boundedId == id){
            if(tag == 'date') stored[k].completeDate = value
            if(tag == 'hour') stored[k].ellapsedHours = value
            if(tag == 'time') stored[k].ellapsedTimes = value
            if(tag == 'tc') stored[k].tc = value
            if(tag == 'ng') stored[k].ng = value
            if(tag == 'nf') stored[k].nf = value
            if(tag == 'engineTime') stored[k].engineTime = value
            if(tag == 'number') stored[k].serialNumber = value
            if(tag == 'trace') stored[k].trace = value
          }
        })
      }else{
        if(tag == 'date') this_info.completeDate = value;
        if(tag == 'hour') this_info.ellapsedHours = value;
        if(tag == 'time') this_info.ellapsedTimes = value;
        if(tag == 'tc') this_info.tc = value;
        if(tag == 'ng') this_info.ng = value;
        if(tag == 'nf') this_info.nf = value;
        if(tag == 'engineTime') this_info.engineTime = value;
        if(tag == 'trace') this_info.trace = value;
        if(tag == 'number') this_info.serialNumber = value;
        stored.push(this_info)
      }
        localStorage.post_data = JSON.stringify(stored)
    }else{
      if(tag == 'date') this_info.completeDate = value;
      if(tag == 'hour') this_info.ellapsedHours = value;
      if(tag == 'time') this_info.ellapsedTimes = value;
      if(tag == 'tc') this_info.tc = value;
      if(tag == 'ng') this_info.ng = value;
      if(tag == 'nf') this_info.nf = value;
      if(tag == 'engineTime') this_info.engineTime = value;
      if(tag == 'trace') this_info.trace = value;
      if(tag == 'number') this_info.serialNumber = value;
      var arr = new Array();
      arr[0] = this_info;
      localStorage.post_data = JSON.stringify(arr)
    }
  }
  // 点击tag标签
  $(document).on('click', ".bounded_ul a", function(){
    url = $(this).attr('for');
    
    $(".timecontrol").show();
    
    $.blockUI({ css:{ backgroundColor:'none', border:'none'},message: '<h1><img src="/static/img/loading-spinner-default.gif" .>' });
    $(".blockUI").css('z-index','10051');
    getData(url)
    .then(function(result){
      if(boundTag() == 'timecontrol' || boundTag() == 'lifecontrol'){
        $(".addTrace").show()
      }else{
        $(".addTrace").hide()
      }
      return register_event(result);
    })
  })

  function in_key(search, obj){
    if(JSON.stringify(obj) == "{}"){
       return false
    }else{
      for(x in obj){
        if(search == x){
          return true
        }
      }
        return false
    }
  }

  // 获取维修方案信息
  function getData(url){
    var action = new Promise(function(resolve,reject){
      var cur = new Date();
      url = url + '&stamp=' + cur.getTime()
      $.get(url,{},function(result){
        
        /*拼页面左侧ID列表,加到对应的位置*/
        var len = result.data.items.length;
        var item = result.data.items
        if(!item) {
          $.unblockUI();
          return '暂无数据'
        }
        if(boundTag() == 'lifecontrol' || boundTag() == 'timecontrol'){
          var objArr = new Object()
          objArr = new Object()
          item.forEach(function(v, k, arr){
            if(in_key(v.id, objArr) == false){
              objArr[v.id] = v
              objArr[v.id].other = new Array()
            }else{
              objArr[v.id].other.push(v)
            }
          })

          var str = '<ul class="list-group">';
          for(x in objArr){
            str += '<li class="list-group-item bound_id" for="'+x+'"><a>' + objArr[x]['id'] + '</a></li>'
          }
          str += '</ul>';
          $("#"+boundTag()+' .col-md-4').html('').wrapInner(str);
          localStorage.source = JSON.stringify(objArr)

        }else{
          var str = '<ul class="list-group">';
          for (var i = 0; i < len; i++) {
            if('id' in item[i]){
              str += '<li class="list-group-item bound_id" for="'+i+'"><a>' + item[i]['id'] + '</a></li>'
            }
          }
          str += '</ul>';
          $("#"+boundTag()+' .col-md-4').html('').wrapInner(str);
          localStorage.response = JSON.stringify(item)
          if(localStorage.source){
            localStorage.removeItem('source');
          }
        }
        resolve(result);
      })
    });
    return action;
  }


  $(".addTrace").click(function(){
      $.get(
        '/admin/aircraft_informationview/mx-duplicate/',
        {
          'mxId':$(this).attr('mxid'),
          'mxType':$(this).attr('mxtype'),
          'planeId':$(this).attr('planeid'),
        },
        function(msg){
          $("#"+boundTag()+" .bottom:first").find('.profile-desc-text').attr('id', boundId())  
          DIV = $("#"+boundTag()+" .bottom:first").clone()
          DIV.find('.profile-desc-text').attr('id', msg.data.boundedId)
          DIV.find('.mx_date,.mx_time,.mx_hour,.mx_number,.mx_tc,.mx_ng,.mx_nf,.mx_engineTime').html('')
          DIV.find('.checked').removeAttr('class')
          DIV.appendTo('#'+boundTag()+' .col-md-8')
          editable_init();
          var all_data_info = JSON.parse(localStorage['response']);
          var exist_id = new Array();
          all_data_info.forEach(function(v, k, arr){exist_id[k] = v.boundedId; });
          if(!in_array(msg.data.boundedId, exist_id)){
            all_data_info.push(msg.data)
          }
          localStorage.response = JSON.stringify(all_data_info)
        })
    })

  function bottom_str(flag, data){
    if(flag == 'stored'){
      if(localStorage['post_data']){
          var stored = JSON.parse(localStorage['post_data'])
      }else{
          var stored = []
          stored[0] = {boundedId:data.boundedId}
      }

      if(stored.length > 0){
        for(var i = 0; i < stored.length; i++){
          if(data.boundedId == stored[i].boundedId){
            mxDate = stored[i].completeDate?stored[i].completeDate:data.completeDate
            mxDate = formatDate(mxDate)
            mxTime = stored[i].ellapsedTimes?stored[i].ellapsedTimes:data.ellapsedTimes
            mxHour = stored[i].ellapsedHours?stored[i].ellapsedHours:data.ellapsedHours
            mxNumber = stored[i].serialNumber?stored[i].serialNumber:data.serialNumber
            mxTc = stored[i].tc?stored[i].tc:data.tc
            mxNg = stored[i].ng?stored[i].ng:data.ng
            mxNf = stored[i].nf?stored[i].nf:data.nf
            mxEngineTime = stored[i].engineTime?stored[i].engineTime:data.engineTime
            trace = stored[i].trace?stored[i].trace:data.trace
            break                                                                                                                                                                                                                                                                                                                                                                                                             
          }else{
            mxDate = data.completeDate
            mxDate = formatDate(mxDate)
            mxTime = data.ellapsedTimes
            mxHour = data.ellapsedHours
            mxNumber = data.serialNumber
            mxTc = data.tc
            mxNg = data.ng
            mxNf = data.nf
            mxEngineTime = data.engineTime
            trace = data.trace
          }
        }
      }
      $("#"+boundTag()+" .bottom:first").find('.profile-desc-text').attr('id', data.boundedId) 
      if(trace){
        $("#"+boundTag()+" .onoff").parent().addClass('checked')
      }else{
        $("#"+boundTag()+" .onoff").parent().removeClass("checked")
      }

      if(mxNumber == '') mxNumber = 0
      $("#"+boundTag()+" .mx_date").html(mxDate)
      $("#"+boundTag()+" .mx_time").html(mxTime)

      if(typeof(mxHour) == 'number'){
        mxHour = HHmm(mxHour)
      }
      if(typeof(mxEngineTime) == 'number'){
        mxEngineTime = HHmm(mxEngineTime)
      }

      if(mxHour == 0){
        $("#"+boundTag()+" .mx_hour").html('00:00')
      }else{
        $("#"+boundTag()+" .mx_hour").html(mxHour)
      }
      if(mxEngineTime == 0){
        $("#"+boundTag()+" .mx_engineTime").html('00:00')
      }else{
        $("#"+boundTag()+" .mx_engineTime").html(mxEngineTime)
      }
      
      $("#"+boundTag()+" .mx_number").html(mxNumber)
      $("#"+boundTag()+" .mx_tc").html(mxTc)
      $("#"+boundTag()+" .mx_ng").html(mxNg)
      $("#"+boundTag()+" .mx_nf").html(mxNf)
    }else if(flag == 'special'){
      if(localStorage['post_data']){
          var stored = JSON.parse(localStorage['post_data'])
      }else{
          var stored = []
      }
      $("#"+boundTag()+" .bottom:first").find('.profile-desc-text').attr('id', data.boundedId) 
      $("#"+boundTag()+" .bottom:first").nextAll().remove()
      if(stored.length > 0){
        for(var i = 0; i < stored.length; i++){
          if(data.boundedId == stored[i].boundedId){
            mxDate = stored[i].completeDate?stored[i].completeDate:data.completeDate
            mxDate = formatDate(mxDate)
            mxTime = stored[i].ellapsedTimes?stored[i].ellapsedTimes:data.ellapsedTimes
            mxHour = stored[i].ellapsedHours?stored[i].ellapsedHours:data.ellapsedHours
            mxNumber = stored[i].serialNumber?stored[i].serialNumber:data.serialNumber
            mxTc = stored[i].tc?stored[i].tc:data.tc
            mxNg = stored[i].ng?stored[i].ng:data.ng
            mxNf = stored[i].nf?stored[i].nf:data.nf
            mxEngineTime = stored[i].engineTime?stored[i].engineTime:data.engineTime
            trace = stored[i].trace?stored[i].trace:data.trace
            break                                                        
          }else{
            mxDate = data.completeDate
            mxDate = formatDate(mxDate)
            mxTime = data.ellapsedTimes
            mxHour = data.ellapsedHours
            mxNumber = data.serialNumber
            mxTc = data.tc
            mxNg = data.ng
            mxNf = data.nf
            mxEngineTime = data.engineTime
            trace = data.trace
          }
        }
        
        if(trace){
          $("#"+boundTag()+" .onoff").parent().addClass('checked')
        }else{
          $("#"+boundTag()+" .onoff").parent().removeClass("checked")
        }
        if(mxNumber == '') mxNumber = 0
        $("#"+data.boundedId+" .mx_date").html(mxDate)
        $("#"+data.boundedId+" .mx_time").html(mxTime)
        
        $("#"+data.boundedId+" .mx_number").html(mxNumber)
        if(typeof(mxHour) == 'number'){
          mxHour = HHmm(mxHour)
        }
        if(typeof(mxEngineTime) == 'number'){
          mxEngineTime = HHmm(mxEngineTime)
        }

        if(mxHour == 0){
          $("#"+boundTag()+" .mx_hour").html('00:00')
        }else{
          $("#"+boundTag()+" .mx_hour").html(mxHour)
        }
        if(mxEngineTime == 0){
          $("#"+boundTag()+" .mx_engineTime").html('00:00')
        }else{
          $("#"+boundTag()+" .mx_engineTime").html(mxEngineTime)
        }
        $("#"+data.boundedId+" .mx_tc").html(mxTc)
        $("#"+data.boundedId+" .mx_ng").html(mxNg)
        $("#"+data.boundedId+" .mx_nf").html(mxNf)
      }else{
        if(data.other.length > 0){
          for(x in data.other){
            DIV = $("#"+boundTag()+" .bottom:first").clone()
            DIV.find('.profile-desc-text').attr('id',data.other[x].boundedId)
            mxDate = formatDate(data.other[x].completeDate)
            DIV.find('.mx_date').html(mxDate)
            DIV.find('.mx_time').html(data.other[x].ellapsedTimes)
            if(typeof(data.other[x].ellapsedHours) == 'number'){
              data.other[x].ellapsedHours = HHmm(data.other[x].ellapsedHours)
            }
            if(typeof(data.other[x].engineTime) == 'number'){
              data.other[x].engineTime = HHmm(data.other[x].engineTime)
            }
            if(data.other[x].ellapsedHours == 0){
              DIV.find('.mx_hour').html('00:00')
            }else{
              DIV.find('.mx_hour').html(data.other[x].ellapsedHours)
            }
            if(data.other[x].engineTime == 0){
              DIV.find('.mx_engineTime').html('00:00')
            }else{
              DIV.find('.mx_engineTime').html(data.other[x].engineTime)
            }
            DIV.find('.mx_number').html(data.other[x].serialNumber?data.other[x].serialNumber:0)
            DIV.find('.mx_tc').html(data.other[x].tc)
            DIV.find('.mx_ng').html(data.other[x].ng)
            DIV.find('.mx_nf').html(data.other[x].nf)
            if(data.other[x].trace){
              DIV.find('.onoff').parent().addClass('checked')
            }else{
              DIV.find('.onoff').parent().removeClass("checked")
            }
            DIV.appendTo('#'+boundTag()+' .col-md-8')
          }
          mxDate = formatDate(data.completeDate)
          $("#"+data.boundedId+" .mx_date").html(mxDate)
          $("#"+data.boundedId+" .mx_time").html(data.ellapsedTimes)
          $("#"+data.boundedId+" .mx_hour").html(HHmm(data.ellapsedHours))
          $("#"+data.boundedId+" .mx_number").html(data.serialNumber?data.serialNumber:0)
          $("#"+data.boundedId+" .mx_tc").html(data.tc)
          $("#"+data.boundedId+" .mx_ng").html(data.ng)
          $("#"+data.boundedId+" .mx_nf").html(data.nf)
          $("#"+data.boundedId+" .mx_engineTime").html(HHmm(data.engineTime))
          if(data.trace){
            $("#"+data.boundedId+" .onoff").parent().addClass('checked')
          }else{
            $("#"+data.boundedId+" .onoff").parent().removeClass("checked")
          }
        }else{
          mxDate = formatDate(data.completeDate)
          $("#"+data.boundedId+" .mx_date").html(mxDate)
          $("#"+data.boundedId+" .mx_time").html(data.ellapsedTimes)
          $("#"+data.boundedId+" .mx_hour").html(HHmm(data.ellapsedHours))
          $("#"+data.boundedId+" .mx_number").html(data.serialNumber?data.serialNumber:0)
          $("#"+data.boundedId+" .mx_tc").html(data.tc)
          $("#"+data.boundedId+" .mx_ng").html(data.ng)
          $("#"+data.boundedId+" .mx_nf").html(data.nf)
          $("#"+data.boundedId+" .mx_engineTime").html(HHmm(data.engineTime))
          if(data.trace){
            $("#"+data.boundedId+" .onoff").parent().addClass('checked')
          }else{
            $("#"+data.boundedId+" .onoff").parent().removeClass("checked")
          }
        }
      }
    }
    str = renderTemplate(data)
    $("#"+boundTag()+" .col-md-8").show();
    $("#"+boundTag()+" .col-md-8 .top").html('').wrapInner(str);
      editable_init();
      $.unblockUI();
  }

  $(document).on('click','.onoff',function(){
    if($(this).parent().attr('class')){
      $(this).parent().removeClass('checked')
    }else{
      $(this).parent().addClass("checked")
    }
  })
  // 注册点击事件
  function register_event(result){
    $(document).on('click','#'+boundTag()+' .bound_id',function(){
      $(this).css('background',"rgb(220, 224, 226)")
      $(this).siblings().css('background','#fff')

      var No = $(this).attr('for')
  
      if((boundTag() == 'lifecontrol' || boundTag() == 'timecontrol') && localStorage.source){
        var special = JSON.parse(localStorage['source'])[No]
        $("#"+boundTag()+" .addTrace").attr({'mxId':special.id,'mxType':boundTag()})
        bottom_str('special', special)

      }else{
        bottom_str('stored',result.data.items[No])

      }

    })
    $("#"+boundTag()+" .bound_id:first").click()
  }


  function renderTemplate(data){
    for(x in data){
      if($.inArray(x, ['rii', 'forceExec']) > -1){
        if(data[x] === true){
          data[x] = '是'
        }else if(data[x] === false){
          data[x] = '否'
        }
      }
    }
    var sl = '<tr><td class="profile-desc-title col-sm-3">'
    var sr = '</td></tr>'
    var str = '<table class="table table-hover table-bordered table-striped basic_infomation profile-desc-text">'
    str += '<label class="boundedId">' + data.boundedId + '</label>'
    if(!(typeof(data.interval) == 'undefined')){
      var len = data.interval.length
      for(x in data.interval){
        if(x == 0){
          var type_left_td = '<tr><td rowspan="' + len + '" class="profile-desc-title col-sm-3">间隔类型:</td>'
        }else{
          var type_left_td = '<tr>'
        }
        if(data.interval[x].offsetType == 2){
          var unit = '天'
        }else if (data.interval[x].offsetType == 3) {
          var unit = '月'
        }else if (data.interval[x].offsetType == 4) {
          var unit = '年'
        }
        if(data.interval[x].type == 0){
          str += type_left_td + '<td>飞行小时' + data.interval[x].value + '小时</td><td>-' + data.interval[x].min + '小时/+' + data.interval[x].max + '小时' + sr
        }else if(data.interval[x].type == 1){
          str += type_left_td + '<td>起落/循环次数' + data.interval[x].value + '次</td><td>-' + data.interval[x].min + '次/+' + data.interval[x].max + '次' + sr
        }else if(data.interval[x].type == 2){
          str += type_left_td + '<td>日历时间' + data.interval[x].value + '天</td><td>-' + data.interval[x].min + unit + '/+' + data.interval[x].max + unit + sr
        }else if(data.interval[x].type == 3){
          str += type_left_td + '<td>日历时间' + data.interval[x].value + '月</td><td>-' + data.interval[x].min + unit + '/+' + data.interval[x].max + unit + sr
        }else if(data.interval[x].type == 4){
          str += type_left_td + '<td>日历时间' + data.interval[x].value + '年</td><td>-' + data.interval[x].min + unit + '/+' + data.interval[x].max + unit + sr
        }else if(data.interval[x].type == 6){
          str += type_left_td + '<td>扭矩循环次数' + data.interval[x].value + '次</td><td>-' + data.interval[x].min + '次/+' + data.interval[x].max + '次' + sr
        }else if(data.interval[x].type == 7){
          str += type_left_td + '<td>燃气发生器循环数' + data.interval[x].value + '次</td><td>-' + data.interval[x].min + '次/+' + data.interval[x].max + '次' + sr
        }else if(data.interval[x].type == 8){
          str += type_left_td + '<td>动力涡轮循环数' + data.interval[x].value + '次</td><td>-' + data.interval[x].min + '次/+' + data.interval[x].max + '次' + sr
        }else if(data.interval[x].type == 9){
          str += type_left_td + '<td>发动机时间' + data.interval[x].value + '小时</td><td>-' + data.interval[x].min + '小时/+' + data.interval[x].max + '小时' + sr
        }
      }
    }
    if(!(typeof(data.ataCode) == 'undefined'))str += sl + 'ATA章节:</td><td>' + data.ataCode + sr
    if(!(typeof(data.description) == 'undefined'))str += sl + '维修描述:</td><td>' + data.description + sr
    if(!(typeof(data.environmentCategory) == 'undefined'))str += sl + '环境类别:</td><td>' + data.environmentCategory + sr
    if(!(typeof(data.reference) == 'undefined'))str += sl + '参考章节:</td><td>' + data.reference + sr
    if(!(typeof(data.name) == 'undefined'))str += sl + '部件名:</td><td>' + data.name + sr
    if(!(typeof(data.category) == 'undefined'))str += sl + '类别:</td><td>' + data.category + sr
    if(!(typeof(data.adapt) == 'undefined'))str += sl + '适用性:</td><td>' + data.adapt + sr
    if(!(typeof(data.area) == 'undefined'))str += sl + '所属区域:</td><td>' + data.area + sr
    if(!(typeof(data.source) == 'undefined'))str += sl + '来源:</td><td>' + data.source + sr
    if(!(typeof(data.forceExec) == 'undefined'))str += sl + '强制执行项:</td><td>' + data.forceExec + sr
    if(!(typeof(data.remark) == 'undefined'))str += sl + '备注:</td><td>' + data.remark + sr
    if(!(typeof(data.rii) == 'undefined'))str += sl + '必检项RII:</td><td>' + data.rii + sr
    if(!(typeof(data.pn) == 'undefined'))str += sl + '型号:</td><td>' + data.pn + sr
    
    if(!(typeof(data.completeDate) == 'undefined')){$(".bound_date").show(); }else{$(".bound_date").hide(); } if(!(typeof(data.ellapsedTimes) == 'undefined')){$(".bound_time").show(); }else{$(".bound_time").hide(); } if(!(typeof(data.ellapsedHours) == 'undefined')){$(".bound_hour").show(); }else{$(".bound_hour").hide(); } if(!(typeof(data.serialNumber) == 'undefined')){$(".bound_number").show(); }else{$(".bound_number").hide(); } if(!(typeof(data.tc) == 'undefined')){$(".bound_tc").show(); }else{$(".bound_tc").hide(); } if(!(typeof(data.ng) == 'undefined')){$(".bound_ng").show(); }else{$(".bound_ng").hide(); } if(!(typeof(data.nf) == 'undefined')){$(".bound_nf").show(); }else{$(".bound_nf").hide(); }if(!(typeof(data.trace) == 'undefined')){$(".bound_trace").show(); }else{$(".bound_trace").hide(); }if(!(typeof(data.engineTime) == 'undefined')){$(".bound_engineTime").show(); }else{$(".bound_engineTime").hide(); }
  
    str += '</table>'
    return str
  }
  function floatToStr(totalHours){
    totalHours = totalHours.replace(/：/ig,':');
    var hour = parseInt(totalHours.split(":")[0])
    var minute = parseInt(totalHours.split(":")[1])
    minute = minute / 60
    var totalHours = hour+minute
    return totalHours
  }
  // 提交:localStorage中的数据提交到后台
  $(document).on('click', "#fa_status_modal_window .modal-footer .btn-primary", function(){
    var url = $("#mx_post_url").val(); 
    if(localStorage['post_data']){
      var postData = JSON.parse(localStorage['post_data']); 
      for(x in postData)
      {
        if(typeof(postData[x].ellapsedHours) == 'string'){
            postData[x].ellapsedHours = floatToStr(postData[x].ellapsedHours)
        }
        if(typeof(postData[x].engineTime) == 'string'){
            postData[x].engineTime = floatToStr(postData[x].engineTime)
        }
        if(postData[x].serialNumber == '') postData[x].serialNumber = '0'

      }
      postData = $.toJSON(postData); 

      $.post(url, postData, function(result){

      if(result.code == 200){
        window.location.reload();
        localStorage.removeItem('post_data');} 
      }) 
    }else{
      $("#fa_status_modal_window .modal-footer .btn-default").click()
    }
    
  })
  // 点击取消
  $(document).on('click', "#fa_status_modal_window .modal-footer .btn-default", function(){localStorage.removeItem('post_data'); })

  return false
});