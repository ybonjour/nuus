__author__ = 'Yves Bonjour'

from Proxies import FeedProxy
from OPMLReader import OPMLReader
import uuid
import os
import sys
import ConfigParser

USAGE = "USAGE: python Service.py [config_file] [subscriptions_file]"


def create_feedimporter(feed_url):
    reader = OPMLReader()
    feed_proxy = FeedProxy(feed_url)
    return FeedImporter(reader, feed_proxy)


class FeedImporter(object):
    def __init__(self, reader, feed_proxy):
        self.reader = reader
        self.feed_proxy = feed_proxy

    def import_feeds(self, filename, user):
        feed_container = self.reader.read(filename)
        for feed in feed_container.get_feeds():
            self.feed_proxy.add_feed(feed.url, feed.title, user)


if __name__ == "__main__":
    arguments = sys.argv[1:]
    if len(arguments) != 2:
        print(USAGE)
        quit()

    config_file = arguments[0]
    subscriptions_file = arguments[1]
    if not os.path.isfile(config_file) or not os.path.isfile(subscriptions_file):
        print(USAGE)
        quit()

    config_parser = ConfigParser.RawConfigParser()
    config_parser.read(config_file)

    feed_url = config_parser.get("FeedImporter", "feed_url")

    importer = create_feedimporter(feed_url)
    importer.import_feeds(subscriptions_file, uuid.uuid4())