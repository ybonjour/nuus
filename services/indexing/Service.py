__author__ = 'Yves Bonjour'

from Indexer import create_indexer
from werkzeug.serving import run_simple
from werkzeug.routing import Map, Rule
from WerkzeugService import WerkzeugService
from WerkzeugService import create_status_ok_response
from WerkzeugService import create_status_error_response
from WerkzeugService import create_json_response

def create_index_service():
    return IndexService(create_indexer())

class IndexService(WerkzeugService):

    def __init__(self, indexer):
        super(IndexService, self).__init__(Map([
            Rule('/posting_list/<term>', endpoint='posting_list'),
            Rule('/index/<document>', endpoint='index')
        ]))

        self.indexer = indexer

    def on_posting_list(self, _, term):
        posting_list = {str(doc_uuid):value for doc_uuid, value in self.indexer.get_posting_list(term).iteritems()}
        return create_json_response(posting_list)

    def on_index(self, request, document):
        if request.method != "POST":
            return create_status_error_response("Request must be POST", status=400)

        if "title" not in request.form or "text" not in request.form:
            return create_status_error_response("Request must have the fields title and text", status=400)

        title = request.form["title"]
        text = request.form["text"]

        self.indexer.index(title, document)
        self.indexer.index(text, document)

        return create_status_ok_response()

if __name__ == "__main__":
    service = create_index_service()
    service.run()
