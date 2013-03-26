__author__ = 'Yves Bonjour'

from Mock import Mock


class FeedStoreMock(Mock):
    def set_feed_urls(self, feed_urls):
        self.feed_urls = feed_urls

    def get_feed_urls(self):
        self._handle_method_call("get_feed_urls")
        return self.feed_urls