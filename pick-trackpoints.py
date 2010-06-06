#!/usr/bin/python

import sys
from xml.dom import minidom

def getText(node):
	rc = []
	for child in node.childNodes:
		if child.nodeType == child.TEXT_NODE:
			rc.append(child.data)
	return ''.join(rc)

def getChildTagWithName(domNode, tag, name):
	#print n
	for i in domNode.getElementsByTagName(tag):
		compare = getText(i.getElementsByTagName("name")[0])
		#print compare
		if compare == name:
			#print name
			return i
	return -1

if len(sys.argv) < 2:
	print "Usage: " + sys.argv[0] + " file.kml"
	sys.exit()

fileToParse = sys.argv[1]
xmldoc = minidom.parse(fileToParse)
doc = xmldoc.getElementsByTagName("Document")
folder = getChildTagWithName(doc[0], "Folder", "Tracks")
subfolder = getChildTagWithName(folder, "Folder", "DG-100 tracklog")
points = getChildTagWithName(subfolder, "Folder", "Points")

placemarks = []
for p in points.childNodes:
	if p.nodeType == p.TEXT_NODE:
		continue
	if p.tagName == "Placemark" and getText(p.getElementsByTagName("name")[0]) != "Path":
		placemarks.append(p)
trackpointsRead = len(placemarks)

print "Read " + str(trackpointsRead) + " points."

selection = {}
tp = raw_input("Specify individual or ranges of trackpoints to export.\n")
while tp != "":
	arr = tp.partition('-')
	if arr[2] == "":
		selection[int(arr[0])] = True
		print "Added", arr[0], "to the selection."
	else:
		start = int(arr[0])
		end = int(arr[2])
		if start > end:
			x = start
			start = end
			end = x
		for x in range(start, end+1):
			selection[x] = True
		print "Added", arr[0] + "-" + arr[2], "to the selection."
	
	print ""
	tp = raw_input("Specify individual or ranges of trackpoints to export.\n")
	
formatString = raw_input("Specify the format of the outpute string, [lat] for latitude, [lng] for longitude.\n")
filename = raw_input("Specify the filename to write to.\n")

handle = open(filename, 'w')

sKeys = selection.keys()
sKeys.sort()
for s in sKeys:
	p = placemarks[s]
	name = getText(p.getElementsByTagName("name")[0])
	if int(name.rpartition('-')[2]) != s:
		print "Error '" + name + "' does not match", s
	else:
		lookat = p.getElementsByTagName("LookAt")[0]
		lat = getText(lookat.getElementsByTagName("latitude")[0])
		lng = getText(lookat.getElementsByTagName("longitude")[0])
		handle.write(formatString.replace("[lat]", lat).replace("[lng]", lng) + "\n")

print "Done"