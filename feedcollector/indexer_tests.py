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