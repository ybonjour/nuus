import database
import bayesian_classifier

filename = 'language_detection'

def trainWithAllArticles(db):
    classifier = bayesian_classifier.Classifier()
    for article in db.iterQuery("SELECT content, language FROM article"):
        classifier.trainText(article[0], article[1])
    classifier.save(filename)

    
def testGuesses(db):
    classifier = bayesian_classifier.Classifier()
    classifier.load(filename)
    successes = 0
    unknown = 0
    total = 0
    for article in db.iterQuery("SELECT content, language FROM article WHERE Id IN (1398, 1449)"):
        content = article[0]
        language = article[1]
        guessed = classifier.guessCategory(content)
        if guessed == bayesian_classifier.Classifier.UNKNOWN_CATEGORY: unknown += 1
        if guessed == language: successes += 1
        total += 1
        print "guessed: {0}".format(guessed)
        print "real: {0}".format(language)
    
    print "Total: {0}".format(total)
    print "Unknnown {0}".format(unknown)
    print "Successes: {0}".format(successes)
    print "Fails: {0}".format(total-successes+unknown)
    print "Ratio: {0}".format(1.0*successes / total)


db = database.Database()
db.connect()
try:
    #trainWithAllArticles(db)
    testGuesses(db)
finally:
    db.close()
