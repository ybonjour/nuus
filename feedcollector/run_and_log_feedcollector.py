from timeit import Timer
import datetime
import feedcollector
import database

def run():
    feedCollector = feedcollector.Feedcollector()
    feedCollector.collect()

def getCounts():
    db = database.Database()
    db.connect()
    try:
        article_count = db.uniqueScalarOrZero("SELECT COUNT(Id) FROM article")
        word_count = db.uniqueScalarOrZero("SELECT COUNT(Id) FROM word")
        index_count = db.uniqueScalarOrZero("SELECT COUNT(Id) FROM word_index")
        return (article_count, word_count, index_count)
    finally:
        db.close()
            
if __name__ == '__main__':
    log = open('log/collector.log', 'a')
    try:
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
    finally:
        log.close()

