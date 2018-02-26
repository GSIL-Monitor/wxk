function onceRenderer(hot) {
}

function customNotNull(hot, row, col) {
    return true;
}

function customSettings(hot) {
    hot.updateSettings({
        beforeRenderer: function (TD, row, col, prop, value, cellProperties) {
            if (col === 4) {
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