var articles;
articles = [
    {
        'id': '1',
        'title': "test test",
        'source': "fuckingbreakingnews.com",
        'updated_on': "2 hours ago",
        'summary': "zusammenfassung dsaf asfds fsfdsf dsf",
        'content': "das ist der inhalt bla bla bla"
    },
    {
        'id': '2',
        'title': "bla bla bla",
        'source': "anothergoodnews.com",
        'updated_on': "3 hours ago",
        'summary': "dsaf asfds fsfdsf dsf sdf sdf dsfds dsff",
        'content': "tets est est est estse testres testests testetsts"
    },
    {
        'id': '3',
        'title': "bla bla bla",
        'source': "anothergoodnews.com",
        'updated_on': "3 hours ago",
        'summary': "dsaf asfds fsfdsf dsf sdf sdf dsfds dsff",
        'content': "tets est est est estse testres testests testetsts"
    },
    {
        'id': '4',
        'title': "bla bla bla",
        'source': "anothergoodnews.com",
        'updated_on': "3 hours ago",
        'summary': "dsaf asfds fsfdsf dsf sdf sdf dsfds dsff",
        'content': "tets est est est estse testres testests testetsts"
    }
];

function stream()
{
    function getCurrent()
    {
        return $('div.stream_list_item.active');
    }

    function setInactive(element)
    {
        $(element.attr('data-target')).hide(200);
        element.removeClass('active');
    }

    function setActive(element)
    {
        $(element.attr('data-target')).show(200);
        element.addClass('active')
    }

    var keyboardHandlers = {
        // down
        40: function () {
            var current = getCurrent();
            if(!current.length) return;

            var next = current.next('div.stream_list_item');
            if(!next.length) return;

            setInactive(current);
            setActive(next);
        },
        // up
        38: function () {
            var current = getCurrent();
            if(!current.length) return;

            var previous = current.prev('div.stream_list_item');
            if(!previous.length) return;

            setInactive(current);
            setActive(previous);
        }
    };

    var ViewStates = {
        OVERWIEW: 1,
        READING: 2
    }

    var viewState = ViewStates.OVERWIEW;

    return {

        Init: function () {
            StreamRenderer().render($('#stream_container'), articles);

            this.EnsureEventHandlers();
        },

        EnsureEventHandlers: function () {
            $('div[data-toggle="nuus_summary"]')
                .off('hover')
                .hover(
                function () {
                    var current = getCurrent();
                    setInactive(current);
                    setActive($(this))
                },
                function () {
                    setInactive($(this))
                }
            );

            $(document)
                .off('keydown')
                .keydown(function (e) {
                    keyboardHandlers[e.keyCode](e);
                });

            $('div.stream_list_item a')
                .off('click')
                .click(function () {
                    if(viewState === ViewStates.OVERWIEW)
                    {
                        viewState = ViewStates.READING;
                        $('#article_container').show(50);
                        $('#stream_container').animate({
                                marginLeft: "-=300",
                                fontSize: "-=3px"}
                            , 250)
                            .removeClass('stream_large', 2000)
                            .removeClass('span7', 2000)
                            .addClass('span4', 2000)
                            .addClass('stream_small', 2000);
                    }
                });
            }
    };
}

        $(document).ready(function () {

            stream().Init();

        });
