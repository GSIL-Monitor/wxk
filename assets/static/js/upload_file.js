var maxfiles = 3;
var index = 1;

function getFileName(obj){
    var fileName="";
    if(typeof(fileName) != "undefined")
    {
        fileName = $(obj).val().split("\\").pop();
    }
    return fileName;
}

function resetFileInput(file){
    file.after(file.clone().val(""));
    file.remove();
}

function showFile() {
    var idStr = "#accefile" + index;
    var fileIdStr = "#name" + index;
    var name = getFileName(idStr);
    $(fileIdStr).html(name)
    $(fileIdStr).parent().append('<span class="badge badge-danger">删除</span>');
    $(fileIdStr).parents().find(".list-group-item").removeAttr('style');
    index = index + 1
    $('#upload').attr('index', index);
    addFileList();
    addInput();
    checkCanUpload();
}

function checkCanUpload() {
    var fileNumber = $('input[id^="accefile"]').length;
    if (fileNumber > maxfiles) {
        $('#upload').attr('disabled', true);
    } else {
        if ($('#upload').attr('disabled')) {
            $('#upload').removeAttr('disabled');
        }
    }
}

function addFileList() {
    var ids = index;
    $('ul.list-group').append('<li class="list-group-item filename' + index + '" style="display: none;">' +
                              '<span id="name'+ ids +'"></span></li>')
}

function addInput() {
    var ids = index
    $('.inputs').append('<input name="acce'+ ids +'" id="accefile'+ ids +'" type="file" style="display: none;" />')
}

$('#upload').unbind('click').click(function () {
    var idStr = "#accefile" + index;
    $(idStr).click();
    $(idStr).change(function () {
        var ids = "#accefile" + index;
        var inputFile = $(ids);
        var value = $(ids).val();
        var size;
        if (value != "") {
            size = $(ids)[0].files[0].size/1024/1024;
        }
        if(size && size > 0 && size < 10 && value !="" && value.length >0 && value.length < 47){
            showFile();
        } else if (value !="" && value.length >= 47) {
            alert('附件文件名应该保持在30个字内');
            resetFileInput($(ids));
        } else if (size > 10) {
            resetFileInput($(ids));
            alert('附件不能大于10M');
        } else {
            resetFileInput($(ids));
        }
    });
});

$(document).on('click', '.badge.badge-danger', function(){
    var ids = $(this).prev().attr('id');
    var inputId = "#accefile" + ids.substr(ids.length-1, 1);
    $(this).parent().remove();
    $(inputId).remove();
    checkCanUpload();
})

$(function(){
    var fileNumber = $('input[id^="accefile"]').length;
    index = fileNumber;
    $('#upload').attr('index', index);
    checkCanUpload();
});