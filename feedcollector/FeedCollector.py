__author__ = 'Yves Bonjour'

import uuid
from Proxies import IndexProxy
from Proxies import ClusterProxy
from Proxies import FeedProxy
from FeedParser import FeedParser


def create_feed_collector():
    index_proxy = IndexProxy("http://localhost:5000")
    cluster_proxy = ClusterProxy("http://localhost:5001")
    feed_proxy = FeedProxy("http://localhost:5002")
    parser = FeedParser()
    return FeedCollector(feed_proxy, index_proxy, cluster_proxy, parser)


class FeedCollector(object):

    def __init__(self, feed_proxy, indexer_proxy, cluster_proxy, parser):
        self.feed_proxy = feed_proxy
        self.indexer_proxy = indexer_proxy
        self.cluster_proxy = cluster_proxy
        self.parser = parser

    def collect(self):
        for url in self.feed_proxy.get_feed_urls():
            for article in self.parser.parse(url):
                self._handle_article(article)

    def _handle_article(self, article):
        # TODO: include article service to safe article and get article_id
        article_id = uuid.uuid4()
        self.indexer_proxy.index(article_id, article.title, article.text)
        self.cluster_proxy.add_article(article_id)