__author__ = 'Yves Bonjour'

import sys
import os
import ConfigParser
from WerkzeugService import WerkzeugService
from WerkzeugService import create_status_error_response
from WerkzeugService import create_json_response
from werkzeug.routing import Map, Rule
from Articles import Article
from Articles import create_articles
from Articles import article_to_dict

USAGE = "USAGE: python Service.py [config_file]"

def create_article_service(host, port, debug, couch_host, couch_port, couch_db):
    article_service = create_articles(couch_host, couch_port, couch_db)
    return ArticleService(article_service, host, port, debug)

class ArticleService(WerkzeugService):
    def __init__(self, articles, host, port, debug):
        super(ArticleService, self).__init__(host, port, Map([
            Rule('/add', endpoint='add'),
            Rule('/articles', endpoint='articles')
        ]), debug=debug)

        self.articles = articles

    def on_articles(self, _):
        articles = self.articles.get_articles()
        d = [article_to_dict(a) for a in articles]
        return create_json_response(d)

    def on_add(self, request):
        if request.method != "POST":
            return create_status_error_response("Request must be POST", status_code=400)

        if "title" not in request.form or "text" not in request.form or "feed" not in request.form or "updated_on" not in request.form:
            return create_status_error_response("Request must have required attributes of article", status_code=400)

        article = Article(request.form["title"], request.form["text"], request.form["updated_on"], request.form["feed"])

        try:
            article_id = self.articles.add_article(article)
        except Exception as e:
            return create_status_error_response(str(e))

        return create_json_response({"status": "ok", "id": article_id})


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

    host = config_parser.get("ArticleService", "host")
    port = config_parser.getint("ArticleService", "port")
    debug = config_parser.getboolean("ArticleService", "debug")
    couch_host = config_parser.get("ArticleService", "couch_host")
    couch_port = config_parser.getint("ArticleService", "couch_port")
    couch_db = config_parser.get("ArticleService", "couch_db")

    service = create_article_service(host, port, debug, couch_host, couch_port, couch_db)
    service.run()