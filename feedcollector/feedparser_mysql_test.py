import time
import database
import feedparser

def existsArticle(db, article, feedId):
    count = db.countQuery("""SELECT id FROM article
                  WHERE title=%s AND Feed=%s AND Updated=%s""",
                  (article.title, feedId,
                  time.strftime("%Y-%m-%d %H:%M:%S", article.updated_parsed)))
    return count > 0

def handleArticle(db, article, feedId):
    if existsArticle(db, article, feedId):
        return
    
    db.manipulationQuery("""INSERT INTO article
                        (Title, Content, Feed, Updated)
                        VALUES(%s, %s, %s, %s)""",
                        (article.title,
                         article.summary_detail.value, feedId,
                         time.strftime("%Y-%m-%d %H:%M:%S",
                                       article.updated_parsed)))

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
