$(function(){
      //菜单高亮
      active_sub = location.href.split('sub=')[1]
      if(active_sub) active_sub = active_sub.split('&')[0]
      $('.profile-usermenu a').each(function(){
          var href = $(this).attr('href')
          var sub_action = href.split('sub=')[1];
          if(sub_action){
              sub_action = sub_action.split('&')[0]
              if(sub_action.indexOf(active_sub) >= 0){
                  $(this).parent().addClass('active')
              }else{
                  $(this).parent().removeClass('active')
              }
          }else{
                  $(this).parent().removeClass('active')
              }

          
      })
    //到期列表Tab页
     due_active_sub = location.href.split('mxtype=')[1]
      if(due_active_sub) {
        due_active_sub = due_active_sub.split('&')[0]
      }else{
        due_active_sub = 'scheduled'
      }
      $('.due_list_ul a').each(function(){
          var href = $(this).attr('href')
          var sub_action = href.split('mxtype=')[1];
          if(sub_action){
              sub_action = sub_action.split('&')[0]
              if(sub_action == due_active_sub){
                  $(this).parent().addClass('active')
              }else{
                  $(this).parent().removeClass('active')
              }
          }else{
                  $(this).parent().removeClass('active')
              }

          
      })
  })