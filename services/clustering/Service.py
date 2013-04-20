__author__ = 'Yves Bonjour'

from Clusterer import create_clusterer

from werkzeug.routing import Map, Rule
from WerkzeugService import WerkzeugService
from WerkzeugService import create_status_ok_response
from WerkzeugService import create_status_error_response


def create_clustering_service():
    return ClusteringService(create_clusterer())


class ClusteringService(WerkzeugService):

    def __init__(self, clusterer):
        super(ClusteringService, self).__init__(5001, Map([
            Rule('/add/<document>', endpoint='add'),
            ]))

        self.clusterer = clusterer

    def on_add(self, _, document):
        try:
            self.clusterer.add_document(document)
            return create_status_ok_response()
        except Exception as e:
            return create_status_error_response(str(e))

if __name__ == "__main__":
    service = create_clustering_service()
    service.run()