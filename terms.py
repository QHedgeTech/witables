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

	f = open(filepath + '/LICENSE')

	output += '''
<div class="jumbotron">
  <h1>Terms</h1>
  <h2>CopyLeft</h2>
  <p>Do whatever it pleases you with the sources as long as your code remains open.</p>
  <p><a class="btn btn-primary btn-lg" role="button">Getting Started</a></p>
</div>

<div class="panel panel-default">
  <div class="panel-heading">Panel heading without title</div>
  <div class="panel-body">
    %s
  </div>
</div>
''' % f.read()


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

