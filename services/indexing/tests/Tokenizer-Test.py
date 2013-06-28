__author__ = 'parallels'

import unittest
from TokenizerMock import TokenizerMock
from Tokenizer import LowerCaseTokenizer


class LowerCaseTokenizerTest(unittest.TestCase):

    def setUp(self):
        self.tokenizer_mock = TokenizerMock()
        self.tokenizer = LowerCaseTokenizer(self.tokenizer_mock)

    def test_tokenize(self):
        # Arrange
        tokens = ["Foo", "bar", "FOO"]
        text = " ".join(tokens)
        self.tokenizer_mock.set_tokens(tokens)

        # Act
        tokens = self.tokenizer.tokenize(text)

        # Assert
        self.assertEqual(1, self.tokenizer_mock.num_method_calls("tokenize"))
        arguments = self.tokenizer_mock.get_arguments("tokenize")
        self.assertEqual(text, arguments[0])

        self.assertEqual("foo", tokens[0])
        self.assertEqual("bar", tokens[1])
        self.assertEqual("foo", tokens[2])

if __name__ == '__main__':
    unittest.main()
