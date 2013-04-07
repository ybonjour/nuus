__author__ = 'Yves Bonjour'

from Mock import Mock

class ArticleProxyMock(Mock):
    def set_id(self, identifier):
        self.identifier = identifier

    def add_article(self, title, text, updated_on, feed):
        self._handle_method_call("add_article", (title, text, updated_on, feed))
        return self.identifier