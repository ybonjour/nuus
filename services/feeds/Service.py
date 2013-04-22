__author__ = 'Yves Bonjour'

import sys
import os
import ConfigParser
from Feeds import Feed
from Feeds import create_feeds
from WerkzeugService import WerkzeugService
from WerkzeugService import create_status_error_response
from WerkzeugService import create_status_ok_response
from WerkzeugService import create_json_response
from werkzeug.routing import Map, Rule
import uuid

USAGE = "USAGE: python Service.py [config_file]"

def create_feed_service(host, port, debug, redis_host, redis_port):
    feeds = create_feeds(redis_host, redis_port)
    return FeedService(feeds, host, port, debug)

class FeedService(WerkzeugService):
    def __init__(self, feeds, host, port, debug):
        super(FeedService, self).__init__(host, port, Map([
            Rule('/add', endpoint='add'),
            Rule('/feed_urls', endpoint='feed_urls')
            ]), debug=debug)

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
    arguments = sys.argv[1:]
    if len(arguments) != 1:
        print(USAGE)
        quit()

    config_file = arguments[0]
    if not os.path.isfile(config_file):
        print(USAGE)
        quit()

    config_parser = ConfigParser.RawConfigParser()
    config_parser.read(config_file)

    host = config_parser.get("FeedService", "host")
    port = config_parser.getint("FeedService", "port")
    debug = config_parser.getboolean("FeedService", "debug")
    redis_host = config_parser.get("FeedService", "redis_host")
    redis_port = config_parser.getint("FeedService", "redis_port")

    service = create_feed_service(host, port, debug, redis_host, redis_port)
    service.run()