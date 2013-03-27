__author__ = 'Yves Bonjour'

from collections import namedtuple
import feedparser


Article = namedtuple("Article", "title, text")


class FeedParser(object):
    def parse(self, url):
        d = feedparser.parse(url)
        return [Article(e.title, e.summary_detail.value) for e in d.entries]