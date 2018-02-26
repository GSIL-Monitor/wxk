function   formatDate(time)   {
  if(time > 0){
    time = time * 1000
    var date= new Date(time);
    var year=date.getYear()+1900;  
    var month=date.getMonth()+1; 
    var date=date.getDate();
    return year+"-"+month+"-"+date;  
  }else{
    return 'Empty'
  }
}