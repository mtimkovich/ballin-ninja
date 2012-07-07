import webapp2
import jinja2

import os
import hashlib
import logging

from google.appengine.ext import db
from google.appengine.api import memcache

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

def blank(string):
    return (not string or string.isspace())

class Controller(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Paste(db.Model):
    name = db.StringProperty()
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class Index(Controller):
    def get(self):
        self.render('paste.html')

    def post(self):
        content = self.request.get('content')

        if not blank(content):
            p = Paste(content = content)
            p.put()

            id = str(p.key().id())
            name = hashlib.md5(id).hexdigest()[0:6]

            p.name = name
            p.put()

            memcache.set(name, content)

            self.redirect('/paste/' + name)
        else:
            error = 'paste cannot be blank'
            self.render('paste.html', error = error)


class PastePage(Controller):
    def get_paste(self, name):
        paste = memcache.get(name)

        if not paste:
            logging.info('DB QUERY')
            rows = Paste.all().filter('name =', name)

            if rows.count():
                paste = rows[0].content
                memcache.set(name, paste)
            else:
                return None

        return paste

    def get(self, name):
        content = self.get_paste(name)

        if content:
            self.response.headers['Content-Type'] = 'text/plain'
            self.write(content)
        else:
            self.error(404)

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/paste/(\w+)', PastePage),
],
    debug=True)
