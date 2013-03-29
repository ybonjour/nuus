__author__ = 'Yves Bonjour'

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../common"))

from WerkzeugService import create_status_error_response
from WerkzeugService import create_status_ok_response
from WerkzeugService import WerkzeugService
from werkzeug.routing import Map, Rule
from werkzeug.utils import  redirect
from NewsletterStore import create_newsletter_store
from NewsletterStore import is_valid



def create_newsletter_service(port):
    store = create_newsletter_store()
    return NewsletterService(store, port)


class NewsletterService(WerkzeugService):
    def __init__(self, store, port):
        super(NewsletterService, self).__init__(port, Map([
            Rule('/register', endpoint='register'),
            Rule('/', endpoint='index')
        ]), {"/": os.path.join(os.path.dirname(__file__), "web")}, False)
        self.store = store

    def on_index(self, request):
        return redirect('/index.html');

    def on_register(self, request):
        if request.method != "POST":
            return create_status_error_response("Request must be POST", status=400)

        if "email" not in request.form:
            return create_status_error_response("Request must have the fields title and text", status=400)

        email = request.form["email"]

        if not is_valid(email):
            return create_status_error_response("Invalid e-mail address.", status_code=400)

        self.store.store_email(email)

        return create_status_ok_response()


if __name__ == "__main__":
    usage = "USAGE: python Service.py [port]"
    if len(sys.argv) != 2:
        print(usage)
        quit()

    try:
        port = int(sys.argv[1])
    except ValueError:
        print(usage)
        quit()

    service = create_newsletter_service(port)
    service.run()