#!/usr/bin/python

import sys
from xml.dom import minidom

def getPlacemarks(filename):
    xmldoc = minidom.parse(filename)

    elements = []
    for p in xmldoc.getElementsByTagName("Placemark"):
        elements.append(p)

    placemarks = []
    for e in elements:
        if len(e.childNodes) < 7: continue
        if len(e.childNodes[6].childNodes) < 6: continue
        if len(e.childNodes[6].childNodes[5].childNodes) < 1: continue
        if e.childNodes[6].childNodes[5].childNodes[0].data.count(",") != 2: continue
        placemarks.append(e.childNodes[6].childNodes[5].childNodes[0].data)
    return placemarks

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: " + sys.argv[0] + " file.kml"
        sys.exit()

    filename = sys.argv[1]
    placemarks = getPlacemarks(filename)
    print "Read", len(placemarks), "points."

    selection = {}
    tp = raw_input("Specify individual or ranges of trackpoints to export.\n")
    while tp != "":
        arr = tp.split('-')
        if len(arr) == 1:
            selection[int(arr[0])] = True
            print "Added", arr[0], "to the selection."
        elif len(arr) == 2:
            start = int(arr[0])
            end = int(arr[1])
            if start > end:
                x = start
                start = end
                end = x
            for x in range(start, end+1):
                selection[x] = True
            print "Added", start, "-", end, "to the selection."
        elif len(arr) == 3:
            start = int(arr[0])
            every = int(arr[1])
            end = int(arr[2])
            if start > end:
                x = start
                start = end
                end = x
            for x in range(start, end+1, every):
                selection[x] = True
            print "Added every", str(every) + "th", "between", start, "and", end, "to the selection."
        
        print ""
        tp = raw_input("Specify individual or ranges of trackpoints to export.\n")
        
    formatString = raw_input("Specify the format of the outpute string, [lat] for latitude, [lng] for longitude, [alt] for altitude.\n")
    filename = raw_input("Specify the filename to write to.\n")

    handle = open(filename, 'w')

    sKeys = selection.keys()
    sKeys.sort()
    for s in sKeys:
        p = placemarks[s]
        components = p.split(',')
        lat = components[0]
        lng = components[1]
        alt = components[2]
        handle.write(formatString.replace("[lat]", lat).replace("[alt]", alt).replace("[lng]", lng) + "\n")

    print "Done"