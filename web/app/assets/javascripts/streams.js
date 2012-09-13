$(document).ready(function(){
    switchToIndex(0);

    $(".streamArticle").click(function(){
        switchToIndex($(this).index());
    });

    $("body").keydown(function(e){
        if(e.keyCode === 38){
            switchToPreviousArticle();
        } else if(e.keyCode === 40){
            switchToNextArticle();
        }
    });
});

function switchToIndex(index){
    var element = $("#stream div:nth-child(" + (index+1) + ")");
    if(element.length === 0) return;
    $(".selected").removeClass("selected");
    element.addClass("selected");
}

function switchToPreviousArticle(){
    var selectedElement, index;
    selectedElement = $(".selected");
    index = selectedElement.index();
    switchToIndex(index-1);
}

function switchToNextArticle(){
    var selectedElement, index;
    selectedElement = $(".selected");
    index = selectedElement.index();
    switchToIndex(index+1);
}