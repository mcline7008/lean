#!/usr/bin/env python

import socket
import demjson
import json

TCP_IP = '192.168.1.9'
TCP_PORT = 5005
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print 'Connection address: ' , addr
while 1:
	data = conn.recv(BUFFER_SIZE)
	if not data: break
	obj = demjson.decode(data)
	print "received data: ", obj
	with open('data.txt', 'w') as outfile:
		json.dump(obj, outfile)
	conn.send(data)
conn.close()
