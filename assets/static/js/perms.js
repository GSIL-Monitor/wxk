var ops = 0;
var options = '';

function groupDiv(the, selector) {
    return $(the).parents("div.inline-form-field")
        .find(selector)
        .parents("div[style*='background']");
}

function unShown(the, perm) {
    selector = "input[id$=-" + perm + "]";
    groupDiv(the, selector).css({
        "display": "none",
        "position": "fixed"
    });
}

function shown(the, perm) {
    selector = "input[id$=-" + perm + "]";
    groupDiv(the, selector).css({
        "display": "block",
        "position": "inherit"
    });
}

function showPerms(the, thePerms) {
    var all = allowed_actions;
    for (var perm in all) {
        if ($.inArray(all[perm], thePerms) != -1) {
            shown(the, all[perm]);
        }
        else {
            unShown(the, all[perm]);
        }
    }
}


function initShow(the) {
    var value = $(the).val();
    showPerms(the, model_allowed_perms[value]);
}

$("#actions").on("select2-opening", "select[id$='model']", function() {
    var op = options;
    $(this).empty();
    $(this).append(op);

    var id = $(this).attr("id");
    var opt = "#" + id + " option:first";
    var noThis = $("select[id$='model']").not(this);
    
    for (var i = 0; i < noThis.length; i++) {
        $(this).find("option[value=" + noThis[i].value + "]").remove();
    }
    
    if($(opt).val() != "__None"){
        $(this).prepend('<option selected="" value="__None"></option>');  
    }
    
});

$(document).on("change","#actions select[id$='model']", function() {
    initShow(this);
});

$(function() {
    var ops = $("select[name='actions-0-model'] option").size();
    var options = $("select[name='actions-0-model']").html(); 
    $("select[id$='model']").each(function() {
        initShow(this);
    });
    var selNum = $("select").length;
    if (ops == selNum){
        $("#actions-button").hide();
    }
});

$("#actions").on('click', "a.inline-remove-field", function() {
    var button = $("#actions-button");
    var showed = button[0].style.display;
    if(showed === 'none'){
        button.show();
    }
});

$("#actions-button").on('click', function() {
    if (ops == 0){
        ops = $("select[name='actions-0-model'] option").size();
        options = $("select[name='actions-0-model']").html();    
    }
    selNum = $("select").length;
    if (ops == selNum){
        $(this).hide();
    }
});