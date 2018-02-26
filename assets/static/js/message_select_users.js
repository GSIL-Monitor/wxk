$(function () {

    var $AllOp = $("#recieveId option").detach();
    var roleSelected = $("#role").val();

    showCanSelectOp($AllOp, roleSelected);

    $(document).on('change', '#role', function () {
        var roleSelected = $(this).val();
        showCanSelectOp($AllOp, roleSelected);
    })
})

function showCanSelectOp(allOp, value) {
    $("#recieveId").empty();
    getSeleceted(allOp);
    var $showOp = allOp.filter("[data-type*='" + value + "']");
    if ($showOp) {
        $("#recieveId").append($showOp);
    }
}

function getSeleceted(allOp) {
    var $selected = $("#s2id_recieveId").find('.select2-search-choice div');
    $selected.each(function () {
        var value = $(this).text();
        var $append = allOp.filter("[value='" + value + "']");
        if ($append) {
            $("#recieveId").append($append);
        }
    })
}
