__author__ = 'Yves Bonjour'

import ConfigParser
import os
import sys
from Clusterer import create_clusterer
from werkzeug.routing import Map, Rule
from WerkzeugService import WerkzeugService
from WerkzeugService import create_status_ok_response
from WerkzeugService import create_status_error_response

USAGE = "USAGE: python Service.py [config_file]"

def create_clustering_service(host, port, debug, redis_host, redis_port, clustering_threshold, index_url):
    clusterer = create_clusterer(redis_host, redis_port, clustering_threshold, index_url)
    return ClusteringService(clusterer, host, port, debug)


class ClusteringService(WerkzeugService):

    def __init__(self, clusterer, host, port, debug):
        super(ClusteringService, self).__init__(host, port, Map([
            Rule('/add/<document>', endpoint='add'),
            ]), debug=debug)

        self.clusterer = clusterer

    def on_add(self, _, document):
        try:
            self.clusterer.add_document(document)
            return create_status_ok_response()
        except Exception as e:
            return create_status_error_response(str(e))

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
    host = config_parser.get("ClusteringService", "host")
    port = config_parser.getint("ClusteringService", "port")
    debug = config_parser.getboolean("ClusteringService", "debug")
    redis_host = config_parser.get("ClusteringService", "redis_host")
    redis_port = config_parser.getint("ClusteringService", "redis_port")
    clustering_threshold = config_parser.getfloat("ClusteringService", "threshold")
    index_url = config_parser.get("ClusteringService", "index_url")

    service = create_clustering_service(host, port, debug, redis_host, redis_port, clustering_threshold, index_url)
    service.run()