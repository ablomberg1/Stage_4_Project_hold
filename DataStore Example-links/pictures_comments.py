import webapp2
# library - ndb is amodule that helps create these properties
from google.appengine.ext import ndb

# define Picture class, give it some attributes (data type)
class Picture(ndb.Model):
	link = ndb.StringProperty()
	comment = ndb.StringProperty()
	date = ndb.DateTimeProperty(auto_now_add=True)
	# id = ndb.IntegerProperty()
	# use documentation to determine the correct property type
	# https://cloud.google.com/appengiven/docs/python/ndb/properties

	# DEBUG Populate Datastore for testing

	#create a few objects
	# pic1 = Picture(link='http://i2.cdn.turner.com/cnnnext/dam/assets/150611161942-04-week-in-photos-0612-restricted-super-169.jpg', 
	# 	comment='Love this picture!')

	# pic2 = Picture(link='http://i2.cdn.turner.com/cnnnext/dam/assets/150611172724-39-week-in-photos-0612-super-169.jpg', 
	# 	comment='This is crazy!')

	# # Saves the pictures to the database, datastore (this is the majic). Use the method put
	# pic1.put()
	# pic2.put()

	# # Need to wate a little bit of time for the local Datastore to update.
	# import time
	# time.sleep(.1)
	# tells python to wait for .1 seconds

# use string formatting to replace 
# html template - the variable is HTML
HTML = '''<!DOCTYPE html>
<html>
	<head>
		<meta charset='utf-8'>
		<meta http-equiv="x-UA-Compatible" content="IE=edge">
		<title>Favorite Pictures!</title>
		<style>input[type='text'] {width: 412px;}
		th {color: teal;}
		td {border: 1px solid black;}
		img {width: 450px}
		label {font-weight: bold;}
		.error {color: red;font-weight: bold;}
		</style>
	</head>
	<body>
		<h1>Hello! Please submit a picture link and comment on the picture</h1>
		<!-- Insert table of pictures here (use string formatting to replace the string)-->
		%s
		<br>
		<span class="error">%s</span> <!--create space for error message here--><br><br>
		<form method="post" action="/">
			<label>link</label><br><input type="text" name="link"<br><br>
			<label>comment</label><br><textarea name="comment" rows=10 cols=66></textarea>
			<br>
			<input type="submit">
		</form>
	</body>
</html>'''

	# how do you extract data from the database




class MainPage(webapp2.RequestHandler):
	def get(self):
		error = self.request.get('error','') #check for error message
		query = Picture.query().order(Picture.date) #query Datastore and order earliest date first
		# query method and order method (1st picture added will appear first)
		# how to extract data from db

		# method called fetch. fetch me 5 pictures from the db
		# pictures_list = query.fetch(5)

		# print '####'
		# print len(pictures_list) #index
		# print pictures_list[0].link
		# print pictures_list[1].link
		# print '####'

		# # OR test to print out all the picture objects
		# print '####'
		# for picture in query:
		# 	print picture.link
		# print '####'

		# write information from the Datastore and build the HTML table
		table = '<table>\n<tr><th>Link</th><th>Comment</th></tr>\n'
		#table = 'HELLO WORLD HELLO HELLO'
		#error = 'THERE IS AN ERROR HERE'

		#Create a row for every picture in the query. Get picture and comment
		# this is how you would get data and present it in a useable form
		for picture in query:
			link = picture.link
			comment = picture.comment

		# build html here
			row = '<tr>\n'
			row += '<td><img src="' + link + '" alt="picture"></td>\n'
			row += '<td>' + comment + '</td>\n'
			row += '</tr>\n'

			table += row
		table += '<table>\n' #close out table loop

		rendered_html = HTML % (table,error)

		self.response.out.write(rendered_html)

	def post(self):
		link = self.request.get('link')
		comment = self.request.get('comment')

		# if either of the fields (link or comment) is blank
		if link and comment:
			picture = Picture(link=link, comment=comment)
			picture.put()

			import time
			time.sleep(.1)
			self.redirect('/')
		else:
			self.redirect('/?error=Please fill out the link and comment sections!')

router = [('/',MainPage)]

app = webapp2.WSGIApplication(router, debug=True)

