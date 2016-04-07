#!/usr/bin/python
# coding: utf-8

import json
import pprint 
import MySQLdb as mdb
import sys

def writeGPS():
	global cur
	global podID
	global time
	global latitude
	global longitude

	cur.execute("INSERT INTO gps(pod_id, time, latitude, longitude) VALUES(%s, %s, %s, %s)", (podID, time, latitude, longitude))

def writeTemp():
	global cur
	global podID
	global time
	global temp

	cur.execute("INSERT INTO temp(pod_id, time, temp) VALUES(%s, %s, %s)", (podID, time, temp))

def writeLuminosity():
	global cur
	global podID
	global time
	global luminosity

	cur.execute("INSERT INTO luminosity(pod_id, time, luminosity) VALUES(%s, %s, %s)", (podID, time, luminosity))

def writeAcceleration():
	global cur 
	global podID
	global time
	global acceleration

	cur.execute("INSERT INTO acceleration(pod_id, time, acceleration) VALUES(%s, %s, %s)", (podID, time, acceleration))

def addPod():
	global cur
	global podID
	global mac
	global ip

	cur.execute("INSERT INTO pods(pod_id, mac_address, ip_address) VALUES(%s, %s, %s)", (podID, mac, ip))

dataFile = open("test.json")
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

