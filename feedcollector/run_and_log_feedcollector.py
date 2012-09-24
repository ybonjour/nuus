from timeit import Timer
import datetime
from feedcollector import Feedcollector
from database import Database
from bayesian_classifier import Classifier
from indexer import Indexer

def run():
    db = Database()
    db.connect()
    try:
        classifier = Classifier()
        classifier.load("language_detection")
        indexer = Indexer(db)
        feedCollector = Feedcollector(db, classifier, indexer)
        feedCollector.collect()
        db.commit()
    finally:
        db.close()

def getCounts():
    db = Database()
    db.connect()
    try:
        article_count = db.uniqueScalarOrZero("SELECT COUNT(Id) FROM article")
        word_count = db.uniqueScalarOrZero("SELECT COUNT(Id) FROM word")
        index_count = db.uniqueScalarOrZero("SELECT COUNT(Id) FROM word_index")
        return (article_count, word_count, index_count)
    finally:
        db.close()
            
if __name__ == '__main__':
    with open('log/collector.log', 'a') as log:
        now = str(datetime.datetime.now())
        log.write("--------------------------------\n")
        log.write("Started: {0}\n".format(now))

        count_before = getCounts() 

        t = Timer('run()', "from __main__ import run")    
        time = t.timeit(number=1)
        
        count_after = getCounts()        
        log.write("Time used: {0}\n".format(time))
        log.write("Added {0} articles, {1} words, {2} indices\n".format(count_after[0]-count_before[0],
                                                                     count_after[1]-count_before[1],
                                                                     count_after[2]-count_before[2]))