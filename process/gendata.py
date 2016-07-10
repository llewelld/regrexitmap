#!bin/python

import json
import urllib2
from random import randint
from os import getcwd

# Northern Ireland constituencies
# TODO: Factor these out (don't have referendum data for them)
ignorepcon = [
"N06000001", 
"N06000002", 
"N06000003", 
"N06000004", 
"N06000005", 
"N06000006", 
"N06000007", 
"N06000008", 
"N06000009", 
"N06000010", 
"N06000011", 
"N06000012", 
"N06000013", 
"N06000014", 
"N06000015", 
"N06000016", 
"N06000017", 
"N06000018"
]

areas = {}

def getOslauaFromPcon(pcon):
	for oslaua in areas.iterkeys():
		pcons = areas[oslaua]
		if pcon in pcons:
			return oslaua, pcons[pcon]
	return None, None
	
def getOslauaData(oslaua):
	for area in oslauadata:
		if area["gss"] == oslaua:
			return area["name"], area["answers"][0]["votes"], area["answers"][1]["votes"]
	return None, None, None
	

filein = "PostcodesData/nspd_2015_11.csv"
with open(filein, "r") as text_file:
	# Skip the header line
	line = text_file.readline()
	#print line
	while line:
		line = text_file.readline()
		if line:
			line = line.rstrip()
			data = line.split(',')
			oslaua = data[3]
			pcon = data[7]
			if oslaua in areas:
				if pcon in areas[oslaua]:
					areas[oslaua][pcon] += 1
				else:
					areas[oslaua][pcon] = 1
			else:
				areas[oslaua] = {}
				areas[oslaua][pcon] = 1

	#print "OSLAUA, PCON, proportion"
	for oslaua in areas.iterkeys():
		total = 0
		pcons = areas[oslaua]
		for pcon in pcons.iterkeys():
			total += pcons[pcon]

		for pcon in pcons.iterkeys():
			share = (0.0 + pcons[pcon]) / total
			pcons[pcon] = share


lines = {}
pcondata = {}

response = urllib2.urlopen('file://' + getcwd() + '/petition.json')
petition = response.read()

pcondata = json.loads(petition)

totalsignature = 0
constituencies = pcondata["data"]["attributes"]["signatures_by_constituency"]
for constituency in constituencies:
	totalsignature += constituency["signature_count"]


response = urllib2.urlopen('file://' + getcwd() + '/results.json')
results = response.read()

oslauadata = json.loads(results)

totalremain = 0
constituencies = oslauadata
for constituency in constituencies:
	if constituency["answers"][0]["shortText"] == "Remain":
		totalremain += constituency["answers"][0]["votes"]
	elif constituency["answers"][1]["shortText"] == "Remain":
		totalremain += constituency["answers"][1]["votes"]
		print "Reversed"
	else:
		print "Error: no Remain shortText"

#print "Total signatures {}".format(totalsignature)
#print "Total votes {}".format(totalremain)

#print '"{}", "{}", "{}", "{}", "{}"'.format("PCON", "OSLAUA", "Change", "Expected sigs", "Actual sigs")

results = dict()
constituencies = pcondata["data"]["attributes"]["signatures_by_constituency"]
for constituency in constituencies:
	name = constituency["name"].encode('utf-8').strip()
	code = constituency["ons_code"].encode('utf-8').strip()
	mp = constituency["mp"]
	sigs = constituency["signature_count"]

	oslaua, proportion = getOslauaFromPcon(code)
	if oslaua == None:
		print "No proportion"
	else:
		oslauaname, remain, leave = getOslauaData(oslaua)
		if oslauaname == None:
			change = 1.0
			#print "No OSLAUA: {}, {}, {}".format(oslauaname, oslaua, code)
		else:
			signatures = constituency["signature_count"]
		
			pconremain = remain * proportion
			pconleave = leave * proportion
			expectedsigs = (pconremain * totalsignature) / totalremain
		
			change = (0.0 + signatures) / expectedsigs
		
			#print '"{}", "{}", {}, {}, {}'.format(name, oslauaname, change, expectedsigs, signatures)
			results[code] = dict()
			results[code]["name"] = name
			results[code]["loa"] = oslauaname
			results[code]["change"] = change
			results[code]["remain"] = int(round(pconremain))
			results[code]["leave"] = int(round(pconleave))
			results[code]["mp"] = mp
			results[code]["sigs"] = sigs

#print results
print(json.dumps(results, sort_keys=False, indent=2))





#constituencies = pcondata["data"]["attributes"]["signatures_by_constituency"]
#for constituency in constituencies:
#	totalsignature += constituency["signature_count"]
#	name = constituency["name"].encode('utf-8').strip()
#	code = constituency["ons_code"].encode('utf-8').strip()
#	lines[name] = '"{}", "{}"'.format(name, code)

#constituencies = oslauadata
#for constituency in constituencies:
#	name = constituency["name"].encode('utf-8').strip()
#	code = constituency["gss"].encode('utf-8').strip()
#	if name in lines:
#		lines[name] = '{}, "{}"'.format(lines[name], code)
#	else:
#		lines[name] = '"{}", "", "{}"'.format(name, code)


