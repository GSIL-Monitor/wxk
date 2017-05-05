$(function(){
  $(document).on('click','#actions-button',function(){
      switch_form()
  })
    var len = $(".onoff").length
   $(".onoff").each(function(i){
    $(this).parent().parent().prev().hide()
    $(this).parent().parent().parent().css({'float':'left','margin':'0px 2%','background':'none','width':'205px'})
    $(this).parent().parent().attr('class','col-md-12')
      $(this).bootstrapSwitch({
          onText:$(this).next().find('label').html(),  
          offText:$(this).next().find('label').html(),
     });
    if(i === len - 1){
        $('.admin-form').append('<style>.well{background:none !important}</style>')
        $('.inline-form-field').css('width','700px').append('<div style="clear:both"></div')
    }
    $('.bootstrap-switch-handle-on,.bootstrap-switch-handle-off').css('width','86px')
   })

})


function switch_form(){
   var len = $(".onoff").length
   $(".onoff").each(function(i){
      $(this).parent().parent().prev().hide()
      var parentDiv = $(this).parent().parent().parent()
      
      var colmd = $(this).parent().parent()
      if(colmd.attr('class') == 'col-md-10'){
          colmd.attr('class','col-md-12')
      }
      if(parentDiv.attr('class') == 'form-group'){
          parentDiv.css({'float':'left','margin':'0px 2%','background':'none','width':'205px'})
      }
      $(this).bootstrapSwitch({
          onText:$(this).next().find('label').html(),  
          offText:$(this).next().find('label').html(),
     });
      if(i === len - 1){
        $('.inline-form-field').css('width','700px').append('<div style="clear:both"></div')
    }
    $('.bootstrap-switch-handle-on,.bootstrap-switch-handle-off').css('width','86px')
   })
}