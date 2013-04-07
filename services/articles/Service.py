__author__ = 'Yves Bonjour'

from WerkzeugService import WerkzeugService
from WerkzeugService import create_status_error_response
from WerkzeugService import create_status_ok_response
from WerkzeugService import create_json_response
from werkzeug.routing import Map, Rule
from Articles import Article
from Articles import create_articles
from Articles import article_to_dict

def create_article_service():
    article_service = create_articles()
    return ArticleService(article_service)

class ArticleService(WerkzeugService):
    def __init__(self, articles):
        super(ArticleService, self).__init__("localhost", 5003, Map([
            Rule('/add', endpoint='add'),
            Rule('/articles', endpoint='articles')
        ]))

        self.articles = articles

    def on_articles(self, request):
        articles = self.articles.get_articles()
        d = [article_to_dict(a) for a in articles]
        return create_json_response(d)

    def on_add(self, request):
        if request.method != "POST":
            return create_status_error_response("Request must be POST", status=400)

        if "title" not in request.form or "text" not in request.form or "feed" not in request.form or "updated_on" not in request.form:
            return create_status_error_response("Request must have required attributes of article", status=400)

        article = Article(request.form["title"], request.form["text"], request.form["updated_on"], request.form["feed"])

        try:
            article_id = self.articles.add_article(article)
        except Exception as e:
            return create_status_error_response(str(e))

        return create_json_response({"status": "ok", "id": article_id})


if __name__ == "__main__":
    service = create_article_service()
    service.run()