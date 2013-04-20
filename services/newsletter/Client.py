__author__ = 'Yves Bonjour'

from urlparse import urljoin
import requests


newsletter_service = "http://localhost:50010/"


def register(email):
    url = urljoin(newsletter_service, "register")

    payload = {"email": email}
    r = requests.post(url, data=payload)
    print r.status_code
    print r.content

if __name__ == "__main__":
    register("ybonjour@student.ethz.ch")
