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
        db.manipulationQuery("""INSERT INTO word_index
                                (Article, Word, Position, InTitle)
                                VALUES (%s, %s, %s, %s)""", (articleId, wordId, wordPosition, inTitle))
        wordPosition += 1
    
    return wordPosition
    
def indexArticleTitle(db, articleId, title):
    return indexText(db, articleId, title, 1)
  
def articleAlreadyIndexed(db, articleId):
    count = db.uniqueScalarOrZero("SELECT COUNT(Id) FROM article WHERE Id=%s AND TitleWordCount IS NOT NULL", articleId)
    return count != 0
    
def indexArticleContent(db, articleId, content):
    return indexText(db, articleId, content, 0)

def indexArticle(db, articleId):
    if articleAlreadyIndexed(db, articleId): return 

    query = "SELECT id, title, content FROM article WHERE Id=%s"
    for article in db.iterQuery(query, articleId):
        num_words_title = indexArticleTitle(db, articleId, article[1])
        num_words_content = indexArticleContent(db, articleId, article[2])
        update_query = "UPDATE article SET TitleWordCount=%s, ContentWordCount=%s WHERE Id=%s"
        db.manipulationQuery(update_query, (num_words_title, num_words_content, articleId))