__author__ = 'Yves Bonjour'

from WerkzeugService import create_status_error_response
from WerkzeugService import create_status_ok_response
from WerkzeugService import WerkzeugService
from werkzeug.routing import Map, Rule
from werkzeug.utils import  redirect
from NewsletterStore import create_newsletter_store
from NewsletterStore import is_valid
import os


def create_newsletter_service():
    store = create_newsletter_store()
    return NewsletterService(store)


class NewsletterService(WerkzeugService):
    def __init__(self, store):
        super(NewsletterService, self).__init__(50010, Map([
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
    service = create_newsletter_service()
    service.run()