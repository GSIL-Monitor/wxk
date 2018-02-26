function onceRenderer(hot) {
    for (var y = 0; y < hot.countRows(); y++) {
        var types = hot.getDataAtCell(y, 0);
        if (isInArray(types)) {
            hot.setCellMeta(y, 4, 'readOnly', true);
        } else {
            if (hot.getDataAtCell(y, 2)) {
                hot.setCellMeta(y, 4, 'readOnly', true);
            }
        }
    }
}

function customNotNull(hot, row, col) {
    return true;
}

function customSettings(hot) {

    hot.updateSettings({
        afterChange: function (changes, source) {
            if (!changes) {
                return;
            }
            for (var i = 0; i < changes.length; i++) {
                if (changes[i][1] === 4) {
                    putOutStorageListQuantity(hot, changes, i);
                }
            }
        },
        beforeOnCellMouseDown: function (event, coords, TD) {
            var column = coords.col;
            var row = coords.row;
            if (column === 5) {
                clickGetSpecialTime(hot, 1, 2, 7, 5, row, column, 'effect');
            }
            if (column === 7) {
                clickGetSpecialTime(hot, 1, 2, 7, 5, row, column, 'nextcheck');
            }
        },
    })
}

function getBorrowAppNum() {
    return $("#borrow option:selected").text();
}

function getPn() {
    if (createOrEdit('/new/') || createOrEdit('/approve-edit-view/')) {
        var num = getBorrowAppNum();
        if (num === "") {
            return "noBorrow"
        }
        var data = requestAjax(getPnFormLendApp, { "num": num });
        return JSON.parse(data);
    } else {
        return "notCheck";
    }
}

$(function () {
    $("#borrow").change(function () {
        var value = getBorrowAppNum()
        var data = requestAjax(getBorrowInfo, { 'borrow': value });
        data = JSON.parse(data);
        $("#lendCategory").val(data[0]);
        $("#companyName").val(data[1]);
        $("#contactPerson").val(data[2]);
        $("#companyAddr").val(data[3]);
        $("#telephone").val(data[4]);
        $("#fax").val(data[5]);
        $("#mailbox").val(data[6]);
    });
});
