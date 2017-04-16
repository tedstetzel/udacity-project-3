import os
import re
from string import letters

import webapp2
import jinja2

from google.appengine.ext import db

"""Step 1: Create a Basic Blog
Front page that lists blog posts.
A form to submit new entries.
Blog posts have their own page."""


# Template Finder ---------------------------------
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

# Used by Page Handlers to load template---------------------------------

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


class BaseHandler(webapp2.RequestHandler):

    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

# Write posts to Database ---------------------------------

#First make ID
def blog_uid(name = 'default'):
    return db.Key.from_path('blogs', name)

#Right post to DB
class Post(db.Model):
    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

   # escape line breaks and entries from database
    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p=self)

# Page Handlers for actual pages ---------------------------------

# Homepage


class MainHandler(BaseHandler):

    def get(self):
        self.render('blog.html')


# Make New Post page
class NewPostHandler(BaseHandler):

    def get(self):
        self.render('form.html')

    def post(self):
        title = self.request.get('title')
        content = self.request.get('content')

        if title and content:
            # p = Post(parent = blog_uid(), title = title, content = content)
            p = Post(parent = blog_uid(), title = title, content = content)
            p.put()
            self.redirect('/blog')
        else:
            error = "Please supply and Title and blog entry"
            self.render("form.html", title=title, content=content, error=error)

# List of all posts
class BlogHomePage(BaseHandler):

    def get(self):
        posts = db.GqlQuery("select * from Post order by created desc limit 5")
        self.render('homepage.html', posts=posts)


# View a single blog post on it's own page
class BlogPostPage(BaseHandler):

    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_uid())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        self.render("blog-page.html", post=post)

#Login 
class LoginHandler(BaseHandler):

    def get(self):
        self.render('login.html')

#Sign up 
class SignupHandler(BaseHandler):

    def get(self):
        self.render('sign-up.html')


# Loads handler based on URL ---------------------------------
app = webapp2.WSGIApplication([
    ('/blog', BlogHomePage),
    ('/new-post', NewPostHandler),
    ('/blog/([0-9]+)', BlogPostPage),#numbers only in blog link
    ('/sign-up', SignupHandler),
    ('/login', LoginHandler)
], debug=True)
