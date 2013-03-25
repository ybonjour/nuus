__author__ = 'Yves Bonjour'

from Clusterer import create_clusterer

from werkzeug.serving import run_simple
from werkzeug.routing import Map, Rule
from WerkzeugService import WerkzeugService
from WerkzeugService import create_status_ok_response


def create_clustering_service():
    return ClusteringService(create_clusterer())


class ClusteringService(WerkzeugService):

    def __init__(self, clusterer):
        super(ClusteringService, self).__init__(Map([
            Rule('/add/<document>', endpoint='add'),
            ]))

        self.clusterer = clusterer

    def on_add(self, _, document):
        self.clusterer.add_document(document)
        return create_status_ok_response()

if __name__ == "__main__":
    service = create_clustering_service()
    run_simple('127.0.0.1', 5000, service, use_debugger=True, use_reloader=True)