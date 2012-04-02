from similarity import Similarity
from similarity import Article

class Clusterer:
    def __init__(self, similarity, db, k):
        self.similarity = similarity
        self.db = db
        self.centroids = {}
        self.k = k
    
    def createArticleFromItem(self, articleItem):
        return Article(articleItem[0], articleItem[1], articleItem[2], articleItem[3],
                                    articleItem[4], articleItem[5], articleItem[6], articleItem[7])
    
    def initializeCentroids(self):
        self.db.manipulationQuery("DELETE FROM cluster")
        while len(self.centroids) < self.k:
            query = """SELECT Id, Title, Content, Feed, Updated, TitleWordCount,
                    ContentWordCount, Language FROM article ORDER BY rand() LIMIT 1"""
            articleItem = self.db.uniqueQuery(query)
            article = self.createArticleFromItem(articleItem)
            self.centroids[article.id] = article
            self.db.insertQuery("INSERT INTO cluster (Centroid) VALUES(%s)", articleItem[0])
            
    def assignArticlesToCluster(self):
        query = """SELECT Id, Title, Content, Feed, Updated, TitleWordCount,
                    ContentWordCount, Language FROM article"""

        for articleItem in self.db.iterQuery(query):
            article = Article(articleItem[0], articleItem[1], articleItem[2], articleItem[3],
                                    articleItem[4], articleItem[5], articleItem[6], articleItem[7])
            
            maxSimilarity = 0.0
            maxCentroid = None
            for centroid in self.centroids.values():
                similarity = self.similarity.articleSimilarity(centroid, article)
                if similarity > maxSimilarity:
                    maxCentroid = centroid
                    maxSimilarity = similarity
            
            clusterId = self.db.uniqueScalarOrZero("SELECT Id FROM cluster WHERE Centroid=%s", centroid.id)
            self.db.manipulationQuery("UPDATE article SET Cluster=%s", clusterId)
    
    def getSummedSimilarity(self, clusterId, article):
        sumSimilarity = 0.0
        query = """SELECT Id, Title, Content, Feed, Updated, TitleWordCount,
                    ContentWordCount, Language FROM article WHERE Cluster=%s"""            
        for compareArticleItem in self.db.iterQuery(query, clusterId):
            if compareArticleItem[0] == article.id : continue #do not count the article itself
            compareArticle = self.createArticleFromItem(compareArticleItem)
            sumSimilarity += self.similarity.articleSimilarity(article, compareArticle)
        return sumSimilarity
    
    def determineNewCentroid(self, clusterId):
        #TODO: can be optimized by first calculating all the similarities between
        #the articles in a cluster
        
        #assume that old centroid is new centroid
        query = """SELECT article.Id, Title, Content, Feed, Updated, TitleWordCount,
                    ContentWordCount, Language FROM article
                    INNER JOIN cluster ON cluster.Centroid=article.Id AND cluster.Id=%s"""
        articleItem = self.db.uniqueQuery(query, clusterId)
        maxSumSimilarityArticle = self.createArticleFromItem(articleItem)      
        maxSumSimilarity = self.getSummedSimilarity(clusterId, maxSumSimilarityArticle)

        query = """SELECT Id, Title, Content, Feed, Updated, TitleWordCount,
                    ContentWordCount, Language FROM article WHERE Cluster=%s"""
        for articleItem in self.db.iterQuery(query, clusterId):
            print "next article"
            article = self.createArticleFromItem(articleItem)
            sumSimilarity = self.getSummedSimilarity(clusterId, article)  
            if sumSimilarity > maxSumSimilarity:
                print "update"
                maxSumSimilarity = sumSimilarity
                maxSumSimilarityArticle = article
            
        return maxSumSimilarityArticle
    
    def updateCentroids(self):
        changed = False
        for cluster in self.db.iterQuery("SELECT Id, Centroid FROM Cluster"):
            clusterId, oldCentroidId = cluster
            self.centroids.pop(oldCentroidId)
            print "determine for cluster {0}".format(clusterId)
            centroid = self.determineNewCentroid(clusterId)
            self.centroids[centroid.id] = centroid
            self.db.manipulationQuery("UPDATE cluster SET Centroid=%s WHERE Id=%s", (centroid.id, clusterId))
            changed |= (oldCentroidId != centroid.id)
        return changed 
    
    def clustering(self):
        self.initializeCentroids()
        changed = True
        while changed:
            print "next iteration"
            self.assignArticlesToCluster()
            changed = self.updateCentroids()
            