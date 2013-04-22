__author__ = 'Yves Bonjour'

from FeedCollector import create_feed_collector
import time
import sys
import os
import ConfigParser

USAGE = "USAGE: python Service.py [config_file]"

if __name__ == "__main__":
    arguments = sys.argv[1:]
    if len(arguments) != 1:
        print(USAGE)
        quit()

    config_file = arguments[0]
    if not os.path.isfile(config_file):
        print(USAGE)
        quit()

    config_parser = ConfigParser.RawConfigParser()
    config_parser.read(config_file)

    wait_time = config_parser.getint("FeedCollector", "wait")
    index_url = config_parser.get("FeedCollector", "index_url")
    cluster_url = config_parser.get("FeedCollector", "cluster_url")
    feed_url = config_parser.get("FeedCollector", "feed_url")
    article_url = config_parser.get("FeedCollector", "article_url")


    feed_collector = create_feed_collector(index_url, cluster_url, feed_url, article_url)
    while True:
        feed_collector.collect()
        time.sleep(wait_time)
