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


