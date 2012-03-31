import time
import database
import feedparser
import bayesian_classifier
import indexer

class Feedcollector:
    def __init__(self):
        self.classifier = bayesian_classifier.Classifier()
        self.classifier.load("language_detection")
        self.db = database.Database()

    def existsArticle(self, article, feedId):
        count = self.db.uniqueScalarOrZero("""SELECT COUNT(id) FROM article
                      WHERE title=%s AND Feed=%s AND Updated=%s""",
                      (article.title, feedId,
                      time.strftime("%Y-%m-%d %H:%M:%S", article.updated_parsed)))
        return count > 0

    def createArticle(self, article, feedId):
        return self.db.insertQuery("""INSERT INTO article
                            (Title, Content, Feed, Updated)
                            VALUES(%s, %s, %s, %s)""",
                            (article.title,
                             article.summary_detail.value, feedId,
                             time.strftime("%Y-%m-%d %H:%M:%S",
                                           article.updated_parsed)))
        

    def determineLanguage(self, articleId):
        article = self.db.uniqueQuery("SELECT Content FROM article WHERE Id=%s", articleId)
        language = self.classifier.guessCategory(article[0])
        if language == bayesian_classifier.Classifier.UNKNOWN_CATEGORY: language = "-"
        self.db.manipulationQuery("UPDATE article SET language=%s WHERE Id=%s", (language, articleId)) 
                                                 
    def handleArticle(self, article, feedId):
        if self.existsArticle(article, feedId):
            return
        id = self.createArticle(article, feedId)
        self.determineLanguage(id)
        indexer.indexArticle(self.db, id)

    def collect(self):
        self.db.connect()
        try:
            for feed in self.db.iterQuery("SELECT id, url FROM feed"):    
                d = feedparser.parse(feed[1])
                self.db.manipulationQuery("""UPDATE feed
                                        SET Title=%s
                                        WHERE Id=%s""", (d.feed.title, feed[0]))
                for article in d.entries:
                    self.handleArticle(article, feed[0])
            self.db.commit()
        finally:
            self.db.close()