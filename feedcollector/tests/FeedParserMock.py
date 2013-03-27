__author__ = 'Yves Bonjour'

from Mock import Mock

class FeedParserMock(Mock):
    def set_articles(self, articles):
        self.articles = articles

    def parse(self, url):
        self._handle_method_call("parse", (url,))
        return self.articles[url]

