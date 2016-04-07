#!/usr/bin/env python

import socket
import demjson

TCP_IP = '192.168.1.9'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = [{"a": 1, "c": 3, "b": 2, "e": 5, "d": 4}]
json = demjson.encode(MESSAGE)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(json)
data = s.recv(BUFFER_SIZE)
s.close()

print "Send data: ", data
