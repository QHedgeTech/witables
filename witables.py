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

def valueModal(table, activeFile, activeNode, activeCol, activeRow):

	# If an exception occurs we tells it and ask to retry.
	if type(table) is not Table:
		return errorModal(activeRow, activeCol, "Error while loading node %s in file %s" % (activeFile, activeNode))

	# Get the value
	value = table[int(activeRow)][activeCol]

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

def columnView(table, activeFile, activeNode, activeCol):
	
	# If an exception occurs we try again
	if type(table) is not Table:
		return "<h2>Error while loading node %s in file %s</h2>" % (activeFile, activeNode)

	# Get the column
	column = table.colinstances[activeCol]

	# Get the row number
	totalRowNumber = table.nrows
	
	# Set a header for the page.
	output = '<div class="page-header"><span class="badge pull-left">%s</span><h1>Column view <small>click row, column or value to see it</small></h1>' % totalRowNumber
	output += '<div style="float:right;"><br><button id="popover-description" type="button" class="btn btn-default" data-toggle="popover" data-placement="bottom" title="Description" data-content="%s">See PyTables Description</button>' % column.descr
	output += '&nbsp;<button id="popover-type" type="button" class="btn btn-info" data-toggle="popover" data-placement="bottom" title="Column Type" data-content="%s">See PyTables Column Type</button>' % column.type
	output += '</div></div>'

	# Print table description
	output += '<h3>From table %s</h3>' % column.table	

	# Add the modal window.
	output += makeModal()

	# Show the table in a table sctructure, isn't it smart ?
	output += '<br><table class="table table-striped value" style="text-align:center">'
	output += '<tr>'

	# First table headers.
	output += '<th style="text-align:center; width:50px;">Id</th>'
	mapping = [0,0]

	shape = table.coldescrs[activeCol].shape
	if not shape:
		output += '<th style="text-align:center">%s</th>' % activeCol
	else:
		if len(shape) == 1:
			output += '<th style="text-align:center">%s [%s]</th>' % (activeCol, shape[0])
			mapping = [shape[0],0]
		if len(shape) == 2:
			output += '<th style="text-align:center">%s [%sx%s]</th>' % (activeCol, shape[0], shape[1])
			mapping = [shape[0],shape[1]]
	output += '</tr>'

	# Then table data.
	rowNumber = 0
	for row in table.iterrows():
		
		# Create the truncated row version
		output += '<tr id="row-%s">' % rowNumber
		output += '<td><button type="button" class="btn btn-primary" id="row-button-%s">%s</button></td>' % (rowNumber, rowNumber)

		# Toggle modal when clicking on a value.
		output += '<td><a data-toggle="modal" data-target="#myModal" href="value.py?path=%s%s/%s/%s">%s</a></td>' % (activeFile, activeNode, activeCol, rowNumber, truncValue(row[activeCol]))
		output += '</tr>'

		# Create the extended row version
		extendedRowNumber = totalRowNumber + rowNumber
		output += '<tr id="row-%s" style="display:none;">' % extendedRowNumber
		output += '<td><button type="button" class="btn btn-success" id="row-button-%s">%s</button></td>' % (extendedRowNumber, rowNumber)

		# Toggle modal when clicking on a value.
		output += '<td><a data-toggle="modal" data-target="#myModal" href="value.py?path=%s%s/%s/%s">%s</a></td>' % (activeFile, activeNode, activeCol, rowNumber, extendValue(row[activeCol], mapping))
		output += '</tr>'

		rowNumber += 1
	output += '</table>'

	return output

def selectData(table, activeFile, activeNode):
	
	# Predicat: it must be a table.
	if type(table) is not Table:
		return "<h2>Error provided node %s in file %s is not a table.</h2>" % (activeFile, activeNode)

	# Get the row number
	totalRowNumber = table.nrows

	# Set a header for the page.
	output = '<div class="page-header"><span class="badge pull-left">%s</span><h1>Table view <small>click row, column or value to see it</small></h1>' % totalRowNumber
	output += '<div style="float:right;"><br><button id="popover-description" type="button" class="btn btn-default" data-toggle="popover" data-placement="bottom" title="Description" data-content="%s">See PyTables Description</button>' % table.description
	output += '&nbsp;<button id="popover-type" type="button" class="btn btn-info" data-toggle="popover" data-placement="bottom" title="Column Type" data-content="%s">See PyTables Column Type</button>' % table.coltypes
	output += '</div></div>'

	# Add the modal window.
	output += makeModal()

	# Show the table in a table sctructure, isn't it smart ?
	output += '<br><table class="table table-striped value" style="text-align:center">'


	# First table headers.
	output += '<th style="text-align:center">Id</th>'
	mapping = {}
	for name in table.colnames:
		shape = table.coldescrs[name].shape
		output += '<th style="text-align:center"><a href="witables.py?path=%s%s/%s">%s</a>' % (activeFile, activeNode, name, name)
		if not shape:
			output += '</th>'
			mapping[name] = [0,0]
		else:
			if len(shape) == 1:
				output += ' [%s]</th>' % shape[0]
				mapping[name] = [shape[0],0]
			if len(shape) == 2:
				output += ' [%sx%s]</th>' % (shape[0], shape[1])
				mapping[name] = [shape[0],shape[1]]
	output += '</tr>'

	# Then table data.
	rowNumber = 0
	for row in table.iterrows():
		
		# Create the truncated row version
		output += '<tr id="row-%s">' % rowNumber
		output += '<td><button type="button" class="btn btn-primary" id="row-button-%s">%s</button></td>' % (rowNumber, rowNumber)
		for col in table.colnames:
			# Toggle modal when clicking on a value.
			output += '<td><a data-toggle="modal" data-target="#myModal" href="witables.py?path=%s%s/%s/%s">%s</a></td>' % (activeFile, activeNode, col, rowNumber, truncValue(row[col]))
		output += '</tr>'

		# Create the extended row version
		extendedRowNumber = totalRowNumber + rowNumber
		output += '<tr id="row-%s" style="display:none;">' % extendedRowNumber
		output += '<td><button type="button" class="btn btn-success" id="row-button-%s">%s</button></td>' % (extendedRowNumber, rowNumber)
		for col in table.colnames:
			# Toggle modal when clicking on a value.
			output += '<td><a data-toggle="modal" data-target="#myModal" href="witables.py?path=%s%s/%s/%s">%s</a></td>' % (activeFile, activeNode, col, rowNumber, extendValue(row[col], mapping[col]))
		output += '</tr>'

		rowNumber += 1
	output += '</table>'

	return output

def rowJavascript(table):

	totalRowNumber = table.nrows
	output = '''
	$('button.btn.btn-primary').click(function () {
		// Parse Id to get row number	
		var id = $(this).attr('id').replace('row-button-','');
		$('#row-' + id).hide();
		
		idInt = parseInt(id) + %s
		$('#row-' + idInt.toString()).show();
	});

	$('button.btn.btn-success').click(function () {
		// Parse Id to get row number	
		var id = $(this).attr('id').replace('row-button-','');
		$('#row-' + id).hide();
		
		idInt = parseInt(id) - %s
		$('#row-' + idInt.toString()).show();
	});
''' % (totalRowNumber,totalRowNumber)

	# Add jquery script to destroy modal content. This is needed to change the content each time the modal is shown.
	output += '''
	$('body').on('hidden.bs.modal', '.modal', function () {
		console.log("Remove data?");
	  $(this).removeData('bs.modal');
	});
'''

	# Enable toggle buttons.
	output += '''
	$(document).ready(function() {
		$("button#popover-description").popover();
		$("button#popover-type").popover();
	});
'''

	return output

# Show the node as group structure
def selectNode(root, activeFile, activeNode):

	# Set a header for the page.
	output = '<div class="page-header"><h1>Node List of File %s <small>click one to see it</small></h1></div>' % activeFile

	# If an exception occurs we try again
	if not isinstance(root, Group):
		return "<h2>Error. Provided node %s in file %s to selectNode is not a group.</h2>" % (activeFile, activeNode)

	output += '<br><table class="table table-striped"><tr><th>%s Node List</th></tr>' % root

	# Show the groups of the root element and how many nodes they contain.
	nodeIndex = 0
	for node in root._f_iter_nodes():
		if node._f_getattr('CLASS') == "TABLE":
			output += '<tr><td><ul><li><span class="label label-primary">TABLE</span>&nbsp;<a href="witables?path=%s%s"><span class="badge pull-right">%s</span>%s</a></li></ul></td></tr>' % (activeFile, escape(node._v_pathname), node.nrows, node._v_name)
		else:
			output += '<tr><td><ul><li><span class="label label-primary">%s</span>&nbsp;<a href="witables?path=%s%s"><span class="badge pull-right"><div id="node-%s"></div>%s</span>%s</a></li></ul></td></tr>' % (node._f_getattr('CLASS'), activeFile, escape(node._v_pathname), nodeIndex, spinner(nodeIndex), node._v_name)
			nodeIndex += 1
	output += '</table>'

	return output

def loaderJavascript(root, activeFile, activeNode):

	# If an exception occurs we try again
	if not isinstance(root, Group):
		return "<h2>Error. Provided node %s in file %s to loaderJavascript is not a group.</h2>" % (activeFile, activeNode)

	# Generated javascript output (omit script tag)
	output = ''

	# Show the groups of the root element and how many nodes they contain.
	nodeIndex = 0
	for node in root._f_iter_nodes():

		# Skip tables, the row number can be accessed instantaneously
		if node._f_getattr('CLASS') == "TABLE":
			continue

		output += '''
$("#node-%s").load("childnumber.py?file=%s&path=%s", function() {
$("#spinner-%s").hide();
});''' % (nodeIndex, activeFile, escape(node._v_pathname), nodeIndex)

		nodeIndex += 1

	return output

def selectFile(rootDirectory=''):
	
	# Set a header for the page.
	if rootDirectory == '':
		output = '<div class="page-header"><h1>Scan *.h5 files and directories in folder:root <small>click one to walk its tree</small></h1></div>'
	else:
		output = '<div class="page-header"><h1>Scan *.h5 files and directories in folder: %s <small>click one to walk its tree</small></h1></div>' % rootDirectory

	# Get the list of database files from the directory.
        #fileList = filter(lambda x: x.find('.h5') > -1, os.listdir(filepath + databaseDirectory))
	fileList = os.listdir(filepath + databaseDirectory + '/' + rootDirectory)

	# Sort elements
	directoryList = []
	databaseList = []
	for filename in fileList:
		if os.path.isdir(filepath + databaseDirectory + '/' + rootDirectory + '/' + filename):
			directoryList.append(filename)
		else:
			if filename.find('.h5') > -1:
				databaseList.append(filename)

	output += '<div class="list-group">'	

	for directoryName in directoryList:
		output += '<a href="witables.py?path=%s/%s" class="list-group-item active">%s</a>' % (rootDirectory, directoryName, directoryName)

	for filename in databaseList:
		output += '<a href="witables.py?path=%s/%s" class="list-group-item">%s</a>' % (rootDirectory, filename, filename)

	output += '</div>'

	return output

# Make route and define how we will build the document.
def router(parameterDict):
	
	# Common content.	
	content = {'code':'200', 'title':'WiTables', 'navbar':navbar(parameterDict)}

	# Get the requested path
	if 'path' not in parameterDict.keys():
		# If we ain't got a file, build the body to select one.	
		content['body'] = selectFile()

		# Return content immediately
		return content
	
	# Split path elements.
	pathList = parameterDict['path'][0].split('/')
	
	# Make file path
	databasePath = ''

	# Build the path with the given list.
	for i in range(len(pathList)):
		element = pathList[i]

		# Skip empty element.
		if element == '':
			continue

		# Add element to the path.
		databasePath += '/' + element

		# If it is not a directory anymore, we stop here.
		if not os.path.isdir(filepath + databaseDirectory + databasePath):
			# Delete elements we consumed to build this path.
			pathList[0:i+1] = []	
			break

		# If we consumed each element without reaching a file, go to the file selector.
		if i == len(pathList) - 1:
			# If we ain't got a file, build the body to select one.	
			content['body'] = selectFile(databasePath)

			# Return content immediately
			return content
			

	# Either we found the file, either it does not exists.
	if not os.path.isfile(filepath + databaseDirectory + databasePath):
		content['code'] = '404'
		content['body'] = "<h2>Could not find the database at location: %s</h2>" % databasePath
		
		# Return content immediately
		return content


	# Yeah, we found the filepath, now we open the database and look for the node path.	
	database = open_file(filepath + databaseDirectory + databasePath, mode = 'r')

	# Get the node with path
	node = database.get_node('/')

	# If an exception occurs we return an error.
	if not isinstance(node, Group):
		content['code'] = '404'
		content['body'] = "<h2>Error while loading root node in file %s in router</h2><p><a href='witables.py?path=%s'>Try again</a></p>" % (databasePath,parameterDict['path'][0])

		# Close database file first, then return error content.
		database.close()
		return content

	# If the path list is empty, directly go to the node selector.
	if pathList == []:
		# If we ain't got a node path, build the body to select one.	
		content['body'] = selectNode(node, databasePath, '/')
		content['javascript'] = loaderJavascript(node, databasePath, '/')

		database.close()
		return content

	nodePath = ''
	# Build the path with the given list.
	for i in range(len(pathList)):
		element = pathList[i]

		# Add element to the path.
		nodePath += '/' + element
		
		# Find the node
		try:
			node = node._f_get_child(element)
		except NoSuchNodeError:
			content['code'] = '404'
			content['body'] = "<h2>Could not find a node at location %s in file %s</h2><p><a href='witables.py?path=%s'>Try again</a></p>" % (nodePath, databasePath, parameterDict['path'][0])
			database.close()
			return content

		# If it is not a group anymore, we stop here.
		if not isinstance(node, Group):
			# Delete elements we consumed to build this path.
			pathList[0:i+1] = []
			break

		# If we consumed each element without reaching a leaf, go to the node selector.
		if i == len(pathList) - 1:
			# If we ain't got a file, build the body to select one.	
			content['body'] = selectNode(node, databasePath, nodePath)
			content['javascript'] = loaderJavascript(node, databasePath, nodePath)

			database.close()
			return content

	
	# If something wrong happened, we return an error.
	if not isinstance(node, Table):
		content['body'] = "<h2>Could not find a table at location %s in file %s</h2><p><a href='witables.py?path=%s'>Try again</a></p>" % (nodePath, databasePath, parameterDict['path'][0])
		database.close()
		return content

	# If the path list is empty, this is a table, go to the data selector.
	if pathList == []:
		content['body'] = selectData(node, databasePath, nodePath)
		content['javascript'] = rowJavascript(node)

		database.close()
		return content
	
	
	# If the list is not empty, next element is a column name.
	colname = pathList.pop(0)
	if pathList == []:
		content['body'] = columnView(node, databasePath, nodePath, colname)
		content['javascript'] = rowJavascript(node)
	
		database.close()
		return content
	
	rowNumber = pathList.pop(0)
	if pathList == []:
		content['modal'] = valueModal(node, databasePath, nodePath, colname, rowNumber)
	
		database.close()
		return content


	# Finally close database in any case.
	database.close()

	# Return extra argument error.
	content['code'] = '400'
	content['body'] = "<h2>Requested location %s in file %s as extra arguments: %s</h2>" % (nodePath, databasePath, pathList)

	return content
	

def application(environ, start_response):
	# Process the parameters if any.
	parameterDict = parse_qs(environ.get('QUERY_STRING', ''))

	# Make route and define how we will build the document.
	content = router(parameterDict)

	if content['code'] != '200':
		return errorPage(content['code'], content['body'], environ, start_response)

	# Make answer header.
	status = content['code'] + ' ' + status_description[content['code']]
	response_headers = [('Content-Type', 'text/html; charset=utf-8')]
	start_response(status, response_headers)

	# Return it.
	return [html(content)]


parameters = {'path':['/temp/test2.h5']}
html(router(parameters))
#print html(router(parameters))
