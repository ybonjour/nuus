import time
import database
import feedparser
import bayesian_classifier
import indexer

classifier = bayesian_classifier.Classifier()
classifier.load("language_detection")
print classifier.data

def existsArticle(db, article, feedId):
    count = db.uniqueScalarOrZero("""SELECT COUNT(id) FROM article
                  WHERE title=%s AND Feed=%s AND Updated=%s""",
                  (article.title, feedId,
                  time.strftime("%Y-%m-%d %H:%M:%S", article.updated_parsed)))
    return count > 0

def createArticle(db, article, feedId):
    return db.insertQuery("""INSERT INTO article
                        (Title, Content, Feed, Updated)
                        VALUES(%s, %s, %s, %s)""",
                        (article.title,
                         article.summary_detail.value, feedId,
                         time.strftime("%Y-%m-%d %H:%M:%S",
                                       article.updated_parsed)))
    

def determineLanguage(db, articleId):
    article = db.uniqueQuery("SELECT Content FROM article WHERE Id=%s", articleId)
    language = classifier.guessCategory(article[0])
    if language == bayesian_classifier.Classifier.UNKNOWN_CATEGORY: language = "-"
    db.manipulationQuery("UPDATE article SET language=%s WHERE Id=%s", (language, articleId)) 
                                             
def handleArticle(db, article, feedId):
    if existsArticle(db, article, feedId):
        return
    print "."
    id = createArticle(db, article, feedId)
    determineLanguage(db, id)
    indexer.indexArticle(db, id)
    
db = database.Database()
db.connect()
try:
    for feed in db.iterQuery("SELECT id, url FROM feed"):    
        d = feedparser.parse(feed[1])
        db.manipulationQuery("""UPDATE feed
                                SET Title=%s
                                WHERE Id=%s""", (d.feed.title, feed[0]))
        for article in d.entries:
            handleArticle(db, article, feed[0])
    db.commit()
finally:
    db.close()