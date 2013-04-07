__author__ = 'Yves Bonjour'

import unittest
from FeedProxyMock import FeedProxyMock
from FeedParserMock import FeedParserMock
from ArticleProxyMock import ArticleProxyMock
from Mock import Mock
from FeedCollector import FeedCollector
from NuusFeedParser import Article
import datetime


class FeedCollectorTest(unittest.TestCase):
    def setUp(self):
        self.article_mock = ArticleProxyMock()
        self.feed_mock = FeedProxyMock()
        self.index_mock = Mock()
        self.cluster_mock = Mock()
        self.parser_mock = FeedParserMock()
        self.feed_collector = FeedCollector(self.article_mock, self.feed_mock, self.index_mock, self.cluster_mock, self.parser_mock)

    def test_collect_no_url(self):
        # Arrange
        self.feed_mock.set_feed_urls([])
        self.parser_mock.set_articles([])

        # Act
        self.feed_collector.collect()

        # Assert
        self.assertEquals(1, self.feed_mock.num_method_calls("get_feed_urls"))
        self.assertEquals(0, self.parser_mock.num_method_calls("parse"))
        self.assertEquals(0, self.article_mock.num_method_calls("add_article"))
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

        self.assertEquals(0, self.article_mock.num_method_calls("add_article"))
        self.assertEquals(0, self.index_mock.num_method_calls("index"))
        self.assertEquals(0, self.cluster_mock.num_method_calls("add_article"))

    def test_collect_one_url_one_article(self):
        # Arrange
        updated_on = datetime.date.today()
        article = Article("foo", "bar", updated_on)
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

        self.assertEqual(1, self.article_mock.num_method_calls("add_article"))
        article_args = self.article_mock.get_arguments("add_article")
        self.assertEqual("foo", article_args[0])
        self.assertEqual("bar", article_args[1])
        self.assertEqual(updated_on, article_args[2])
        self.assertEqual(url, article_args[3])

        self.assertEquals(1, self.index_mock.num_method_calls("index"))
        index_args = self.index_mock.get_arguments("index")
        self.assertEquals(article.title, index_args[1])
        self.assertEquals(article.text, index_args[2])

        self.assertEquals(1, self.cluster_mock.num_method_calls("add_article"))
        add_article_args = self.cluster_mock.get_arguments("add_article")
        self.assertEquals(index_args[0], add_article_args[0])

    def test_collect_one_url_two_articles(self):
        # Arrange
        updated_on_1 = datetime.date.today()
        updated_on_2 = datetime.date(2010, 1, 1)
        article1 = Article("foo", "bar", updated_on_1)
        article2 = Article("foo2", "bar2", updated_on_2)
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

        self.assertEquals(2, self.article_mock.num_method_calls("add_article"))
        article_args1 = self.article_mock.get_arguments("add_article", 1)
        self.assertEqual("foo", article_args1[0])
        self.assertEqual("bar", article_args1[1])
        self.assertEqual(updated_on_1, article_args1[2])
        self.assertEqual(url, article_args1[3])

        article_args2 = self.article_mock.get_arguments("add_article", 2)
        self.assertEqual("foo2", article_args2[0])
        self.assertEqual("bar2", article_args2[1])
        self.assertEqual(updated_on_2, article_args2[2])
        self.assertEqual(url, article_args2[3])

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
        updated_on_1 = datetime.date.today()
        updated_on_2 = datetime.date(2010, 1, 1)
        article1 = Article("foo", "bar", updated_on_1)
        article2 = Article("foo2", "bar2", updated_on_2)
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

        self.assertEquals(2, self.article_mock.num_method_calls("add_article"))
        article_args1 = self.article_mock.get_arguments("add_article", 1)
        self.assertEqual("foo", article_args1[0])
        self.assertEqual("bar", article_args1[1])
        self.assertEqual(updated_on_1, article_args1[2])
        self.assertEqual(url1, article_args1[3])

        article_args2 = self.article_mock.get_arguments("add_article", 2)
        self.assertEqual("foo2", article_args2[0])
        self.assertEqual("bar2", article_args2[1])
        self.assertEqual(updated_on_2, article_args2[2])
        self.assertEqual(url2, article_args2[3])

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
