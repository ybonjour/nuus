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
    
    def distanceToVector(self, article, averageWordImportanceDict):
        return self.distance(self.wordImportanceDict(article), averageWordImportanceDict)
    
    def similarity(self, wordImportanceDictionary1, wordImportanceDictionary2):
        words1 = set(wordImportanceDictionary1.keys())
        words2 = set(wordImportanceDictionary2.keys())
        commonWords = words1 & words2
        
        scalarProduct = 0.0
        for commonWordId in commonWords:
            scalarProduct += wordImportanceDictionary1[commonWordId]*wordImportanceDictionary2[commonWordId]
        
        return float(scalarProduct) / (self.l2Norm(wordImportanceDictionary1.values())*self.l2Norm(wordImportanceDictionary2.values()))

    def similarityToVector(self, article, wordImportanceDict):
        return self.similarity(self.wordImportanceDict(article), wordImportanceDict)
        
    def wordImportanceDict(self, article):
        query = "SELECT Word FROM word_index WHERE Article=%s"
        return dict((wordId, self.termWeight(wordId, article.id)) for (wordId, ) in self.db.iterQuery(query, article.id))
    
    def articleSimilarity(self, article1, article2):
        return self.similarity(self.wordImportanceDict(article1), self.wordImportanceDict(article2))