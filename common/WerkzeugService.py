__author__ = 'Yves Bonjour'

import json
from werkzeug.exceptions import HTTPException
import werkzeug.serving
from werkzeug.wrappers import Request, Response


class WerkzeugService(object):

    def __init__(self, url_map):
        self.url_map = url_map

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

    def run(self):
        werkzeug.serving.run_simple('127.0.0.1', 5000, self, use_debugger=True, use_reloader=True)


def create_status_ok_response():
    return create_json_response({"status": "ok"})


def create_status_error_response(message, status_code=500):
    return create_json_response({"status": "error", "message": message}, status_code)


def create_json_response(obj, status_code=200):
    return Response(json.dumps(obj), mimetype="application/json", status=status_code)

