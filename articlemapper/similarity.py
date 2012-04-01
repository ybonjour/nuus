import database

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
    def __init__(self):
        self.similarity_measures = []
        self.similarity_measures = [(self.feedSimilarity, 0.3),
                                    (self.languageSimilarity, 0.3),
                                    (self.titleSimilarity, 0.2),
                                    (self.contentSimilarity, 0.2) ]
        self.db = database.Database()
        
    def languageSimilarity(self, article1, article2):
        if article1.language == article2.language and article1.language != '-':
            return 1.0
        else:
            return 0

    def feedSimilarity(self, article1, article2):2 
        if article1.feedId == article2.feedId:
            return 1.0
        else:
            return 0.0

    def textSimilarity(self, article1, article2, inTitle):
        #Build a 1 to 1 mapping between words from article1 and words
        #words from article2 if they are equal.
        #e.g. if article1 contains twice the word 'the'
        #and article2 contains the word 'the' once
        #then this is counted as 1 common word.

        query = """select w1.Count, w2.Count
                    from word_index as w1
                    inner join word_index as w2
                        on w1.Word = w2.Word
                            and w1.Id <> w2.Id
                            and w1.Article=%s
                            and w2.Article=%s
                            and w1.InTitle=%s
                            and w2.InTitle=%s
                    inner join word on w1.Word = word.Id"""
            
        numCommonWords = 0
        for commonWord in self.db.iterQuery(query, (article1.id, article2.id, inTitle, inTitle)):
            numCommonWords += min(commonWord[0], commonWord[1])
                
        numWordsArticle1 = (article1.titleWordCount if inTitle else article1.contentWordCount)
        numWordsArticle2 = (article2.titleWordCount if inTitle else article2.contentWordCount)
        #the maximum amount of words that could be mapped is the number of words in the smaller text
        numTotalWords = min(numWordsArticle1, numWordsArticle2)

        return 1.0*numCommonWords / numTotalWords
        
    def titleSimilarity(self, article1, article2):
        return self.textSimilarity(article1, article2, 1)
        
    def contentSimilarity(self, article1, article2):
        return self.textSimilarity(article1, article2, 0)
    
    def articleSimilarity(self, article1, article2):
        similarity = 0
        for similarity_function, weight in self.similarity_measures:
            print "similarity comp: {0}".format(weight*similarity_function(article1, article2))
            similarity += weight*similarity_function(article1, article2)
        
        return similarity
        
    def run(self):
        self.db.connect()
        try:
            articles =[]
            query = """SELECT Id, Title, Content, Feed, Updated, TitleWordCount,
                        ContentWordCount, Language FROM article"""

            for article in self.db.iterQuery(query):
                articles.append(Article(article[0], article[1], article[2], article[3],
                                        article[4], article[5], article[6], article[7]))
                                        
            for article1 in articles:
                for article2 in articles:
                    if article1.id <= article2.id: continue
                    print self.articleSimilarity(article1, article2)
        finally:
            self.db.close()