# -*- coding: utf-8 -*-
#!/usr/bin/env python

import cgi
import os
import time
import datetime

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class Feedback(db.Model):
  type = db.StringProperty(multiline=False)
  content = db.StringProperty(multiline=True)
  name = db.StringProperty(multiline=False)
  date = db.DateTimeProperty(auto_now_add=True)

class Del(webapp.RequestHandler):
  def get(self):
    q = db.GqlQuery("SELECT * FROM Feedback")
    results = q.fetch(10)
    for result in results:
      result.delete()

class Add(webapp.RequestHandler):
  def post(self):
    feedback = Feedback()

    feedback.name = self.request.get('name')
    feedback.content = self.request.get('content')
    feedback.type = self.request.get('type')
    feedback.put()

class List(webapp.RequestHandler):
  def get(self):
    apptype= {
              'redhorse':'小红马',
              'quickstart':'快速启动',
              'all':'所有',
            }
    where = ''
    if cgi.escape(self.request.get('type')) == 'all':
      where =  ""
    else:
      where =  "WHERE type = '"+apptype[cgi.escape(self.request.get('type'))].decode('utf-8')+"'"
    q = db.GqlQuery("SELECT * FROM Feedback "+where)
    results = q.fetch(100)
    
    template_values = {
      'itemlist': results,
      'type': apptype[cgi.escape(self.request.get('type'))],
      }

    path = os.path.join(os.path.dirname(__file__), 'list.html')
    self.response.out.write(template.render(path, template_values))

class New(webapp.RequestHandler):
  def get(self):
    template_values = {
      }
    path = os.path.join(os.path.dirname(__file__), 'new.html')
    self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([
  ('/del', Del),
  ('/add', Add),
  ('/new', New),
  ('/list', List),
], debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()