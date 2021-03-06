__author__ = 'Yves Bonjour'

from Proxies import IndexProxy
from Proxies import ClusterProxy
from Proxies import FeedProxy
from Proxies import ArticleProxy
from NuusFeedParser import FeedParser


def create_feed_collector(index_url, cluster_url, feed_url, article_url):
    index_proxy = IndexProxy(index_url)
    cluster_proxy = ClusterProxy(cluster_url)
    feed_proxy = FeedProxy(feed_url)
    article_proxy = ArticleProxy(article_url)
    parser = FeedParser()
    return FeedCollector(article_proxy, feed_proxy, index_proxy, cluster_proxy, parser)


class FeedCollector(object):

    def __init__(self, article_proxy, feed_proxy, indexer_proxy, cluster_proxy, parser):
        self.feed_proxy = feed_proxy
        self.indexer_proxy = indexer_proxy
        self.cluster_proxy = cluster_proxy
        self.article_proxy = article_proxy
        self.parser = parser

    def collect(self):
        for url in self.feed_proxy.get_feed_urls():
            try:
                for article in self.parser.parse(url):
                    self._handle_article(article, url)
            except EnvironmentError as e:
                print("Environment error with url {url}.".format(url=url))
                continue
            except AttributeError:
                print("Unknown error")
                continue

            print("Catched feeds from {url}".format(url=url))

    def _handle_article(self, article, feed_url):
        article_id = self.article_proxy.add_article(article.title, article.text, article.updated_on, feed_url)
        self.indexer_proxy.index(article_id, article.title, article.text)
        self.cluster_proxy.add_article(article_id)