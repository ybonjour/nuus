from similarity import Similarity
from clustering import Article
from database import Database
import sys

def testTwoArticles(articleId1, articleId2):
    db = Database()
    db.connect()
    try:
        s = Similarity(db)        
        print s.articleSimilarity(articleId1, articleId2)
    finally:
        db.close()

def testAllArticles():
    db = Database()
    db.connect()
    try:
        s = Similarity(db)        
        maxSimilarity = 0.0
        minSimilarity = 1.0
        sumSimilarity = 0.0
        articleCount = 0
        for (articleId1,) in db.iterQuery("SELECT Id FROM article"):
            for (articleId2,) in db.iterQuery("SELECT Id FROM article"):
                if articleId1 <= articleId2: continue
                similarity = s.articleSimilarity(articleId1, articleId2)
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