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

                if (changes[i][1] === 0 && changes[i][3]) {
                    reSetTypes(hot, changes, i, 5);
                    hotRemoveExistPn(hot, changes[i][0], changes[i][1] + 1);
                }

                if (changes[i][1] === 1 && changes[i][3]){
                    var values = {'2': 2};
                    setDataByPnChanged(hot, getPnUrl, 5, changes, i, values);
                }

                if (changes[i][1] === 4 || changes[i][1] === 5) {
                    var x = hot.getDataAtCell(changes[i][0], 4);
                    var y = hot.getDataAtCell(changes[i][0], 5);
                    if (x && y && isNumber(x) && isNumber(y)) {
                        var z = parseFloat(x) * parseFloat(y);
                        hot.setDataAtCell(changes[i][0], 6, z);
                    } else {
                        hot.setDataAtCell(changes[i][0], 6, null);
                    }
                }
            }
        },

        beforeOnCellMouseDown: function (event, coords, TD) {
            var column = coords.col;
            var row = coords.row;
            if (column === 1) {
                hotRemoveExistPn(hot, row, column);
            }
        },

    })
}
