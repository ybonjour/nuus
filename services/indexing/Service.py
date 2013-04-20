__author__ = 'Yves Bonjour'

import sys
from Indexer import create_indexer
from werkzeug.routing import Map, Rule
from WerkzeugService import WerkzeugService
from WerkzeugService import create_status_ok_response
from WerkzeugService import create_status_error_response
from WerkzeugService import create_json_response

USAGE = "USAGE: python Service.py [host] [port]"

def create_index_service(host, port):
    return IndexService(create_indexer(), host, port)

class IndexService(WerkzeugService):

    def __init__(self, indexer, host, port):
        super(IndexService, self).__init__(host, port, Map([
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
    arguments = sys.argv[1:]
    if len(arguments) != 2:
        print(USAGE)
        quit()

    host = arguments[0]
    try:
        port = int(arguments[1])
    except ValueError:
        print(USAGE)
        quit()

    service = create_index_service(host, port)
    service.run()
