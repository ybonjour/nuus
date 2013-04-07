__author__ = 'Yves Bonjour'

import uuid
from Proxies import IndexProxy
from Proxies import ClusterProxy
from Proxies import FeedProxy
from Proxies import ArticleProxy
from NuusFeedParser import FeedParser
import datetime


def create_feed_collector():
    index_proxy = IndexProxy("http://localhost:5000")
    cluster_proxy = ClusterProxy("http://localhost:5001")
    feed_proxy = FeedProxy("http://localhost:5002")
    article_proxy = ArticleProxy("http://localhost:5003")
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

if __name__ == "__main__":
    collector = create_feed_collector()
    collector.collect()