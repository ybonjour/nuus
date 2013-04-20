class StreamController(object):
    def __init__(self, lookup):
        self.lookup = lookup

    def index(self):
        tmpl = self.lookup.get_template("stream.html")
        return tmpl.render()