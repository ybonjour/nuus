__author__ = 'Yves Bonjour'

import requests
import uuid

class IndexerProxy(object):
    def __init__(self, url):
        self.url = url

    def index(self, article_id, title, text):
        index_url = self.url + "index/" + str(article_id)
        payload = {"title": title, "text": text}

        try:
            r = requests.post(index_url, data=payload)
        except requests.ConnectionError as e:
            raise EnvironmentError(e)

        if r.status_code != 200:
            raise EnvironmentError(r.content)

class ClustererProxy(object):
    def __init__(self, url):
        self.url = url

    def add_article(self, article_id):
        add_article_url = self.url + "add/" + str(article_id)

        try:
            r = requests.post(add_article_url)
        except requests.ConnectionError as e:
            raise EnvironmentError(e)

        if r.status_code != 200:
            raise EnvironmentError(r.content)


if __name__ == "__main__":
    article_id = uuid.uuid4()
    title = "Where did it go wrong for oligarch?"
    text = "Boris Berezovsky was an oligarch who made a fortune as the Soviet Union collapsed. But by the time he died, he was in financial difficulties."

    indexer_proxy = IndexerProxy("http://localhost:5000/")
    indexer_proxy.index(article_id, title, text)

    clusterer_proxy = ClustererProxy("http://localhost:5001/")
    clusterer_proxy.add_article(article_id)