import webapp2
import jinja2

import os

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class Controller(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Index(Controller):
    def get(self):
        self.response.out.write('hello, world')

class PasteMain(Controller):
    def get(self):
        self.render('paste.html')

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/paste', PasteMain),
],
    debug=True)
