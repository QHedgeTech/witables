#!/usr/bin/python

# Store the filepath for file manipulation
import os
filepath = os.path.abspath(os.path.dirname(__file__))

# Add the file path to the system path to import framework file.
import sys
if filepath not in sys.path:
	sys.path.append(filepath)

# Debug Module.
import cgitb
cgitb.enable()

# Framework module
from framework import *

def makeBody():

	output = '<a href="https://github.com/QHedgeTech/witables"><img style="position: absolute; top: 0; right: 0; border: 0;z-index:2" src="https://camo.githubusercontent.com/652c5b9acfaddf3a9c326fa6bde407b87f7be0f4/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f6769746875622f726962626f6e732f666f726b6d655f72696768745f6f72616e67655f6666373630302e706e67" alt="Fork me on GitHub" data-canonical-src="https://s3.amazonaws.com/github/ribbons/forkme_right_orange_ff7600.png"></a>'

	f = open(filepath + '/VERSION')
	output += '<div class="jumbotron"><h1>WiTables <small>%s</small></h1>' % f.read()

	output += '''
  <h2>The missing view on your PyTables.</h2>
  <p>WiTables is a web-based visualization tool for PyTables. It has been developed by <a href="https://github.com/QHedgeTech">Q-Hedge Technologies</a> as an open-source project. You can contribute on github.</p>
  <p><a class="btn btn-primary btn-lg" role="button" href="https://github.com/QHedgeTech/witables/blob/master/README.md">Getting Started</a> <a class="btn btn-success btn-lg" role="button" href="witables.py">View</a></p>
</div>

      <div class="row">
        <div class="col-md-3">
          <h2>Simple</h2>
          <p>Copy the source code into your localhost directory. Create a symbolic link to your database folder and that's it.</p><p>Don't forget to put a firewall. By default, the code comes with .htaccess files that restrains access to local network.</p>
          <p><a class="btn btn-default" href="https://github.com/QHedgeTech/witables/blob/master/README.md" role="button">View details &raquo;</a></p>
        </div>
        <div class="col-md-3">
          <h2>View & Search</h2>
          <p>Have a look to your data, check them rapidly, don't loose your time anymore to <code>print data</code>.</p><p>Browse them with your favorite web-browser. Bookmark them and navigate with the navigation bar.</p>
          <p><a class="btn btn-default" href="example/select_file.html" role="button">View details &raquo;</a></p>
       </div>
        <div class="col-md-3">
          <h2>Modify</h2>
          <p>This is to come. Nothing has been done in this version to manipulate data.</p><p>Security issues will come with it and a session management will be required to attribute roles to users.</p>
        </div>
        <div class="col-md-3">
          <h2>Graph</h2>
          <p>Some people put pressure on the project to add a graph feature. This would be really nice but is beyond of the actual project.</p><p>Libraries and Contributors are welcome.</p>
        </div>
      </div>'''

	return output

def application(environ, start_response):
	# Process the parameters if any.
	parameters = parse_qs(environ.get('QUERY_STRING', ''))
	
	# Don't accept any parameter on this page.
	if parameters:
		return errorPage('This page does not accept any parameter.', start_response)

	# Make answer header.
	status = '200' + ' ' + status_description['200']
	response_headers = [('Content-Type', 'text/html; charset=utf-8')]
	start_response(status, response_headers)

	# Set Content Parameters
	content = {'title':'WiTables', 'navbar':navbar(parameters), 'body':makeBody()}

	# Return it.
	return [html(content)]

