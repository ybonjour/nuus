import database
import math

class Article:
    def __init__(self, id, title, content, feedId, updated, titleWordCount, contentWordCount, language):
        self.id = id
        self.title = title
        self.content = content
        self.feedId = feedId
        self.updated = updated
        self.titleWordCount = titleWordCount
        self.contentWordCount = contentWordCount
        self.language = language

class Similarity:
    def __init__(self, db):
        self.similarity_measures = []
        self.similarity_measures = [(self.feedSimilarity, 0.1),
                                    (self.languageSimilarity, 0.1),
                                    (self.titleSimilarity, 0.4),
                                    (self.contentSimilarity, 0.4) ]
        self.db = db
        self._numArticles = None
        
    def languageSimilarity(self, article1, article2):
        if article1.language == article2.language and article1.language != '-':
            return 1.0
        else:
            return 0

    def feedSimilarity(self, article1, article2):
        if article1.feedId == article2.feedId:
            return 1.0
        else:
            return 0.0
    
    def titleSimilarity(self, article1, article2):
        return self.textSimilarity(article1, article2, 1)
        
    def contentSimilarity(self, article1, article2):
        return self.textSimilarity(article1, article2, 0)
    
    def termWeight(self, wordId, articleId, inTitle):
        #TODO: maybe normalize termFrequency? -> Check results
        return self.termFrequency(wordId, articleId, inTitle)*self.inverseDocumentFrequency(wordId, inTitle)

    def numArticles(self):
        if self._numArticles == None:
            self._numArticles = self.db.uniqueScalarOrZero("SELECT COUNT(Id) FROM article")
        return self._numArticles
    
    def calcIDF(self, numArticles, nunDocumentsTermOccursIn):
        return math.log(1.0*(numArticles + 1) / (nunDocumentsTermOccursIn + 1))
        
    def inverseDocumentFrequency(self, wordId, inTitle):
        numDocumentsWordOccursIn = self.db.uniqueScalarOrZero("SELECT COUNT(Id) FROM word_index WHERE Word=%s AND InTitle=%s", (wordId, inTitle))
        return self.calcIDF(self.numArticles(), numDocumentsWordOccursIn)
    
    def termFrequency(self, wordId, articleId, inTitle):
        query = "SELECT Count FROM word_index WHERE Article=%s AND Word=%s AND InTitle=%s"
        return self.db.uniqueScalarOrZero(query, (articleId, wordId, inTitle))
    
    def sumSquaredWordWeight(self, articleId, inTitle):
        sumWordWeight = 0
        query = "select word, count from word_index where article=%s and InTitle=%s"
        for word in self.db.iterQuery(query, (articleId, inTitle)):
            wordId, wordCount = word
            sumWordWeight += 1.0*wordCount*math.pow(self.termWeight(wordId, articleId, inTitle), 2)
        return sumWordWeight
    
    def textSimilarity(self, article1, article2, inTitle):
        sumCommonWordWeight = 0
        queryCommon = """select w1.Word, w1.Count, w2.Count
                    from word_index as w1
                    inner join word_index as w2
                        on w1.Word = w2.Word
                            and w1.Id <> w2.Id
                            and w1.Article=%s
                            and w2.Article=%s
                            and w1.InTitle=%s
                            and w2.InTitle=%s
                    inner join word on w1.Word = word.Id"""

        for commonWord in self.db.iterQuery(queryCommon, (article1.id, article2.id, inTitle, inTitle)):
            wordId, wordCount1, wordCount2 = commonWord
            
            #The same word can occur in both textes multiple times
            #the smaller of the both values is the number of times
            #the two articles have this word in common
            wordCount = min(wordCount1, wordCount2)
            
            weightInArticle1 = self.termWeight(wordId, article1.id, inTitle)
            weightInArticle2 = self.termWeight(wordId, article2.id, inTitle)
            
            sumCommonWordWeight += wordCount*weightInArticle1*weightInArticle2

        normArticle1 = math.sqrt(self.sumSquaredWordWeight(article1.id, inTitle))
        normArticle2 = math.sqrt(self.sumSquaredWordWeight(article2.id, inTitle))
        
        #similarity = cos(alpha), alpha: angle between article1 and article2
        #cos: R -> [-1..1] -> abs(cos(x)) = [0..1]
        similarity = abs(1.0*sumCommonWordWeight/(normArticle1*normArticle2))
        return similarity
        
    def articleSimilarity(self, article1, article2):
        similarity = 0
        for similarity_function, weight in self.similarity_measures:
            similarity_component = weight*similarity_function(article1, article2)
            similarity += similarity_component
        return similarity