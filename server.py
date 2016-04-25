#!/usr/bin/env python
# coding: utf-8

import socket
import json
import pprint 
import MySQLdb as mdb
import sys
import demjson

#########################################################
#
# Functions for writing to the database
#
#########################################################
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
	global accX
	global accY
	global accZ

	cur.execute("INSERT INTO acceleration(pod_id, time, acc_x, acc_y, acc_z) VALUES(%s, %s, %s, %s, %s)", (podID, time, accX, accY, accZ))

def addPod():
	global cur
	global podID
	global mac
	global ip

	cur.execute("INSERT INTO pods(pod_id, mac_address, ip_address) VALUES(%s, %s, %s)", (podID, mac, ip))




TCP_IP = '192.168.1.9'
TCP_PORT = 5005
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', TCP_PORT))
s.listen(1)

connection, addr = s.accept()
print 'Connection address: ' , addr
while 1:
	dataFile = connection.recv(BUFFER_SIZE)
	if not dataFile: break
	try:
		data = demjson.decode(dataFile)
	except: print("failed decode")
	print "received data: ", data
	
	podID = data["pod_id"]
	readingType = data["reading_type"]
	mac = data["mac_address"]
	ip = data["ip_address"]
	time = data["time"]
	temp = data["temp"]
	luminosity = data["luminosity"]
	accX = data["acc_x"]
	accY = data["acc_y"]
	accZ = data["acc_z"]
	latitude = data["latitude"]
	longitude = data["longitude"]

	con = mdb.connect('localhost', 'leanuser', 'leanteam', 'leanSensors')
	cur = con.cursor()

	if readingType == "Pod Add":
		addPod()
	elif readingType == "GPS":
		writeGPS()
	elif readingType == "Temp":
		writeTemp()
	elif readingType == "Luminosity":
		writeLuminosity()
	elif readingType == "Acceleration":
		writeAcceleration()

	con.commit()

	con.close()
	
	connection.send("Success!")
connection.close()

