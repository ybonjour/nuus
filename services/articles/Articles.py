__author__ = 'Yves Bonjour'

import couchdb

def article_to_dict(article):
    d = {
        "title": article.title,
        "text": article.text,
        "updated_on": article.updated_on,
        "feed": article.feed
    }
    if article.identifier: d["id"] = article.identifier
    return d

class Article(object):
    def __init__(self, title, text, updated_on, feed, identifier=None):
        self.title = title
        self.text = text
        self.updated_on = updated_on
        self.feed = feed
        self.identifier = identifier

def create_articles():
    store = CouchDBArticleStore("localhost", 5984, "nuus_articles")
    return Articles(store)

class Articles(object):
    def __init__(self, store):
        self.store = store

    def add_article(self, article):
        return self.store.save_article(article)

    def get_articles(self):
        return self.store.get_all_articles()


class CouchDBArticleStore(object):
    def __init__(self, server, port, database):
        url = "http://{server}:{port}/".format(server=server, port=port)
        couch = couchdb.Server(url)
        self.db = couch[database]

    def get_all_articles(self):
        articles = []
        for id in self.db:
            doc = self.db[id]
            articles.append(Article(doc["title"], doc["text"], doc["updated_on"], doc["feed"], id))
        return articles

    def save_article(self, article):
        d = article_to_dict(article)
        doc_id, _ = self.db.save(d)
        return doc_id