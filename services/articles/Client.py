__author__ = 'Yves Bonjour'

import requests
import datetime

feed_service = "http://localhost:5003/"

def add_article(title, text, updated_on, feed):
    service_url = feed_service + "add"
    payload = {"title": title, "text": text, "updated_on": updated_on, "feed": feed}
    r = requests.post(service_url, data=payload)
    print r.status_code
    print r.content

if __name__ == "__main__":
    title = "Lorem Ipsum"
    text = "Dolor sit amet"
    updated_on = datetime.date.today()
    feed = "http://feeds.espace.ch/espacenews"
    add_article(title, text, updated_on, feed)