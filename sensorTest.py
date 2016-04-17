# coding=UTF-8

import smbus
import time
import RPi.GPIO as GPIO
import math
import sys
import curses
import locale

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

def GPIOInit():
	GPIO.setwarnings(False)				#Disable warnings
	GPIO.setmode(GPIO.BOARD)			#Set the pin mode to physical numbering
	GPIO.setup(8, GPIO.OUT)				#Set pin as output to power sensors
	GPIO.output(8, GPIO.LOW)			#Remove power from sensors the 3.3v output
	time.sleep(.005)
	GPIO.output(8, GPIO.HIGH)			#Drive the 3.3V output
	time.sleep(.005)

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

def updateScreen(lux, tmp, acc, luxT, tmpT, accT):
	luxT_remaining = 15 - luxT
	tmpT_remaining = 15 - tmpT
	accT_remaining = 10 - accT

	return "Lux Magnitude: {0:d}, updating in {5:d} \nTemperature: {1:.4f} degreeC, updating in {6:d} \nX : {2:d}\tY : {3:d}\tZ : {4:d}, updating in {7:d}".format(lux, tmp, acc[0], acc[1], acc[2], luxT_remaining, tmpT_remaining, accT_remaining)
	
stdscr = curses.initscr()
curses.noecho()
curses.curs_set(0)
curses.halfdelay(1)
stdscr.keypad(1)
curses.resizeterm(12, 50)
stdscr.clear()
stdscr.addstr(0,0, "Initializing Program")

GPIOInit()
luxInit()

luxTime = 0
tmpTime = 0
accTime = 0

time.sleep(.5)

lux = luxReading()
tmp = tmpReading()
acc = accReading()

while True:
	event = stdscr.getch()
	if event == ord("q"):
		GPIO.output(8, GPIO.LOW)
		curses.beep()
		break
	if luxTime == 15:
		lux = luxReading()
		luxTime = 0

	if tmpTime == 15:
		tmp = tmpReading()
		tmpTime = 0
	
	if accTime == 10:
		acc = accReading()
		accTime = 0

	luxTime += 1
	tmpTime += 1
	accTime += 1

	stdscr.clear()
	stdscr.addstr(0,0,updateScreen(lux, tmp, acc, luxTime, tmpTime, accTime))
	time.sleep(1)

curses.endwin()
