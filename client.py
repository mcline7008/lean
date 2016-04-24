#!/usr/bin/env python

import socket
import demjson

#Imports for sensors
import smbus
import time
import RPi.GPIO as GPIO
import math
#end imports for sensors

TCP_IP = '10.1.71.92'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = {"reading_type": "GPS", "pod_id": "1", "mac_address": "fe:fe:fe:fe:fe", "ip_address": "192.168.1.9", "time": "2016-04-13 18:45:30", "temp": "98", "luminosity": "85", "acceleration": "1.2", "latitude": "29.3499123", "longitude": "43.1234567"}

#definitions for sensors
bus = smbus.SMBus(1)	#Setup i2c object

luxAddr = 0x39		#Address for the lux sensor with floating ADDR pin
luxCmd = 0x80		#Basic mask for sending a command to sensor
#Last byte selects the register

tmpAddr = 0x1c		#Address for the temperature sensor with A2:0 = 001
tmpPointerByte = 0x05	#Value to be written to the pointer register to read temperature data

accAddr = 0x18		#Address for the accelerometer
accXL_addr = 0x28	#Register for lower X byte
accXH_addr = 0x29	#Register for upper X byte
accYL_addr = 0x2a	#Register for lower Y byte
accYH_addr = 0x2b	#Register for upper Y byte
accZL_addr = 0x2c	#Register for lower Z byte
accZH_addr = 0x2d	#Register for upper Z byte
#end definitions for sensors

#methods for sensors
def GPIOInit():
    GPIO.setwarnings(False)				#Disable warnings
    GPIO.setmode(GPIO.BOARD)			#Set the pin mode to physical numbering
    GPIO.setup(8, GPIO.OUT)				#Set pin as output to power sensors
    GPIO.output(8, GPIO.LOW)			#Remove power from sensors the 3.3v output
    time.sleep(.005)
    GPIO.output(8, GPIO.HIGH)			#Drive the 3.3V output
    time.sleep(3)

def luxInit():
    bus.write_byte_data(luxAddr, 0x80, 0x03)		#Power up sensor
    powerUp = bus.read_byte_data(luxAddr, 0x80)		#Read power up register status
    
    bus.write_byte_data(luxAddr, 0xb1, 0x02)		#Set timing register
    timingRegister = bus.read_byte_data(luxAddr, 0x81)	#Read timing register status

def luxReading():
    luxLow = bus.read_byte_data(luxAddr, 0x8c)		#Read low byte
    luxHigh = bus.read_byte_data(luxAddr, 0x8d)		#Read high byte
    lux = (luxHigh << 8) + (luxLow & 0xff)			#Full lux reading
    
    return lux

def tmpReading():
    tmp = bus.read_word_data(tmpAddr, 0x05)			#Read temperature register
    
    lower = tmp >> 8					#After testing, word gets saved backwards of what would be expected
    upper = (tmp & 0xff) & 0x1f
    
    tmp = (upper * 16.0) + (lower / 16.0)
    
    return tmp

def accInit():
    bus.write_byte_data(accAddr, 0x1f, 0x80)		#enable adc
    bus.write_byte_data(accAddr, 0x20, 0x17)		#set 1Hz refresh rate, enable x, y, z axis
    bus.write_byte_data(accAddr, 0x21, 0x00)		#disable all ctrl reg 2 features
    bus.write_byte_data(accAddr, 0x23, 0x30)		#enable full g range
    bus.write_byte_data(accAddr, 0x21, 0x80)		#Enable filtered data selection

def accReading():
    accXL = bus.read_byte_data(accAddr, accXL_addr)
    accXH = bus.read_byte_data(accAddr, accXH_addr)
    accYL = bus.read_byte_data(accAddr, accYL_addr)
    accYH = bus.read_byte_data(accAddr, accYH_addr)
    accZL = bus.read_byte_data(accAddr, accZL_addr)
    accZH = bus.read_byte_data(accAddr, accZH_addr)
    
    accX = (accXH << 8) + (accXL & 0xff)
    accY = (accYH << 8) + (accYL & 0xff)
    accZ = (accZH << 8) + (accZL & 0xff)
    
    acc = [accX, accY, accZ]
    
    return acc

#end methods for sensors

json = demjson.encode(MESSAGE)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

GPIOInit()
luxInit()
accInit()

luxTime = 0
tmpTime = 0
accTime = 0

time.sleep(.5)

while 1:
    if luxTime == 15:
        lux = luxReading()
        MESSAGE["reading_type"] = "Luminosity"
        MESSAGE["luminosity"] = lux;
        MESSAGE["time"] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        json = demjson.encode(MESSAGE)
        s.send(json)
        luxTime = 0
    
    if tmpTime == 15:
        tmp = tmpReading()
        MESSAGE["reading_type"] = "Temp"
        MESSAGE["temp"] = tmp;
        MESSAGE["time"] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        json = demjson.encode(MESSAGE)
        s.send(json)
        tmpTime = 0
    
    if accTime == 10:
        acc = accReading()
        MESSAGE["reading_type"] = "Accelaration"
        MESSAGE["accelaration"] = acc;
        MESSAGE["time"] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        json = demjson.encode(MESSAGE)
        s.send(json)
        accTime = 0
    
    luxTime += 1
    tmpTime += 1
    accTime += 1
        
        s.send(json)
        data = s.recv(BUFFER_SIZE)
        print "Send data: ", data
    
    time.sleep(1)
#End while loop

s.close()