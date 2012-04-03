from similarity import Similarity
from random import choice
from collections import namedtuple

Article = namedtuple('Article', ('id',
                          'title',
                          'content',
                          'feed',
                          'updated',
                          'titleWordCount',
                          'contentWordCount',
                          'language'))

class Clusterer:
    def __init__(self, similarity, db, k):
        self.similarity = similarity
        self.db = db
        self.centroids = {}
        self.k = k
        
    def initializeCentroids(self):
        self.db.manipulationQuery("UPDATE article SET cluster=NULL")
        self.db.manipulationQuery("DELETE FROM cluster")
        while len(self.centroids) < self.k:
            query = """SELECT Id, Title, Content, Feed, Updated, TitleWordCount,
                    ContentWordCount, Language FROM article ORDER BY rand() LIMIT 1"""
            article = Article._make(self.db.uniqueQuery(query))
            if article.id in self.centroids.keys(): continue
            self.centroids[article.id] = article
            self.db.insertQuery("INSERT INTO cluster (Centroid) VALUES(%s)", article.id)
            
    def assignArticlesToCluster(self):
        query = """SELECT Id, Title, Content, Feed, Updated, TitleWordCount,
                    ContentWordCount, Language FROM article"""

        for articleItem in self.db.iterQuery(query):
            maxSimilarity = 0.0
            maxCentroid = None
            for centroid in self.centroids.values():
                similarity = self.similarity.articleSimilarity(centroid, article)
                print "article {0} for centroid {1} has similarity {2}".format(article.id, centroid.id, similarity)
                if similarity > maxSimilarity:
                    maxCentroid = centroid
                    maxSimilarity = similarity
            
            #if no centroid can be chosen, just select one randomly
            if maxCentroid == None:
                maxCentroid = choice(self.centroids.values())
            
            clusterId = self.db.uniqueScalarOrZero("SELECT Id FROM cluster WHERE Centroid=%s", maxCentroid.id)
            self.db.manipulationQuery("UPDATE article SET Cluster=%s WHERE Id=%s", (clusterId, article.id))
            print "assignend article {0} to cluster {1}({2}), with similarity {3}".format(article.id, clusterId, maxCentroid.id, maxSimilarity)
    
    def determineNewCentroid(self, clusterId):
        numArticles = self.similarity.numArticles() #TODO: move numArticles
        query = """SELECT Word, sum(word_index.Count) FROM word_index
                    WHERE Article IN (SELECT Id FROM article WHERE Cluster=%s)
                    GROUP BY Word"""
        averageWordImportance = dict((word, sum/numArticles) for word, sum in self.db.iterQuery(query, clusterId))
        
        #article in cluster with minimal distance to average
        articleQuery = """SELECT Id, Title, Content, Feed, Updated, TitleWordCount,
                    ContentWordCount, Language FROM article WHERE Cluster=%s"""
        return min((Article._make(row) for row in self.db.iterQuery(articleQuery, clusterId)),
                    key=lambda article: self.similarity.similarityToAverage(article, averageWordImportance))

    def updateCentroids(self):
        changed = False
        for clusterId, oldCentroidId in self.db.iterQuery("SELECT Id, Centroid FROM cluster"):
            self.centroids.pop(oldCentroidId)
            print "determine for cluster {0}".format(clusterId)
            centroid = self.determineNewCentroid(clusterId)
            self.centroids[centroid.id] = centroid
            self.db.manipulationQuery("UPDATE cluster SET Centroid=%s WHERE Id=%s", (centroid.id, clusterId))
            changed |= (oldCentroidId != centroid.id)
        return changed 
    
    def clustering(self):
        self.initializeCentroids()
        print "centroids:"
        for centroid in self.centroids.values():
            print "Article {0}, Feed{1}".format(centroid.id, centroid.feedId)
        
        changed = True
        while changed:
            print "next iteration"
            self.assignArticlesToCluster()
            changed = self.updateCentroids()
            