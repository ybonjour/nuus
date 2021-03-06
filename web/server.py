import cherrypy
from mako.lookup import TemplateLookup
from controller.StreamController import StreamController
import os


def main():
    lookup = TemplateLookup(directories=['view'])
    stream = StreamController(lookup)

    contentDispatcher = cherrypy.dispatch.RoutesDispatcher()
    contentDispatcher.connect('stream', '/', controller=stream, action='index')
    conf = {'/': {'request.dispatch': contentDispatcher}}
    app = cherrypy.tree.mount(root=None, config=conf)

    cssHandler = cherrypy.tools.staticdir.handler(section="/", dir=os.path.join(os.path.dirname(__file__), "static/css"))
    cherrypy.tree.mount(cssHandler, '/css')

    jsHandler = cherrypy.tools.staticdir.handler(section="/", dir=os.path.join(os.path.dirname(__file__), "static/js"))
    cherrypy.tree.mount(jsHandler, '/js')

    imgHandler = cherrypy.tools.staticdir.handler(section="/", dir=os.path.join(os.path.dirname(__file__), "static/img"))
    cherrypy.tree.mount(imgHandler, '/static/img')

    imgHandler = cherrypy.tools.staticdir.handler(section="/", dir=os.path.join(os.path.dirname(__file__), "static/templates"))
    cherrypy.tree.mount(imgHandler, '/static/templates')

    cherrypy.config.update('production.conf')

    cherrypy.quickstart(app)


if __name__ == '__main__':
    cherrypy.quickstart(main())