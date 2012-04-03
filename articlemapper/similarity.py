from math import log

class Similarity:
    def __init__(self, db):
        self.db = db
        self._numArticles = None
    
    def termWeight(self, wordId, articleId, inTitle):
        #TODO: maybe normalize termFrequency? -> Check results
        return self.termFrequency(wordId, articleId, inTitle)*self.inverseDocumentFrequency(wordId, inTitle)

    def numArticles(self):
        if self._numArticles == None:
            self._numArticles = self.db.uniqueScalarOrZero("SELECT COUNT(Id) FROM article")
        return self._numArticles
    
    def calcIDF(self, numArticles, nunDocumentsTermOccursIn):
        return log(1.0*(numArticles + 1) / (nunDocumentsTermOccursIn + 1))
        
    def inverseDocumentFrequency(self, wordId, inTitle):
        numDocumentsWordOccursIn = self.db.uniqueScalarOrZero("SELECT COUNT(Id) FROM word_index WHERE Word=%s AND InTitle=%s", (wordId, inTitle))
        return self.calcIDF(self.numArticles(), numDocumentsWordOccursIn)
    
    def termFrequency(self, wordId, articleId, inTitle):
        query = "SELECT Count FROM word_index WHERE Article=%s AND Word=%s AND InTitle=%s"
        return self.db.uniqueScalarOrZero(query, (articleId, wordId, inTitle))
    
    def l2Norm(self, vector):
        return 1.0*sum(pow(value, 2) for value in vector)
    
    def similarity(self, wordImportanceDictionary1, wordImportanceDictionary2):
        words1 = set(wordImportanceDictionary1.keys())
        words2 = set(wordImportanceDictionary2.keys())
        commonWords = words1 & words2
        
        scalarProduct = 0.0
        for commonWordId in commonWords:
            scalarProduct += wordImportanceDictionary1[commonWordId]*wordImportanceDictionary2[commonWordId]
        
        return scalarProduct / (self.l2Norm(wordImportanceDictionary1.values())*self.l2Norm(wordImportanceDictionary2.values()))

    def wordImportanceDict(self, article):
        query = "SELECT Word FROM word_index WHERE Article=%s"
        return dict((wordId, self.termWeight(wordId, article.id, 0)) for (wordId, ) in self.db.iterQuery(query, article.id))
    
    def textSimilarity(self, article1, article2, inTitle):
        return self.similarity(self.wordImportanceDict(article1), self.wordImportanceDict(article2))

    def similarityToAverage(self, article, averageWordImportance):
        return self.similarity(self.wordImportanceDict(article), averageWordImportance)
    
    def articleSimilarity(self, article1, article2):
        return self.textSimilarity(article1, article2, 0)