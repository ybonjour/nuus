$(document).ready(function(){

    $.get('/streams.json', function(data) {

        $("#stream > *").remove();

        $.each(data, function(key, article) {
           var element = $('<div class="streamArticle">' + article.title + '</div>');
           element.appendTo("#stream");
           element.data('content', article.content);
        });

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

});

function switchToIndex(index){
    var element = $("#stream div:nth-child(" + (index+1) + ")");
    if(element.length === 0) return;
    $(".selected").removeClass("selected");
    element.addClass("selected");

    $('#article').html(element.data('content'));
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