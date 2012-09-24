from time import strftime
import feedparser
from bayesian_classifier import Classifier

class Feedcollector:
    def __init__(self, db, classifier, indexer):
        self.db = db
        self.classifier = classifier
        self.indexer = indexer

    def existsArticle(self, article, feedId):
        count = self.db.uniqueScalarOrZero("""SELECT COUNT(id) FROM article
                      WHERE title=%s AND Feed=%s AND Updated=%s""",
                      (article.title, feedId,
                      strftime("%Y-%m-%d %H:%M:%S", article.updated_parsed)))
        return count > 0

    def createArticle(self, article, feedId):
        return self.db.insertQuery("""INSERT INTO article
                            (Title, Content, Feed, Updated)
                            VALUES(%s, %s, %s, %s)""",
                            (article.title,
                             article.summary_detail.value, feedId,
                             strftime("%Y-%m-%d %H:%M:%S",
                                           article.updated_parsed)))

    def determineLanguage(self, articleId):
        (content, ) = self.db.uniqueQuery("SELECT Content FROM article WHERE Id=%s", articleId)
        language = self.classifier.guessCategory(content)
        if language == Classifier.UNKNOWN_CATEGORY: language = "-"
        self.db.manipulationQuery("UPDATE article SET language=%s WHERE Id=%s", (language, articleId)) 
                                                 
    def handleArticle(self, article, feedId):
        if self.existsArticle(article, feedId): return
        id = self.createArticle(article, feedId)
        self.determineLanguage(id)
        self.indexer.indexArticle(id)

    def collect(self):
        for id, url in self.db.iterQuery("SELECT id, url FROM feed"):    
            d = feedparser.parse(url)
            query = "UPDATE feed SET Title=%s WHERE Id=%s"
            self.db.manipulationQuery(query, (d.feed.title, id))
            for article in d.entries:
                self.handleArticle(article, id)