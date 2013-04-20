__author__ = 'Yves Bonjour'

import requests
import uuid

feed_service = "http://localhost:5002/"

def add_feed(url, name, user):
    service_url = feed_service + "add"
    payload = {"url": url, "name": name, "user": user}
    r = requests.post(service_url, data=payload)
    print r.status_code
    print r.content


if __name__ == "__main__":
    user_id = uuid.uuid4()
    url = "http://feeds.espace.ch/espacenews"
    name = "espace.ch"
    add_feed(url, name, user_id)

    print "Added feed for user {0}".format(user_id)
