import os
import re
from string import letters

import webapp2
import jinja2

from google.appengine.ext import db

#Template Finder ---------------------------------
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

#Not sure what this is---------------------------------
def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)


#Page Handlers for actual pages ---------------------------------
class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world! - this is my project')

class FormHandler(BaseHandler):
     def get(self):
        self.render('form.html')

#Loads handler based on URL ---------------------------------
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/form', FormHandler)
], debug=True)
