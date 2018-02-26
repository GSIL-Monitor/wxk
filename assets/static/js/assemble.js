function onceRenderer(hot) {

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
                if (changes[i][1] === 5) {
                    var value = changes[i][3];
                    var num = getAssAppNum();
                    var pn = hot.getDataAtCell(changes[i][0], 1);
                    var oldValue = requestAjax(getNumberFromAsapPn, { "pn": pn, "num": num });
                    if (value > oldValue) {
                        alert('数值不能大于申请数量');
                        hot.setDataAtCell(changes[i][0], 5, oldValue);
                    }
                }
            }

        },
        beforeRenderer: function (TD, row, col, prop, value, cellProperties) {
            if (col === 5) {
                var types = hot.getDataAtCell(row, 0);
                if (isInArray(types)) {
                    cellProperties.readOnly = true;
                }
                else {
                    cellProperties.readOnly = false;
                }
            }
        },
    })
}

function getAssAppNum() {
    return $("#assembleApplication option:selected").text();
}