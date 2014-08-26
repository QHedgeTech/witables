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

def errorModal(activeRow,activeCol,msg):
	output = '''
<div class="modal-header">
<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
<h4 class="modal-title">Error loading value row: %s, col: %s</h4>
</div>

<div class="modal-body">
    <div class="te">%s</div>
</div>

<div class="modal-footer">
    <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
</div>''' % (activeRow, activeCol, msg)


	# Encode it.
	utf8_output = output.encode('utf-8')

	return utf8_output

def makeBody(activeFile,activeNode,activeRow,activeCol):

	# Open database file.
	database = open_file(filepath + databaseDirectory + '/' + activeFile, mode = 'r')

	# Get the node with path
	table = database.get_node(activeNode)

	# If an exception occurs we try again
	# If an exception occurs we try again
	if type(table) is not Table:
		return errorModal(activeRow, activeCol, "Error while loading node %s in file %s" % (activeFile,activeNode))

	# Get the value
	value = table[int(activeRow)][activeCol]

	# Close database file
	database.close()

	output = '''
<div class="modal-header">
<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
<h4 class="modal-title">%s%s row:%s col:%s</h4>
</div>

<div class="modal-body">
    <div class="te">%s</div>
</div>

<div class="modal-footer">
    <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
</div>''' % (activeFile, activeNode, activeRow, activeCol, value)


	# Encode it.
	utf8_output = output.encode('utf-8')

	return utf8_output 

def application(environ, start_response):
	# Process the parameters if any.
	parameters = parse_qs(environ.get('QUERY_STRING', ''))

	# Test if we've got an active filename.
	if 'file' not in parameters.keys():
		return errorPage('Missing argument. Value page needs a filename argument.<br>Example: value?file=test.h5&path=/foo/bar&row=0&col=chips', start_response)

	# Test if we've got an active filename.
	if 'path' not in parameters.keys():
		return errorPage('Missing argument. Value page needs a path argument that contains the path of the node.<br>Example: value?file=test.h5&path=/foo/bar&row=0&col=chips', start_response)

	# Test if we've got an active filename.
	if 'row' not in parameters.keys():
		return errorPage('Missing argument. Value page needs a row argument that contains the row number in table.<br>Example: value?file=test.h5&path=/foo/bar&row=0&col=chips', start_response)

	# Test if we've got an active filename.
	if 'col' not in parameters.keys():
		return errorPage('Missing argument. Value page needs a "col" argument that contains the row number in table.<br>Example: value?file=test.h5&path=/foo/bar&row=0&col=chips', start_response)

	# Get the filename
	activeFile = parameters['file'][0]
	
	# Get the table path
	activeNode  = parameters['path'][0]
	
	# Get the row number
	activeRow  = parameters['row'][0]
	
	# Get the column name
	activeCol  = parameters['col'][0]

	# Make answer header.
	status = '200 OK'
	response_headers = [('Content-Type', 'text/html; charset=utf-8')]
	start_response(status, response_headers)

	# Return it.
	return [makeBody(activeFile,activeNode,activeRow,activeCol)]

#print makeBody('test.h5','/Economics/GDPEUESTQUOGLD','0','QuoteDate')
