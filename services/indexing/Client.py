__author__ = 'Yves Bonjour'

import uuid
import requests

indexing_service = "http://localhost:5000/"


def index(document, title, text):
    url = indexing_service + "index/" + str(document)

    payload = {"title": title, "text": text}
    r = requests.post(url, data=payload)
    print r.status_code
    print r.content


if __name__ == "__main__":
    doc_id = uuid.uuid4()
    index(doc_id, "An Article", "An article text")

    print "indexed document " + str(doc_id)