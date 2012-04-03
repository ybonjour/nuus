import database
import textprocessing

def getOrCreateWord(db, word):
    #Word has a unique constraint on database,
    #-> ignore errror if it can not be inserted
    # as it then already exists and id = 0
    id = db.insertQuery("INSERT IGNORE INTO word (Word) VALUES(%s)", word)
    if id == 0: 
        id = db.uniqueScalarOrZero("SELECT Id FROM word WHERE Word=%s", word)
    return id
    
def indexText(db, articleId, text, inTitle):
    words = textprocessing.getWordList(text)
    
    wordPosition = 1
    for word in words:
        #words with less than one character may either be punctation
        #or just a single letter
        #in either case such a word is not relevant for the index
        if len(word) <= 1: continue
        if not textprocessing.containsLetters(word): continue
        
        #TODO: stemming
        wordId = getOrCreateWord(db, word)
        
        #word_index has a unique constraint on Article, Word and InTitle
        #in the database -> increase count if entry already exists
        db.insertQuery("""INSERT INTO word_index
                                (Article, Word, FirstOccurence, Count, InTitle)
                                VALUES (%s, %s, %s, %s, %s)
                                ON DUPLICATE KEY UPDATE Count=Count+1""",
                                (articleId, wordId, wordPosition, 1, inTitle))
        wordPosition += 1
    
def indexArticleTitle(db, articleId, title):
    indexText(db, articleId, title, 1)

def indexArticleContent(db, articleId, content):
    indexText(db, articleId, content, 0)
    
def articleAlreadyIndexed(db, articleId):
    count = db.uniqueScalarOrZero("SELECT COUNT(Id) FROM word_index WHERE Article=%s", articleId)
    return count > 0

def indexArticle(db, articleId):
    if articleAlreadyIndexed(db, articleId): return
    query = "SELECT id, title, content FROM article WHERE Id=%s"
    for id, title, content in db.iterQuery(query, articleId):
        indexArticleTitle(db, id, title)
        indexArticleContent(db, id, content)