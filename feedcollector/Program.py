__author__ = 'Yves Bonjour'

from FeedCollector import  create_feed_collector
import time

if __name__ == "__main__":
    feed_collector = create_feed_collector()
    while True:
        feed_collector.collect()
        time.sleep(600)
