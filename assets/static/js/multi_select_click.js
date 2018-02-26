function InitLocalS() {
    var localKey = '';
}

InitLocalS.prototype.urlKeyMaps = {
    '/airmaterialcategory/': 'ac',
    '/airmaterialstoragelist/': 'sl',
    '/stockwarning/': 'sw',
    '/expirewarning/': 'ew',
};

InitLocalS.prototype.keys = ['ac', 'sl', 'sw', 'ew'];

InitLocalS.prototype.getKey = function() {
    return this.localKey;
}

InitLocalS.prototype.getPath = function() {
    var path = window.location.pathname;
    for (url in this.urlKeyMaps) {
        if (path.search(url) > 0) {
            this.localKey = this.urlKeyMaps[url];
        }
    }
}

InitLocalS.prototype.initKey = function() {
    if (this.localKey) {
        var local = localStorage.getItem(this.localKey);
        if (!local) {
            localStorage.setItem(this.localKey, JSON.stringify([]))
        }
    }
    for (var i = 0; i < this.keys.length; i++) {
        if (this.localKey != this.keys[i]) {
            localStorage.removeItem(this.keys[i]);
        }
    }
}


function multiClick(value, urlFunc) {
    var storage = new InitLocalS();
    storage.getPath();
    var typeInput = '<input type="text" hidden="hidden" name="type" value="'+ value +'"/>';
    var checkInput = '<input type="text" hidden="hidden" name="rowids[]" />';
    var $checkInput = $(checkInput);
    $checkInput.attr('value', JSON.parse(localStorage.getItem(storage.getKey())))
    var form = '<form hidden="hidden" id="formpost" action="' + urlFunc()  + '" method="POST"></form>';
    var $postForm = $(form)
    $postForm.append($checkInput[0]);
    $postForm.append(typeInput);
    $(document.body).append($postForm[0]);
    localStorage.removeItem(storage.getKey())
    $postForm.submit();
}

function multiCheckBox(localKey) {
    var local = localStorage.getItem(localKey);
    local = JSON.parse(local);
    if (local.length > 0) {
        $('input[name="rowid"]').each(function () {
            if ($.inArray(this.value.toString(), local) > -1) {
                this.checked = true;
            }
        })
    } else {
        // 对于已失效的勾选记录，后退操作会保留状态，对其进行还原操作
        $('input[name="rowid"]').each(function () {
            var checkedbox = this.checked;
            if (checkedbox) {
                this.checked = false;
            }
        })
    }
    $('input[name="rowid"]').change(function () {
        var local = localStorage.getItem(localKey);
        local = JSON.parse(local);
        if(this.checked){
            if ($.inArray(this.value, local) < 0){
                local.push(this.value);
            }
            localStorage.setItem(localKey, JSON.stringify(local));
        } else {
            if ($.inArray(this.value, local) > -1){
                local.splice($.inArray(this.value, local), 1);
                localStorage.setItem(localKey, JSON.stringify(local));
            }
        }
    })
}

$(function () {
    var storage = new InitLocalS();
    storage.getPath();
    storage.initKey();
    if (storage.getKey()) {
        multiCheckBox(storage.getKey());
    }
});