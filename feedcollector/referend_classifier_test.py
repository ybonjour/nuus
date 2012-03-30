import database
from reverend.thomas import Bayes

language_feed_map = {"de":[1,6], "en":[5,7]}

def remove_html_tags(data):
    #*? ensures that the next closing bracket is matched
    #and not the last possible closing bracket
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def print_statistics(language, correct, article_count):
    correct_ratio = 1.0*correct[language]/article_count[language]
    print "---------------------------"
    print language
    print "Correct: {0}".format(correct[language])
    print "Total: {0}".format(article_count[language])
    print "Correct ratio: {0}".format(correct_ratio)    

def getMostCommonWords(db, language):
    query = """SELECT word.Word FROM word_index
                INNER JOIN word ON word_index.Word=word.Id
                INNER JOIN article ON word_index.Article=article.Id
                                    AND article.Feed IN ("""
    query += ",".join([str(id) for id in language_feed_map[language]])
    query += """) GROUP BY word.Word ORDER BY COUNT(*) DESC LIMIT 20"""
    
    print query
    words = []
    for word in db.iterQuery(query):
        words.append(word[0])
    return words
    
db = database.Database()
db.connect()
try:

    guesser = Bayes()
   
    trainingWordsDe = getMostCommonWords(db, "de")
    print " ".join(trainingWordsDe)
    guesser.train("de", " ".join(trainingWordsDe))
    
    trainingWordsEn = getMostCommonWords(db, "en")
    guesser.train("en", " ".join(trainingWordsEn))

    data = []
    #German feed
    for article in db.iterQuery("SELECT content FROM article WHERE Feed=6"):
        entry = ("de", textprocessing.remove_html_tags(article[0]))
        data.append(entry)
         
    #English feed
    for article in db.iterQuery("SELECT content FROM article WHERE Feed IN (5,7)"):
        entry = ("en", textprocessing.remove_html_tags(article[0]))
        data.append(entry)

    correct = {"de":0, "en":0}
    article_count = {"de":0, "en":0}
    for item in data:
        print "------------------------------------"
        language = item[0]
        text = item[1]
        article_count[language] += 1
        
        guesses = guesser.guess(text)
        if guesses == []:
            print "no language guessed"
            continue
        guesses.sort(key=lambda guess: guess[1], reverse=True)
        guessed_language = guesses[0][0]
        
        if guessed_language == language: correct[language] += 1
        
        print "defined: {0}".format(language)
        print "guessed: {0}".format(guessed_language)
        print "text: {0}".format(text[0:20].encode("latin1", "backslashreplace"))    
        
        
        
    print_statistics("en", correct, article_count)
    print_statistics("de", correct, article_count)
    
finally:
    db.close()