__author__ = 'Yves Bonjour'

from xml.etree import ElementTree
from collections import namedtuple
import unidecode

Feed = namedtuple("Feed", "title,url")
class OPML(object):
    def __init__(self, xml_tree):
        self.tree = xml_tree

    def get_feeds(self):
        for o in self.tree.findall("./body//outline[@type='rss']"):
            if not o.get("title") or not o.get("xmlUrl"): continue
            yield Feed(unidecode.unidecode(o.get("title")), o.get("xmlUrl"))

class OPMLReader(object):
    def read(self, filename):
        tree = ElementTree.parse(filename)
        return OPML(tree.getroot())

if __name__ == "__main__":
    reader = OPMLReader()
    opml = reader.read("subscriptions.xml")
    for f in opml.get_feeds():
        print f