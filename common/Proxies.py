__author__ = 'Yves Bonjour'

import requests
from urlparse import urljoin
import json


class IndexProxy(object):
    def __init__(self, url):
        self.url = url

    def index(self, article_id, title, text):
        index_url = urljoin(self.url, "index/{article}".format(article=article_id))
        payload = {"title": title, "text": text}

        try:
            r = requests.post(index_url, data=payload)
        except requests.ConnectionError as e:
            raise EnvironmentError(e)

        if r.status_code != 200:
            raise EnvironmentError(r.content)


class ClusterProxy(object):
    def __init__(self, url):
        self.url = url

    def add_article(self, article_id):
        add_article_url = urljoin(self.url, "add/{article}".format(article=article_id))

        try:
            r = requests.post(add_article_url)
        except requests.ConnectionError as e:
            raise EnvironmentError(e)

        if r.status_code != 200:
            raise EnvironmentError(r.content)


class FeedProxy(object):
    def __init__(self, url):
        self.url = url

    def add_feed(self, feed_url, name, user):
        add_feed_url = urljoin(self.url, "add")
        payload = {"url": feed_url, "name": name, "user": user}

        try:
            r = requests.post(add_feed_url, data=payload)
        except requests.ConnectionError as e:
            raise EnvironmentError(e)

        if r.status_code != 200:
            raise EnvironmentError(r.content)

    def get_feed_urls(self):
        get_feed_url = urljoin(self.url, "feed_urls")

        try:
            r = requests.get(get_feed_url)
        except requests.ConnectionError as e:
            raise EnvironmentError(e)

        return json.loads(r.content)

class ArticleProxy(object):
    def __init__(self, url):
        self.url = url

    def add_article(self, title, text, updated_on, feed):
        add_feed_url = urljoin(self.url, "add")
        payload = {"title": title, "text": text, "updated_on": updated_on, "feed": feed}
        try:
            r = requests.post(add_feed_url, data=payload)
        except requests.ConnectionError as e:
            raise EnvironmentError(e)

        if r.status_code != 200:
            raise EnvironmentError(r.content)

        d = json.loads(r.content)
        if "status" not in d or d["status"] != "ok" or "id" not in d:
            raise EnvironmentError(r.content)

        return d["id"]

