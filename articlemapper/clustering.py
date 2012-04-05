from similarity import Similarity
from random import randint
from random import choice
from collections import namedtuple

Article = namedtuple('Article', ('id',
                          'title',
                          'content',
                          'feedId',
                          'updated',
                          'language'))

class Clusterer:
    def __init__(self, similarity, db, k):
        self.similarity = similarity
        self.db = db
        self.centroids = {}
        self.k = k
        self.articles = {}
        
    def initializeCentroids(self):
        self.db.manipulationQuery("UPDATE article SET cluster=NULL")
        self.db.manipulationQuery("DELETE FROM cluster")
        while len(self.centroids) < self.k:
            min = self.db.uniqueScalarOrZero("SELECT MIN(Id) FROM article")
            max = self.db.uniqueScalarOrZero("SELECT MAX(Id) FROM article")
            id = randint(min, max)
            
            count = self.db.uniqueScalarOrZero("SELECT COUNT(Id) FROM article WHERE Id=%s", id)
            if count == 0: continue            
            
            query = "SELECT Id, Title, Content, Feed, Updated, Language FROM article WHERE Id=%s"
            article = Article._make(self.db.uniqueQuery(query, id))
            if article.id in self.centroids.keys(): continue
            self.centroids[article.id] = article
            self.db.insertQuery("INSERT INTO cluster (Centroid) VALUES(%s)", article.id)
            
    def assignArticlesToCluster(self):
        query = "SELECT Id, Title, Content, Feed, Updated, Language FROM article"
        for article in (Article._make(articleItem) for articleItem in self.db.iterQuery(query)):
            bestCentroid = max(self.centroids.values(), key=lambda centroid: self.similarity.articleSimilarity(centroid, article))
            
            if article.id in self.centroids:
                print "Got a centroid {0}, assigned to {1}: {2}".format(article.id, bestCentroid.id, self.similarity.articleSimilarity(bestCentroid, article))
            
            clusterId = self.db.uniqueScalarOrZero("SELECT Id FROM cluster WHERE Centroid=%s", bestCentroid.id)
            self.db.manipulationQuery("UPDATE article SET Cluster=%s WHERE Id=%s", (clusterId, article.id))
            self.db.manipulationQuery("UPDATE article SET Cluster=%s WHERE Id=%s", (clusterId, article.id))
    
    def getArticle(self, articleId):
        if not article in self.articles:
            query = "SELECT Id, Title, content, Feed, Updated, Language FROM article WHERE Id=%s"
            articleItem = self.db.uniqueQuery(query, articleId)
            self.articles[articleId] = Article._make(articleItem)
        return self.articles[articleId]
    
    def determineNewCentroid(self, clusterId):
        numArticlesInCluster = self.db.uniqueScalarOrZero("SELECT COUNT(Id) FROM article WHERE Cluster=%s", clusterId)
        
        averageWordImportance = {}
        query = "SELECT Id, Title, Content, Feed, Updated, Language FROM article WHERE Cluster=%s"
        for article in (Article._make(articleItem) for articleItem in self.db.iterQuery(query, clusterId)):
            for word, importance in self.similarity.wordImportanceDict(article).items():
                averageWordImportance[word] = averageWordImportance.get(word, 0) + (float(importance)/numArticlesInCluster)
        
        #print averageWordImportance
        
        #article in cluster with minimal distance to average
        return max((Article._make(articleItem) for articleItem in self.db.iterQuery(query, clusterId)),
                    key=lambda article: self.similarity.similarityToVector(article, averageWordImportance))
        # return min((Article._make(articleItem) for articleItem in self.db.iterQuery(query, clusterId)),
            # key=lambda article: self.similarity.distanceToVector(article, averageWordImportance))
            

    def updateCentroids(self):
        changed = False
        for clusterId, oldCentroidId in self.db.iterQuery("SELECT Id, Centroid FROM cluster"):
            oldCentroid = self.centroids.pop(oldCentroidId)
            centroid = self.determineNewCentroid(clusterId)
            self.centroids[centroid.id] = centroid
            self.db.manipulationQuery("UPDATE cluster SET Centroid=%s WHERE Id=%s", (centroid.id, clusterId))
            if oldCentroidId != centroid.id: print "centroid changed from {0} to {1}".format(oldCentroidId, centroid.id)
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

            
class HierarchicalClusterer:
    def __init__(self, similarity, db, threshold=0.1):
        self.db=db
        self.similarity=similarity
        self.clusters = {}
        self.threshold = threshold
    
    def initializeClusters(self):
        for article in (Article._make(articleItem) for articleItem in self.db.iterQuery("SELECT Id, Title, Content, Feed, Updated, Language FROM article")):
            self.clusters[article.id] = [article]
    
    def mergeClusters(self, clusterId1, clusterId2):
        self.clusters[clusterId1].extend(self.clusters[clusterId2])
        self.clusters[clusterId2] = []
    
    def clusterSimilarity(self, cluster1, cluster2):
        averageWordImportance1 = {}
        for article in cluster1:
            for word, importance in self.similarity.wordImportanceDict(article).items():
                averageWordImportance1[word] = averageWordImportance1.get(word, 0) + float(importance)/len(cluster1)
        
        averageWordImportance2 = {}
        for article in cluster2:
            for word, importance in self.similarity.wordImportanceDict(article).items():
                averageWordImportance2[word] = averageWordImportance2.get(word, 0) + float(importance)/len(cluster2)
                
        return self.similarity.similarity(averageWordImportance1, averageWordImportance2)           
    
    def nonEmptyClusters(self):
        return filter(lambda item: item[1] != [], self.clusters.items())
    
    def saveClusters(self):
        print len(self.nonEmptyClusters())
        self.db.manipulationQuery("UPDATE article SET Cluster=NULL")
        self.db.manipulationQuery("DELETE FROM cluster")
        for id, cluster in self.nonEmptyClusters():
            print "Identification: {0}".format(id)
            clusterId = self.db.insertQuery("INSERT INTO cluster (Centroid) VALUES(%s)", id)
            if clusterId == 0: print "ERRROR"
            self.db.manipulationQuery("UPDATE article SET Cluster=%s WHERE Id IN (%s)", (clusterId, ",".join(str(article.id) for article in cluster)))
    
    def clustering(self):
        self.initializeClusters()
        
        oldLen = len(self.nonEmptyClusters()) + 1
        
        while len(self.nonEmptyClusters()) != oldLen:
            print [item[0] for item in self.nonEmptyClusters()]
            oldLen = len(self.nonEmptyClusters())
            for (id, _) in self.nonEmptyClusters():
                cluster = self.clusters[id]
                if self.clusters[id] == []: continue #might be empty if it was merged before
                mostSimilarId, mostSimilarCluster = max(filter(lambda item: item[0] != id, self.nonEmptyClusters()),
                                              key=lambda item: self.clusterSimilarity(item[1], cluster))
                
                if self.clusterSimilarity(cluster, mostSimilarCluster) > self.threshold:
                    print "merge {0} and {1}".format(id, mostSimilarId)
                    self.mergeClusters(id, mostSimilarId)
        self.saveClusters()