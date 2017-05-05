//高亮选中标签
function GetQueryString(name)
{
  var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
  var r = window.location.search.substr(1).match(reg);
  if(r!=null)
    return unescape(r[2]); 

  return null;
};

(function(){
  var action = GetQueryString("sub");
  $('.subl').each(function(){
    var arr = $(this).attr('href').split('sub=');
    if(action == arr[1]){
      $(this).parent().addClass('active');
   } else if(!action){
     $('.subl:first').parent().addClass('active');
   }
  });
})();
