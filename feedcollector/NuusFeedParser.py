__author__ = 'Yves Bonjour'

from collections import namedtuple
import feedparser

Article = namedtuple("Article", "title, text, updated_on")


class FeedParser(object):
    def parse(self, url):
        d = feedparser.parse(url)
        return [Article(e.title, e.summary_detail.value, e.updated_parsed) for e in d.entries if hasattr(e, "summary_detail")]