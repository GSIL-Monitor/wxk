function onceRenderer(hot) {
}

function customNotNull(hot, row, col) {
    return true;
}

function customSettings(hot) {
    hot.updateSettings({
        afterChange: function (changes, source) {
            for (var i=0; i< changes.length; i++) {
                if (!changes) {
                    return;
                }
                if (changes[i][1] === 0) {
                    reSetTypes(hot, changes, i, 3);
                    hotRemoveExistPn(hot, changes[i][0], changes[i][1] + 1);
                }
                if (changes[i][1] === 1){
                    setDataByPnChanged(hot, getPnUrl, 3, changes, i, {'2': 2})
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