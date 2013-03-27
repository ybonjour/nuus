__author__ = 'Yves Bonjour'

import unittest
from FeedProxyMock import FeedProxyMock
from FeedParserMock import FeedParserMock
from Mock import Mock
from FeedCollector import FeedCollector
from FeedParser import Article


class FeedCollectorTest(unittest.TestCase):
    def setUp(self):
        self.feed_mock = FeedProxyMock()
        self.index_mock = Mock()
        self.cluster_mock = Mock()
        self.parser_mock = FeedParserMock()
        self.feed_collector = FeedCollector(self.feed_mock, self.index_mock, self.cluster_mock, self.parser_mock)

    def test_collect_no_url(self):
        # Arrange
        self.feed_mock.set_feed_urls([])
        self.parser_mock.set_articles([])

        # Act
        self.feed_collector.collect()

        # Assert
        self.assertEquals(1, self.feed_mock.num_method_calls("get_feed_urls"))
        self.assertEquals(0, self.parser_mock.num_method_calls("parse"))
        self.assertEquals(0, self.index_mock.num_method_calls("index"))
        self.assertEquals(0, self.cluster_mock.num_method_calls("add_article"))

    def test_collect_one_url_no_article(self):
        # Arrange
        url = "http://www.nuus.ch"
        self.feed_mock.set_feed_urls([url])
        self.parser_mock.set_articles({url: []})

        # Act
        self.feed_collector.collect()

        # Assert
        self.assertEquals(1, self.feed_mock.num_method_calls("get_feed_urls"))

        self.assertEquals(1, self.parser_mock.num_method_calls("parse"))
        parse_args = self.parser_mock.get_arguments("parse")
        self.assertEquals(url, parse_args[0])

        self.assertEquals(0, self.index_mock.num_method_calls("index"))
        self.assertEquals(0, self.cluster_mock.num_method_calls("add_article"))

    def test_collect_one_url_one_article(self):
        # Arrange
        article = Article("foo", "bar")
        url = "http://www.nuus.ch"
        self.feed_mock.set_feed_urls([url])
        self.parser_mock.set_articles({url: [article]})

        # Act
        self.feed_collector.collect()

        # Assert
        self.assertEquals(1, self.feed_mock.num_method_calls("get_feed_urls"))

        self.assertEquals(1, self.parser_mock.num_method_calls("parse"))
        parse_args = self.parser_mock.get_arguments("parse")
        self.assertEquals(url, parse_args[0])

        self.assertEquals(1, self.index_mock.num_method_calls("index"))
        index_args = self.index_mock.get_arguments("index")
        self.assertEquals(article.title, index_args[1])
        self.assertEquals(article.text, index_args[2])

        self.assertEquals(1, self.cluster_mock.num_method_calls("add_article"))
        add_article_args = self.cluster_mock.get_arguments("add_article")
        self.assertEquals(index_args[0], add_article_args[0])

    def test_collect_one_url_two_articles(self):
        # Arrange
        article1 = Article("foo", "bar")
        article2 = Article("foo2", "bar2")
        url = "http://www.nuus.ch"
        self.feed_mock.set_feed_urls([url])
        self.parser_mock.set_articles({url: [article1, article2]})

        # Act
        self.feed_collector.collect()

        # Assert
        self.assertEquals(1, self.feed_mock.num_method_calls("get_feed_urls"))

        self.assertEquals(1, self.parser_mock.num_method_calls("parse"))
        parse_args = self.parser_mock.get_arguments("parse")
        self.assertEquals(url, parse_args[0])

        self.assertEquals(2, self.index_mock.num_method_calls("index"))
        index_args1 = self.index_mock.get_arguments("index", 1)
        self.assertEquals(article1.title, index_args1[1])
        self.assertEquals(article1.text, index_args1[2])

        index_args2 = self.index_mock.get_arguments("index", 2)
        self.assertEquals(article2.title, index_args2[1])
        self.assertEquals(article2.text, index_args2[2])

        self.assertEquals(2, self.cluster_mock.num_method_calls("add_article"))
        add_article_args1 = self.cluster_mock.get_arguments("add_article", 1)
        self.assertEquals(index_args1[0], add_article_args1[0])

        add_article_args2 = self.cluster_mock.get_arguments("add_article", 2)
        self.assertEquals(index_args2[0], add_article_args2[0])

    def test_collect_two_urls_one_article_each(self):
        # Arrange
        article1 = Article("foo", "bar")
        article2 = Article("foo2", "bar2")
        url1 = "http://www.nuus.ch"
        url2 = "http://code.nuus.ch"
        self.feed_mock.set_feed_urls([url1, url2])
        self.parser_mock.set_articles({url1: [article1], url2: [article2]})

        # Act
        self.feed_collector.collect()

        # Assert
        self.assertEquals(1, self.feed_mock.num_method_calls("get_feed_urls"))

        self.assertEquals(2, self.parser_mock.num_method_calls("parse"))
        parse_args1 = self.parser_mock.get_arguments("parse", 1)
        self.assertEquals(url1, parse_args1[0])

        parse_args2 = self.parser_mock.get_arguments("parse", 2)
        self.assertEquals(url2, parse_args2[0])

        self.assertEquals(2, self.index_mock.num_method_calls("index"))
        index_args1 = self.index_mock.get_arguments("index", 1)
        self.assertEquals(article1.title, index_args1[1])
        self.assertEquals(article1.text, index_args1[2])

        index_args2 = self.index_mock.get_arguments("index", 2)
        self.assertEquals(article2.title, index_args2[1])
        self.assertEquals(article2.text, index_args2[2])

        self.assertEquals(2, self.cluster_mock.num_method_calls("add_article"))
        add_article_args1 = self.cluster_mock.get_arguments("add_article", 1)
        self.assertEquals(index_args1[0], add_article_args1[0])

        add_article_args2 = self.cluster_mock.get_arguments("add_article", 2)
        self.assertEquals(index_args2[0], add_article_args2[0])


if __name__ == '__main__':
    unittest.main()
