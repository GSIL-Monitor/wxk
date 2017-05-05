var popup = function(text, title='', url='', annotation='') {
  $('#popForm').attr('action', url)
  $('#myModalLabel').text(title)
  
  if(annotation){
    $('#annotation').show()
    $('#myModalText').text('').hide()
  }else{
    $('#annotation').hide()
    $('#myModalText').show().text(text)
  }
};
$(document).on('click','#btn-primary',function(){
   $('#popForm').submit()
})