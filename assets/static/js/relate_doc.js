$(function(){
    var files = $("#doc_files").val();
    if (files){
        files = JSON.parse(files);
        for(var i=0;i<files.length;i++) {
            var selectStr = "input[name=doc]:checkbox";
            var checkbox = $(selectStr);
            for(var y=0;y<checkbox.length;y++){
                if (Compare(JSON.parse(checkbox[y].value), files[i])) {
                    checkbox[y].checked = true;
                    break;
                }
            }
        }
    }
});

$("#submit").click(function(){
    var files = new Array();
    $("input[name='doc']:checkbox:checked").each(function(){
      files.push(JSON.parse(this.value));
    });
    var number = files.length;
    var show_head = '<div class="table-responsive"><table class="table table-striped table-hover table-bordered">'
    var show_tail = '</table></div>'
    var tables=new Array();
    if (number > 0){
        $("#doc_number").empty();
        tables.push(show_head);
        for (var i=0; i < number; i++){
            tables.push('<tr><td>');
            var aStr = '<a href=' + url + '?key=' + files[i].key+ '>'
            tables.push(aStr + files[i].name +'</a>');
            tables.push('</td></tr>')
        }
        tables.push(show_tail);
        var table_str=tables.join("");
        $("#doc_number").append(table_str);
    }
    else{
        $("#doc_number").empty();
    }
    files = JSON.stringify(files);
    $("#doc_files").val(files);
    $("#rd_modal_window").modal('hide');
});

function Compare(objA, objB) {
    if (!isObj(objA) || !isObj(objB)) return false; //判断类型是否正确
    if (getLength(objA) != getLength(objB)) return false; //判断长度是否一致
    return CompareObj(objA, objB, true); //默认为true
}

function isObj(object) {
    return object && typeof (object) == 'object' && Object.prototype.toString.call(object).toLowerCase() == "[object object]";
}

function isArray(object) {
    return object && typeof (object) == 'object' && object.constructor == Array;
}

function getLength(object) {
    var count = 0;
    for (var i in object) count++;
    return count;
}

function CompareObj(objA, objB, flag) {
    for (var key in objA) {
        if (!flag) //跳出整个循环
            break;
        if (!objB.hasOwnProperty(key)) {
            flag = false;
            break;
        }
        if (!isArray(objA[key])) { //子级不是数组时,比较属性值
            if (objB[key] != objA[key]) {
                flag = false;
                break;
            }
        } else {
            if (!isArray(objB[key])) {
                flag = false;
                break;
            }
            var oA = objA[key],
                oB = objB[key];
            if (oA.length != oB.length) {
                flag = false;
                break;
            }
            for (var k in oA) {
                if (!flag) //这里跳出循环是为了不让递归继续
                    break;
                flag = CompareObj(oA[k], oB[k], flag);
            }
        }
    }
    return flag;
}