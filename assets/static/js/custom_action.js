var popup = function(text, title, url, annotation){
  $('#popForm').attr('action', url)
  var href = location.href
  try {
    sub = href.split("sub=")[1].split("&")[0];
    if(sub == 'flightlog'){
      type = href.split("flt_1=")[1].split("&")[0];
      basicId = href.split("id=")[1].split("&")[0];
      if(url){
          if(url.indexOf('basicId') < 0){
            $('#popForm').attr('action', url+'&basicId='+basicId+'&type='+type);
          }
      }
    }
  }
  catch(err) {
  }

  $('#ModalLabel').text(title);
  
  if(annotation){
    $('#annotation').show();
    $('#ModalText').text('').hide();
  }else{
    $('#annotation').remove();
    $('#ModalText').show().text(text);
  }
};

$(document).on('click','#btn-primary',function(){
  $(this).attr('disabled', 'disabled')
  $('#popForm').submit();
});
