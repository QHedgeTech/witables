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

# Show the node as group structure
def makePlainText(activeFile, activePath):

	# Open database file.
	database = open_file(filepath + databaseDirectory + '/' + activeFile, mode = 'r')

	# Get the node with path
	node = database.get_node(activePath)

	output = ''	
	#Allowed classname: 'Group', 'Leaf', 'Table' and 'Array'
	if node._f_getattr('CLASS') == 'GROUP':
		output = node._v_nchildren

	if node._f_getattr('CLASS') == 'TABLE':
		output = node.nrows

	if node._f_getattr('CLASS') == 'ARRAY':
		# Array class is not handled yet.
		raise AttributeError

	if node._f_getattr('CLASS') == 'LEAF':
		# Array class is not handled, don't know what to do with it now.
		raise AttributeError

	# Close database file
	database.close()

	return str(output)

def application(environ, start_response):
	# Process the parameters if any.
	parameters = parse_qs(environ.get('QUERY_STRING', ''))

	# Test if we've got an active filename.
	if 'file' not in parameters.keys():
		return errorPage('Missing argument. childnumber page needs a filename argument.', start_response)

	# Test if we've got an active filename.
	if 'path' not in parameters.keys():
		return errorPage('Missing argument. childnumber page needs a path argument.', start_response)

	# Get the filename
	activeFile = parameters['file'][0]

	# Get the node path
	activePath  = parameters['path'][0]

	# Make body answer
	output = makePlainText(activeFile, activePath)

	# Encode it
	utf8_version = output.encode('utf-8')

	# Make answer header
	status = '200 OK'
	response_headers = [('Content-Type', 'text/html; charset=utf-8'), ('Content-Length', str(len(utf8_version)))]
	start_response(status, response_headers)

	# Return the body answer
	return [utf8_version]

print makePlainText('QDatabaseESFinal.h5', '/Economics')
