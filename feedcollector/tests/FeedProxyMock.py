__author__ = 'Yves Bonjour'

from Mock import Mock


class FeedProxyMock(Mock):
    def set_feed_urls(self, urls):
        self.feed_urls = urls

    def get_feed_urls(self):
        self._handle_method_call("get_feed_urls")
        return self.feed_urls
