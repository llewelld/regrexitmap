#!bin/python

import json
import urllib2
from random import randint
from os import getcwd

fileout = "wpc-small-0.125.js"

response = urllib2.urlopen('file://'  + getcwd() + '/wpc-small-0.25.js')
boundaries = response.read()

data = json.loads(boundaries)

features = data["features"]

originaltotal = 0;
proportiontoremove = 0.5
totalcoords = 0;
numbertoremain = 0

def removerandompoints():
	select = randint(1,totalcoords)
	#print "Selected: {}".format(select)
	count = 0

	# Select a coordinate vector
	coordselect = 0
	featureselect = 0
	while (featureselect < len(features)) and (count < select):
		feature = features[featureselect]
		geometry = feature["geometry"]["coordinates"]
		polytype = feature["geometry"]["type"]

		if polytype == "Polygon":
			polyselect = 0
			while (polyselect < len(geometry)) and (count < select):
				polygon = geometry[polyselect]
				if (count + len(polygon)) > select:
					coordselect = select - count
					count = select
				else:
					count += len(polygon)
				if (count < select):
					polyselect += 1
				
		elif polytype == "MultiPolygon":
			thingselect = 0
			while (thingselect < len(geometry)) and (count < select):
				thing = geometry[thingselect]
				polyselect = 0
				while (polyselect < len(thing)) and (count < select):
					polygon = thing[polyselect]
					if (count + len(polygon)) > select:
						coordselect = select - count
						count = select
					else:
						count += len(polygon)
					if (count < select):
						polyselect += 1
				if (count < select):
					thingselect += 1
		else:
			print "Error"
		if (count < select):
			featureselect += 1

	# Pick out the coordinates and its neighbourhood
	remove = True
	coord = [[],[],[]]
	polytype = features[featureselect]["geometry"]["type"]
	if polytype == "Polygon":
		polygon = features[featureselect]["geometry"]["coordinates"][polyselect]
		coord[0] = polygon[(coordselect - 1) % len(polygon)]
		coord[1] = polygon[coordselect]
		coord[2] = polygon[(coordselect + 1) % len(polygon)]
		if len(polygon) < 3:
			remove = False
	elif polytype == "MultiPolygon":
		polygon = features[featureselect]["geometry"]["coordinates"][thingselect][polyselect]
		coord[0] = polygon[(coordselect - 1) % len(polygon)]
		coord[1] = polygon[coordselect]
		coord[2] = polygon[(coordselect + 1) % len(polygon)]
		if len(polygon) < 3:
			remove = False
	else:
		print "Error"




	# Check if the point appears anywhere else
	# but with a different neighbourhood
	found = 0
	removable = remove
	for feature in features:
		geometry = feature["geometry"]["coordinates"]
		polytype = feature["geometry"]["type"]
		if polytype == "Polygon":
			for polygon in geometry:
				coordcount = 0
				for point in range(0, len(polygon)):
					if (polygon[point][0] == coord[1][0]) and (polygon[point][1] == coord[1][1]):
						pre = polygon[(point - 1) % len(polygon)]
						post = polygon[(point + 1) % len(polygon)]
						if ((pre[0] != coord[0][0]) or (pre[1] != coord[0][1])) and ((pre[0] != coord[2][0]) or (pre[1] != coord[2][1])):
							removable = False
						elif ((post[0] != coord[0][0]) or (post[1] != coord[0][1])) and ((post[0] != coord[2][0]) or (post[1] != coord[2][1])):
							removable = False
						else:
							found += 1
		elif polytype == "MultiPolygon":
			for thing in geometry:
				for polygon in thing:
					coordcount = 0
					for point in range(0, len(polygon)):
						if (polygon[point][0] == coord[1][0]) and (polygon[point][1] == coord[1][1]):
							pre = polygon[(point - 1) % len(polygon)]
							post = polygon[(point + 1) % len(polygon)]
							if ((pre[0] != coord[0][0]) or (pre[1] != coord[0][1])) and ((pre[0] != coord[2][0]) or (pre[1] != coord[2][1])):
								removable = False
							elif ((post[0] != coord[0][0]) or (post[1] != coord[0][1])) and ((post[0] != coord[2][0]) or (post[1] != coord[2][1])):
								removable = False
							else:
								found += 1
		else:
			print "Error"

	#print "Removable: {}, found: {}".format(removable, found)

	# If the point is removable, remove all instances of it
	removed = 0
	if removable == True:
		for feature in features:
			geometry = feature["geometry"]["coordinates"]
			polytype = feature["geometry"]["type"]
			if polytype == "Polygon":
				for polygon in geometry:
					toremove = polygon.count(coord[1])
					if (toremove > 0):
						polygon.remove(coord[1])
					removed += toremove
			elif polytype == "MultiPolygon":
				for thing in geometry:
					for polygon in thing:
						toremove = polygon.count(coord[1])
						if (toremove > 0):
							polygon.remove(coord[1])
						removed += toremove
			else:
				print "Error"

	#print "Removed: {}".format(removed)
	return removed


def counttotalcoords():
	count = 0
	for feature in features:
		geometry = feature["geometry"]["coordinates"]
		polytype = feature["geometry"]["type"]
	
		if polytype == "Polygon":
			for polygon in geometry:
				count += len(polygon)
		elif polytype == "MultiPolygon":
			for thing in geometry:
				for polygon in thing:
					count += len(polygon)
		else:
			print "Error"
	return count


totalcoords = counttotalcoords()
originaltotal = totalcoords
numbertoremain = totalcoords - (totalcoords * proportiontoremove)

print "Total coordinates: {}".format(totalcoords)
print "Remain at most: {}".format(numbertoremain)

while totalcoords > numbertoremain:
	totalcoords -= removerandompoints()
	print "Remaining: {}".format(totalcoords / (0.0 + originaltotal))

out = json.dumps(data)

with open(fileout, "w") as text_file:
	text_file.write(out)

