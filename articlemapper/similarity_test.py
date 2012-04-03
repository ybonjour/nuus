from similarity import Similarity
from clustering import Article
import database

def testTwoArticles(articleId1, articleId2):
    db = database.Database()
    db.connect()
    try:
        s = Similarity(db)

        query = """SELECT Id, Title, Content, Feed, Updated, TitleWordCount,
                            ContentWordCount, Language FROM article WHERE Id IN (%s, %s)"""
        
        articles = [Article._make(articleItem) for articleItem in db.iterQuery(query, (articleId1, articleId2))]       
        s.articleSimilarity(articles[0], articles[1])
    finally:
        db.close()

def testAllArticles():
    db = database.Database()
    db.connect()
    try:
        s = Similarity(db)
        
        query = """SELECT Id, Title, Content, Feed, Updated, TitleWordCount,
                    ContentWordCount, Language FROM article"""
        
        articles =[Article._make(articleItem) for articleItem in db.iterquerQuery(query)]
        
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
        print "Max similarity {0}".format(maxSimilarity)
        print "Min similarity {0}".format(minSimilarity)
    finally:
        db.close()

        
#testTwoArticles(2932, 2925)
testAllArticles()

