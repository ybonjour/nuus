from similarity import Similarity
from similarity import Article
import database

def testTwoArticles(articleId1, articleId2):
    db = database.Database()
    db.connect()
    try:
        s = Similarity(db)

        query = """SELECT Id, Title, Content, Feed, Updated, TitleWordCount,
                            ContentWordCount, Language FROM article WHERE Id IN (%s, %s)"""
        
        articles = []
        for article in db.iterQuery(query, (articleId1, articleId2)):
            articles.append(Article(article[0], article[1], article[2], article[3],
                                    article[4], article[5], article[6], article[7]))

        
        s.articleSimilarity(articles[0], articles[1])
    finally:
        db.close()

def testAllArticles():
    db = database.Database()
    db.connect()
    try:
        s = Similarity(db)
        articles =[]
        query = """SELECT Id, Title, Content, Feed, Updated, TitleWordCount,
                    ContentWordCount, Language FROM article"""

        for article in db.iterQuery(query):
            articles.append(Article(article[0], article[1], article[2], article[3],
                                    article[4], article[5], article[6], article[7]))
        
        maxSimilarity = 0.0
        minSimilarity = 1.0
        sumSimilarity = 0.0
        articleCount = 0
        for article1 in articles:
            for article2 in articles:
                if article1.id <= article2.id: continue
                similarity = s.articleSimilarity(article1, article2)
                sumSimilarity += similarity
                articleCount += 1
                maxSimilarity = max(maxSimilarity, similarity)
                minSimilarity = min(minSimilarity, similarity)
        print "Average similarity {0}".format(sumSimilarity/articleCount)
        print "Max similarity {1}".format(maxSimilarity)
        print "Min similarity {1}".format(minSimilarity)
    finally:
        db.close()

        
#testTwoArticles(2932, 2925)
testAllArticles()

