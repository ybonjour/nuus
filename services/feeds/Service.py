__author__ = 'Yves Bonjour'

from Feeds import Feed
from Feeds import create_feeds
from WerkzeugService import WerkzeugService
from WerkzeugService import create_status_error_response
from WerkzeugService import create_status_ok_response
from WerkzeugService import create_json_response
from werkzeug.routing import Map, Rule
import uuid

def create_feed_service():
    return FeedService(create_feeds())

class FeedService(WerkzeugService):
    def __init__(self, feeds):
        super(FeedService, self).__init__("localhost", 5002, Map([
            Rule('/add', endpoint='add'),
            Rule('/feed_urls', endpoint='feed_urls')
            ]))

        self.feeds = feeds

    def on_add(self, request):
        if request.method != "POST":
            return create_status_error_response("Request must be POST", status=400)

        if "url" not in request.form or "name" not in request.form or "user" not in request.form:
            return create_status_error_response("Request must have the url, name and user", status=400)

        feed = Feed(request.form["url"], request.form["name"])
        user_id = uuid.UUID(request.form["user"])

        try:
            self.feeds.add_feed(feed, user_id)
        except Exception as e:
            return create_status_error_response(str(e))

        return create_status_ok_response()

    def on_feed_urls(self, _):
        urls = self.feeds.get_feed_urls()
        return create_json_response(list(urls))

if __name__ == "__main__":
    service = create_feed_service()
    service.run()