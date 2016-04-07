#!/usr/bin/python
# coding: utf-8

import json
import pprint from pprint
import MySQLdb as mdb
import sys

def writeGPS():
	global cur
	global podID
	global time
	global latitude
	global longitude

	cur.execute("INSERT INTO gps(pod_id, time, latitude, longitude) VALUES(%s, %s, %s, %s)", (podID, time, latitude, longitude))

dataFile = open("data.json")
data = json.load(dataFile)

podID = data["pod_id"]
mac = data["mac_address"]
ip = data["ip_address"]
time = data["time"]
temp = data["temp"]
luminosity = data["luminosity"]
acceleration = data["acceleration"]
latitude = data["latitude"]
longitude = data["longitude"]

con = mdb.connect('localhost', 'leanuser', 'leanteam', 'leanSensors')
cur = con.cursor()

