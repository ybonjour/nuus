// This is a manifest file that'll be compiled into including all the files listed below.
// Add new JavaScript/Coffee code in separate files in this directory and they'll automatically
// be included in the compiled file accessible from http://example.com/assets/application.js
// It's not advisable to add code directly here, but if you do, it'll appear at the bottom of the
// the compiled file.
//
//= require jquery
//= require jquery_ujs
//= require_tree .

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