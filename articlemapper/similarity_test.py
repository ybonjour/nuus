from similarity import Similarity
from clustering import Article
from database import Database
import sys

def testTwoArticles(articleId1, articleId2):
    db = Database()
    db.connect()
    try:
        s = Similarity(db)
        
        query = "SELECT Id, Title, Content, Feed, Updated, Language FROM article WHERE Id=%s"
        
        #query twice in order to be able to compare the identical article
        article1 = Article._make(db.uniqueQuery(query, articleId1))
        article2 = Article._make(db.uniqueQuery(query, articleId2))
        
        print s.articleSimilarity(article1, article2)
    finally:
        db.close()

def testAllArticles():
    db = Database()
    db.connect()
    try:
        s = Similarity(db)
        
        query = "SELECT Id, Title, Content, Feed, Updated, Language FROM article"
        
        articles =[Article._make(articleItem) for articleItem in db.iterQuery(query)]
        
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

#first command line argument is python_script
if len(sys.argv) == 3:
    testTwoArticles(sys.argv[1], sys.argv[2])
else:
    testAllArticles()