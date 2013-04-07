__author__ = 'Yves Bonjour'

from Proxies import FeedProxy
from OPMLReader import OPMLReader
import uuid

def create_feedimporter():
    reader = OPMLReader()
    feed_proxy = FeedProxy("http://localhost:5002")
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
    importer = create_feedimporter()
    importer.import_feeds("subscriptions.xml", uuid.uuid4())