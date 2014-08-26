#!/usr/bin/python

from cgi import parse_qs, escape
from tables import *

# Database directory's name: this folder is a symbolic links from the web server location to the directory where the data actually are.
databaseDirectory = '/database'

# HTTP/1.1 status definition
status_description = {'200':'OK', '400': 'Bad Request', '404':'Not Found', '500':'Internal Server Error'}
	
# Error page html format
def error_html(msg):
	output = '''<!DOCTYPE html>
<html lang="fr">
<head>
<title>Error WiTables, I know it's not pleasant.</title>
</head>
<body>
	<h1>Error!</h1>
	%s
</body>
</html>
''' % str(msg)
	# Encode it.
	utf8_output = output.encode('utf-8')

	return utf8_output 

# Error page function, to show exception.
def errorPage(code, msg, environ, start_response):
	
	output = '''<!DOCTYPE html>
<html lang="fr">
<head>
<title>Error WiTables, I know it's not pleasant.</title>
</head>
<body>
	<h1>Error!</h1>
	%s
	<p>Environment: %s</p>
</body>
</html>
''' % (str(msg), str(environ))
	
	# Encode it.
	utf8_output = output.encode('utf-8')
	status = code + ' ' + status_description[code]
	response_headers = [('Content-type', 'text/html; charset=utf-8'),('Content-Length', str(len(utf8_output)))]
	start_response(status, response_headers)

	return [utf8_output]

# Empty Modal where that remotely loads its content.
def makeModal():
	modal = '''
<!-- Modal -->
<div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
        </div>
        <!-- /.modal-content -->
    </div>
    <!-- /.modal-dialog -->
</div>
<!-- /.modal -->
'''
	return modal

# Standard for truncation
def truncValue(value):
	stringValue = str(value)
	if len(stringValue) > 22:
		return stringValue[:19] + '...'
	
	return stringValue

# Extension is made vertically.
def extendValue(value, mapping):
	# If the value is not a matrix, simply return the value.
	if mapping[0] == 0:
		return value
	
	output = "<table class='table table-striped value' style='text-align:center'>"
	for row in value:
		output += '<tr><td>%s</td></tr>' % row
	output += '</table>'

	return output

# Spinner element
def spinner(nodeIndex=None):

	if nodeIndex is not None:
		return 	'<div class="spinner" id="spinner-%s"><div class="rect1"></div> <div class="rect2"></div> <div class="rect3"></div> <div class="rect4"></div> <div class="rect5"></div></div>' % nodeIndex

	return '<div class="spinner"><div class="rect1"></div> <div class="rect2"></div> <div class="rect3"></div> <div class="rect4"></div> <div class="rect5"></div></div>' 
	

# Navigation bar function that can be used to see the path of the node.
def navbar(navigation):

	output = '''
<nav class="navbar navbar-inverse" role="navigation">
	<div class="container-fluid">
    		<div class="navbar-header">
      			<a class="navbar-brand" href="index.py">WiTables</a>
    		</div>
	    	<div class="collapse navbar-collapse">
			
			<ul class="breadcrumb">
'''

	# In any case, put the home path, activate the last element.
	if 'path' in navigation.keys():
		output += '<li><a href="witables.py">Home</a></li>'
		# Get the filename
		activePath = navigation['path'][0]
		nodeList = activePath.split('/')
		nodeList.remove('')
		linkPath = ''
		for node in nodeList[:-1]:
			linkPath += '/' + node 
			output += '<li><a href="witables.py?path=%s">%s</a></li>'	% (linkPath, node)
		output += '<li class="active"><a href="witables.py?path=%s">%s</a></li>'	% (activePath, nodeList[-1])
	else:
		output += '<li class="active"><a href="witables.py">Home</a></li>'

	output += '''
			</ul>
	    	</div><!-- /.navbar-collapse -->
  	</div><!-- /.container-fluid -->
</nav>'''

	return output

# Meta HTML default content for each html render.
def meta():
	return '''
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="author" content="Q-Hedge Technologies">
<meta name="description" content="">
<meta name="keywords" content="python, pytables, visualization, witables, big data, huge datum">
'''

# CSS default content for each page, link bootstrap and custom style.
def css():
	return '''
<link href="bootstrap/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" type="text/css" href="css/witables.css">'''

# Footer that we always place as a signature.	
def footer():
	return '''
    <!-- FOOTER -->
    <hr>
    <footer>
      <p class="pull-right"><a href="#">Back to top</a></p>
      <p><img src="image/copyleft.jpg" alt="copyleft" width="30px"> 2014 Q-Hedge Technologies, Inc. &middot; <a href="privacy.py">Privacy</a> &middot; <a href="terms.py">Terms</a></p>
    </footer>
'''

# Javascript requested almost everywhere javascript (bootstrap and jquery), custom js comes after and can use function from jquery though.
def javascript():
	return '''
	<!-- Placed at the end of the document so the pages load faster -->
	<script src="bootstrap/js/jquery-1.11.1.min.js"></script>
	<script src="bootstrap/js/bootstrap.min.js"></script>
	<script src="js/witables.js"></script>
'''

# Build the html document.
def html(content):

	# For modal content, return the content.
	if 'modal' in content:
		# Encode and return it without document structure.
		return content['modal'].encode('utf-8')

	# First add head content
	output  = '<!DOCTYPE html><html lang="en"><head>%s' % meta()
	if 'title' in content:
		output += '<title>%s</title>' % content['title']
	else:
		output += '<title>WiTables - untitled</title>'
	output += '%s</head>' % css()

	# Then add body content
	output += '<body>'
	if 'navbar' in content:
		output += content['navbar']
	
	# Begin Container for body and footer
	output += '<div class="container">'
	if 'body' in content:
		output += content['body']
	
	output += footer()
	# end containter
	output += '</div>'

	# Place the common javascript.
	output += javascript()
	
	# Place custom javascript from page.	
	if 'javascript' in content:
		output += '<script>'
		output += content['javascript']
		output += '</script>'

	output += '</body></html>'

	# Encode it.
	utf8_output = output.encode('utf-8')

	return utf8_output
