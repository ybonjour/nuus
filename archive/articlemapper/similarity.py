from math import log
from math import sqrt

class Similarity:
    def __init__(self, db):
        self.db = db
        self._numArticles = None
    
    def termWeight(self, wordId, articleId):
        #TODO: maybe normalize termFrequency? -> Check results
        return self.termFrequency(wordId, articleId)*self.inverseDocumentFrequency(wordId)

    def numArticles(self):
        if self._numArticles == None:
            self._numArticles = self.db.uniqueScalarOrZero("SELECT COUNT(Id) FROM article")
        return self._numArticles
    
    def calcIDF(self, numArticles, nunDocumentsTermOccursIn):
        return log(float(numArticles + 1) / (nunDocumentsTermOccursIn + 1))
        
    def inverseDocumentFrequency(self, wordId):
        numDocumentsWordOccursIn = self.db.uniqueScalarOrZero("SELECT COUNT(Id) FROM word_index WHERE Word=%s", wordId)
        return self.calcIDF(self.numArticles(), numDocumentsWordOccursIn)
    
    def termFrequency(self, wordId, articleId):
        query = "SELECT Count FROM word_index WHERE Article=%s AND Word=%s"
        return self.db.uniqueScalarOrZero(query, (articleId, wordId))
    
    def l2Norm(self, vector):
        return sqrt(float(sum(pow(value, 2) for value in vector)))
    
    def distance(self, wordImportanceDict1, wordImportanceDict2):
        unionWordSet = set(wordImportanceDict1.keys()) | set(wordImportanceDict2.keys())
        difference = dict((wordId, wordImportanceDict1.get(wordId, 0)-wordImportanceDict2.get(wordId, 0)) for wordId in unionWordSet)
        return self.l2Norm(difference)
    
    def distanceToVector(self, articleId, averageWordImportanceDict):
        return self.distance(self.wordImportanceDict(articleId), averageWordImportanceDict)
    
    def similarity(self, wordImportanceDictionary1, wordImportanceDictionary2):
        words1 = set(wordImportanceDictionary1.keys())
        words2 = set(wordImportanceDictionary2.keys())
        commonWords = words1 & words2
        
        scalarProduct = 0.0
        for commonWordId in commonWords:
            scalarProduct += wordImportanceDictionary1[commonWordId]*wordImportanceDictionary2[commonWordId]
        
        return float(scalarProduct) / (self.l2Norm(wordImportanceDictionary1.values())*self.l2Norm(wordImportanceDictionary2.values()))

    def clusterSimilarity(self, articleIds1, articleIds2):
        return self.similarity(self.averageWordImportanceDict(articleIds1), self.averageWordImportanceDict(articleIds2))
        
    def similarityToVector(self, articleId, wordImportanceDict):
        return self.similarity(self.wordImportanceDict(articleId), wordImportanceDict)
        
    def wordImportanceDict(self, articleId):
        query = "SELECT Word FROM word_index WHERE Article=%s"
        return dict((wordId, self.termWeight(wordId, articleId)) for (wordId, ) in self.db.iterQuery(query, articleId))
    
    def articleSimilarity(self, articleId1, articleId2):
        return self.similarity(self.wordImportanceDict(articleId1), self.wordImportanceDict(articleId2))
        
    def averageWordImportanceDict(self, articleIds):
        averageWordImportance = {}
        for article in articleIds:
            for word, importance in self.wordImportanceDict(article).items():
                averageWordImportance[word] = averageWordImportance.get(word, 0) + float(importance)/len(articleIds)
        return averageWordImportance