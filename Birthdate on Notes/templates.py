import os
import jinja2
import webapp2


from validation import *

#to initialize jinja
#directory that my current file is in os.path.dirname(__file__)
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader (template_dir),
	autoescape = True)

class Handler(webapp2.RequestHandler):
  def write(self, *a, **kw):
    self.response.out.write(*a, **kw)

  def render_str(self, template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

  def render(self, template, **kw):
    self.write(self.render_str(template, **kw))

class MainPage(Handler):
  def write_form(self, error="", user_month="", user_day="", user_year=""):
    self.render("form.html", error=error, user_month=user_month, user_day=user_day, user_year=user_year)
    #dictionary that we pass into the form
    # self.response.out.write("form.html" % {"error": error,  
    #   "month": month, "day": day, "year": year})
  
  # helper function define variables
  def get_form_data(self):
    user_month = self.request.get('month')
    user_day = self.request.get('day')
    user_year = self.request.get('year')
    return user_month, user_day, user_year 

  def get(self):
    user_month, user_day, user_year=self.get_form_data()
    self.render("form.html", user_month=user_month, user_day=user_day, user_year=user_year)

  def post(self):
    user_month, user_day, user_year=self.get_form_data()
    month = valid_month(user_month)
    day = valid_day(user_day)
    year = valid_year(user_year)
  
    if not (month and day and year):
      self.write_form("That doesn't look valid to me, friend.",
            user_month, user_day, user_year)

    else:
      self.response.out.write("Thanks! That's a totally valid day!")

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
