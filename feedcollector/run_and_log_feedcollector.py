from timeit import Timer
import datetime
import feedcollector

def run():
    feedCollector = feedcollector.Feedcollector()
    feedCollector.collect()

if __name__ == '__main__':
    log = open('log/collector.log', 'a')
    try:
        now = str(datetime.datetime.now())
        log.write("--------------------------------\n")
        log.write("Started: {0}\n".format(now))

        t = Timer('run()', "from __main__ import run")    
        time = t.timeit(number=1)
        
        log.write("Time used: {0}\n".format(time))
    finally:
        log.close()

