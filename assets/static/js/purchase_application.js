// 动态获取维修厂商的信息
$(function () {
    $("#supplier").change(function () {
        var name = $(this).val();
        var data = requestAjax(getSupplierDataFromName, {'name':name});
        data = JSON.parse(data);
        $("#contactPerson").val(data[0]);
        $("#telephone").val(data[1]);
        $("#fax").val(data[2]);
        $("#mailbox").val(data[3]);
    });
});

