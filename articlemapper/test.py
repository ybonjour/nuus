from similarity import Similarity
from clustering import Article
from database import Database

db = Database()
db.connect()
try:
    similarity = Similarity(db)
    article = Article._make(db.uniqueQuery("SELECT Id, Title, content, Feed, Updated, Language FROM article WHERE Id=%s", 8))
    print similarity.wordImportanceDict(article)
    
    
finally:
    db.close()