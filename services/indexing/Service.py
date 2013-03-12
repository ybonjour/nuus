__author__ = 'Yves Bonjour'

from Indexer import create_indexer
from werkzeug.serving import run_simple
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException

from werkzeug.wrappers import Request, Response
import json


class IndexService(object):

    def __init__(self):
        self.url_map = Map([
            Rule('/posting_list/<term>', endpoint='posting_list')
        ])

        self.indexer = create_indexer()

    def on_posting_list(self, request, term):
        posting_list = self.indexer.get_posting_list(term)
        return create_json_response(posting_list)

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

def create_json_response(obj):
    return Response(json.dumps(obj), mimetype="application/json")


if __name__ == "__main__":
    service = IndexService()
    run_simple('127.0.0.1', 5000, service, use_debugger=True, use_reloader=True)
