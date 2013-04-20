

function StreamRenderer()
{
    that = {
        render: function(container, articles){

            jQuery.get('/static/templates/listitem.html', function(template)
            {
                for(i = 0; i < articles.length; i++)
                {
                    container.append(Mustache.render(template, articles[i]));
                }

                stream().EnsureEventHandlers();
            });
        }
    };

    return that;
}