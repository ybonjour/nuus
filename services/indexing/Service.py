__author__ = 'Yves Bonjour'

from Indexer import create_indexer
from werkzeug.serving import run_simple
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException

from werkzeug.wrappers import Request, Response
import json

def create_index_service():
    return IndexService(create_indexer())

class IndexService(object):

    def __init__(self, indexer):
        self.url_map = Map([
            Rule('/posting_list/<term>', endpoint='posting_list'),
            Rule('/index/<document>', endpoint='index')
        ])

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

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, 'on_' + endpoint)(request, **values)
        except HTTPException, e:
            return e

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


def create_status_ok_response():
    return create_json_response({"status": "ok"})


def create_status_error_response(message, status_code=500):
    return create_json_response({"status": "error", "message": message}, status_code)


def create_json_response(obj, status_code=200):
    return Response(json.dumps(obj), mimetype="application/json", status=status_code)


if __name__ == "__main__":
    service = create_index_service()
    run_simple('127.0.0.1', 5000, service, use_debugger=True, use_reloader=True)
