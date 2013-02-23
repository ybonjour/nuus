import textprocessing

class Indexer:
    def __init__(self, db):
        self.db = db
        
    def getOrCreateWord(self, word):
        #Word has a unique constraint on database,
        #-> ignore errror if it can not be inserted
        # as it then already exists and id = 0
        id = self.db.insertQuery("INSERT IGNORE INTO word (Word) VALUES(%s)", word)
        if id == 0: 
            id = self.db.uniqueScalarOrZero("SELECT Id FROM word WHERE Word=%s", word)
        return id
        
    def indexText(self, articleId, text, inTitle):
        words = textprocessing.getWordList(text)
        
        wordPosition = 1
        for word in words:
            #words with less than one character may either be punctation
            #or just a single letter
            #in either case such a word is not relevant for the index
            if len(word) <= 1: continue
            if not textprocessing.containsLetters(word): continue
            
            #TODO: stemming
            wordId = self.getOrCreateWord(word)
            
            #word_index has a unique constraint on Article, Word and InTitle
            #in the database -> increase count if entry already exists
            self.db.insertQuery("""INSERT INTO word_index
                                    (Article, Word, FirstOccurence, Count, InTitle)
                                    VALUES (%s, %s, %s, %s, %s)
                                    ON DUPLICATE KEY UPDATE Count=Count+1""",
                                    (articleId, wordId, wordPosition, 1, inTitle))
            wordPosition += 1
        
    def indexArticleTitle(self, articleId, title):
        self.indexText(articleId, title, 1)

    def indexArticleContent(self, articleId, content):
        self.indexText(articleId, content, 0)
        
    def articleAlreadyIndexed(self, articleId):
        count = self.db.uniqueScalarOrZero("SELECT COUNT(Id) FROM word_index WHERE Article=%s", articleId)
        return count > 0

    def indexArticle(self, articleId):
        if self.articleAlreadyIndexed(articleId): return
        query = "SELECT id, title, content FROM article WHERE Id=%s"
        for id, title, content in self.db.iterQuery(query, articleId):
            self.indexArticleTitle(id, title)
            self.indexArticleContent(id, content)