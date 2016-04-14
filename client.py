import socket
import demjson

TCP_IP = '10.1.71.92'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = {"reading_type": "GPS", "pod_id": "1", "mac_address": "fe:fe:fe:fe:fe", "ip_address": "192.168.1.9", "time": "2016-04-13 18:45:30", "temp": "98", "luminosity": "85", "acceleration": "1.2", "latitude": "29.3499123", "longitude": "43.1234567"}
json = demjson.encode(MESSAGE)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(json)
data = s.recv(BUFFER_SIZE)
s.close()

print("Send data: ", data)
