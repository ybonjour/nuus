__author__ = 'Yves Bonjour'

from Mock import Mock


class TokenizerMock(Mock):
    def set_tokens(self, tokens):
        self.tokens = tokens

    def tokenize(self, text):
        self._handle_method_call("tokenize", (text,))
        return self.tokens