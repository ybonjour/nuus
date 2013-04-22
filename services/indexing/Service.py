__author__ = 'Yves Bonjour'

import sys
import os
import uuid
import ConfigParser
from Indexer import create_indexer
from werkzeug.routing import Map, Rule
from WerkzeugService import WerkzeugService
from WerkzeugService import create_status_ok_response
from WerkzeugService import create_status_error_response
from WerkzeugService import create_json_response

USAGE = "USAGE: python Service.py [config_file]"

def create_index_service(host, port, debug, redis_host, redis_port):
    indexer = create_indexer(redis_host, redis_port)
    return IndexService(indexer, host, port, debug)

class IndexService(WerkzeugService):

    def __init__(self, indexer, host, port, debug):
        super(IndexService, self).__init__(host, port, Map([
            Rule('/posting_list/<term>', endpoint='posting_list'),
            Rule('/terms/<document_id>', endpoint='terms'),
            Rule('/tdf/<term>/<document_id>', endpoint='tdf'),
            Rule('/df/<term>', endpoint='df'),
            Rule('/index/<document>', endpoint='index')
        ]), debug=debug)

        self.indexer = indexer

    def on_posting_list(self, _, term):
        posting_list = {str(doc_uuid):value for doc_uuid, value in self.indexer.get_posting_list(term).iteritems()}
        return create_json_response(posting_list)

    def terms(self, _, document_id):
        terms = self.indexer.get_terms(uuid.UUID(document_id))
        return create_json_response(terms)

    def tdf(self, _, **arguments):
        if "term" not in arguments or "document_id" not in arguments:
            return create_status_error_response("Invalid request", status_code=400)

        tdf = self.indexer.term_document_frequency(arguments["terms"], uuid.UUID(arguments["document_id"]))
        return create_json_response({"tdf": tdf})

    def df(self, _, term):
        df = self.indexer.document_frequency_normalized(term)
        return create_json_response({"df", df})

    def on_index(self, request, document):
        if request.method != "POST":
            return create_status_error_response("Request must be POST", status_code=400)

        if "title" not in request.form or "text" not in request.form:
            return create_status_error_response("Request must have the fields title and text", status_code=400)

        title = request.form["title"]
        text = request.form["text"]

        self.indexer.index(title, document)
        self.indexer.index(text, document)

        return create_status_ok_response()

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

    host = config_parser.get("IndexingService", "host")
    port = config_parser.getint("IndexingService", "port")
    debug = config_parser.getboolean("IndexingService", "debug")
    redis_host = config_parser.get("IndexingService", "redis_host")
    redis_port = config_parser.getint("IndexingService", "redis_port")


    service = create_index_service(host, port, debug, redis_host, redis_port)
    service.run()
