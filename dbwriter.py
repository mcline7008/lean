#!/usr/bin/python
# coding: utf-8

import MySQLdb as mdb
import sys

con = mdb.connect('localhost', 'leanuser', 'leanteam', 'leanSensors')
cur = con.cursor()

cur.execute("SHOW TABLES")

tables = cur.fetchall()

for table in tables:
	print table
	
