from random import randint

class KMeansClusterer:
    def __init__(self, similarity, db, k):
        self.similarity = similarity
        self.db = db
        self.centroids = []
        self.k = k
        self.articles = {}
        
    def initializeCentroids(self):
        self.db.manipulationQuery("UPDATE article SET cluster=NULL")
        self.db.manipulationQuery("DELETE FROM cluster")
        while len(self.centroids) < self.k:
            min = self.db.uniqueScalarOrZero("SELECT MIN(Id) FROM article")
            max = self.db.uniqueScalarOrZero("SELECT MAX(Id) FROM article")
            id = randint(min, max)       
            
            articleId = self.db.uniqueScalarOrZero("SELECT Id FROM article WHERE Id=%s", id)
            if articleId == 0 or articleId in self.centroids: continue
            
            self.centroids.append(articleId)
            self.db.insertQuery("INSERT INTO cluster (Centroid) VALUES(%s)", articleId)
            
    def assignArticlesToCluster(self):
        query = "SELECT Id, Title, Content, Feed, Updated, Language FROM article"
        for (articleId,) in self.db.iterQuery("SELECT Id FROM article"):
            bestCentroid = max(self.centroids, key=lambda centroid: self.similarity.articleSimilarity(centroid, articleId))
            
            if articleId in self.centroids:
                print "Got a centroid {0}, assigned to {1}: {2}".format(articleId, bestCentroid, self.similarity.articleSimilarity(bestCentroid, articleId))
            
            clusterId = self.db.uniqueScalarOrZero("SELECT Id FROM cluster WHERE Centroid=%s", bestCentroid)
            self.db.manipulationQuery("UPDATE article SET Cluster=%s WHERE Id=%s", (clusterId, articleId))
    
    def determineNewCentroid(self, clusterId):
        numArticlesInCluster = self.db.uniqueScalarOrZero("SELECT COUNT(Id) FROM article WHERE Cluster=%s", clusterId)
        
        averageWordImportance = {}
        
        for (articleId,) in self.db.iterQuery("SELECT Id FROM article WHERE Cluster=%s", clusterId):
            for word, importance in self.similarity.wordImportanceDict(articleId).items():
                averageWordImportance[word] = averageWordImportance.get(word, 0) + (float(importance)/numArticlesInCluster)
                
        return max((id for (id,) in self.db.iterQuery("SELECT Id FROM article WHERE Cluster=%s", clusterId)),
                    key=lambda articleId: self.similarity.similarityToVector(articleId, averageWordImportance))
            

    def updateCentroids(self):
        changed = False
        for clusterId, oldCentroid in self.db.iterQuery("SELECT Id, Centroid FROM cluster"):
            self.centroids.remove(oldCentroid)
            centroid = self.determineNewCentroid(clusterId)
            self.centroids.append(centroid)
            self.db.manipulationQuery("UPDATE cluster SET Centroid=%s WHERE Id=%s", (centroid, clusterId))
            if oldCentroid != centroid: print "centroid changed from {0} to {1}".format(oldCentroid, centroid)
            changed |= (oldCentroid != centroid)
        return changed 
    
    def clustering(self):
        self.initializeCentroids() 
        print "centroids:"
        for centroid in self.centroids:
            print "Article {0}".format(centroid)
        
        changed = True
        while changed:
            print "next iteration"
            self.assignArticlesToCluster()
            changed = self.updateCentroids()

class HierarchicalClusterer:
    def __init__(self, similarity, db, threshold=1.0):
        self.db=db
        self.similarity=similarity
        self.clusters = {}
        self.threshold = threshold
    
    def initializeClusters(self):
        for (articleId,) in self.db.iterQuery("SELECT Id FROM article"):
            self.clusters[articleId] = [articleId]
    
    def mergeClusters(self, clusterId1, clusterId2):
        self.clusters[clusterId1].extend(self.clusters[clusterId2])
        self.clusters[clusterId2] = []
    
    def nonEmptyClusters(self):
        return filter(lambda (id, cluster): cluster != [], self.clusters.items())
    
    def saveClusters(self):
        print len(self.nonEmptyClusters())
        self.db.manipulationQuery("UPDATE article SET Cluster=NULL")
        self.db.manipulationQuery("DELETE FROM cluster")
        for id, cluster in self.nonEmptyClusters():
            clusterId = self.db.insertQuery("INSERT INTO cluster (Centroid) VALUES(%s)", id)
            format_strings = ','.join(['%s']*len(cluster))
            updateQuery = "UPDATE article SET Cluster=%s WHERE Id IN ({0})".format(format_strings)
            self.db.manipulationQuery(updateQuery, (clusterId,)+tuple(cluster))
    
    def clustering(self):
        self.initializeClusters()
        
        merged = True
        while merged:
            merged = False
            maxSimilarity = 0
            maxSimilarClusterIds = None
            for (clusterId1,cluster1) in self.nonEmptyClusters():
                for (clusterId2,cluster2) in self.nonEmptyClusters():
                    if clusterId1 >= clusterId2: continue
                    similarity = self.similarity.clusterSimilarity(cluster1, cluster2)
                    if similarity > maxSimilarity:
                        maxSimilarity = similarity
                        maxSimilarClusterIds = (clusterId1, clusterId2)
            
            if maxSimilarClusterIds != None and maxSimilarity > self.threshold:
                print "merge clusters {0} and {1}".format(maxSimilarClusterIds[0], maxSimilarClusterIds[1])
                self.mergeClusters(maxSimilarClusterIds[0], maxSimilarClusterIds[1])
                merged = True
        print "Save clusters"
        self.saveClusters()
        print "Finished"
        
    def clustering_old(self):
        self.initializeClusters()
        
        oldLen = len(self.nonEmptyClusters()) + 1
        merged = True
        while merged and len(self.nonEmptyClusters()) > 1:
            merged = False
            print [item[0] for item in self.nonEmptyClusters()]
            oldLen = len(self.nonEmptyClusters())
            for (id, _) in self.nonEmptyClusters():
                cluster = self.clusters[id]
                if self.clusters[id] == []: continue #might be empty if it was merged before
                mostSimilarId, mostSimilarCluster = max(filter(lambda item: item[0] != id, self.nonEmptyClusters()),
                                              key=lambda item: self.clusterSimilarity(item[1], cluster))
                
                if self.clusterSimilarity(cluster, mostSimilarCluster) > self.threshold:
                    self.mergeClusters(id, mostSimilarId)
                    merged = True
        self.saveClusters()

class GMMClusterer:
    def __init__(self, k):
        self.k = k
        self.centroids = []

    def initializeParameters(self):
        while len(self.centroids) < self.k:
            self.centroids.append((2, 5))

    def assignToCentroids(self):