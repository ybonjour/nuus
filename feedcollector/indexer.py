import database
import textprocessing

def wordExists(db, word):
    query = "SELECT Id FROM word WHERE Word=%s"
    count = db.countQuery(query, word)
    if count > 1: raise Exception
    return count > 0

def getOrCreateWord(db, word):
    if not wordExists(db, word):
        db.manipulationQuery("""INSERT INTO word (Word) VALUES(%s)""", word)
    
    row = db.uniqueQuery("SELECT Id FROM word WHERE Word=%s", word)
    id = row[0]
    if id < 0: raise Exception
    return id
    
def indexText(db, articleId, text, inTitle):
    words = textprocessing.get_word_list(text)
    
    wordPosition = 1
    for word in words:
        #words with less than one character may either be punctation
        #or just a single letter
        #in either case such a word is not relevant for the index
        if len(word) <= 1: continue
        
        #TODO: stemming
        
        wordId = getOrCreateWord(db, word)
        db.manipulationQuery("""INSERT INTO word_index
                                (Article, Word, Position, InTitle)
                                VALUES (%s, %s, %s, %s)""", (articleId, wordId, wordPosition, inTitle))
        wordPosition += 1
    
    return wordPosition
    
def index_article_title(db, articleId, title):
    return indexText(db, articleId, title, 1)
  
def article_already_indexed(db, articleId):
    count = db.countQuery("SELECT Id FROM article WHERE Id=%s AND TitleWordCount IS NOT NULL", articleId)
    return count != 0
    
def index_article_content(db, articleId, content):
    return indexText(db, articleId, content, 0)

def index_article(db, articleId):
    if article_already_indexed(db, articleId): return 

    query = "SELECT id, title, content FROM article WHERE Id=%s"
    for article in db.iterQuery(query, articleId):
        num_words_title = index_article_title(db, articleId, article[1])
        num_words_content = index_article_content(db, articleId, article[2])
        update_query = "UPDATE article SET TitleWordCount=%s, ContentWordCount=%s WHERE Id=%s"
        db.manipulationQuery(update_query, (num_words_title, num_words_content, articleId))