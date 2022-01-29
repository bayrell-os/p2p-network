# -*- coding: utf-8 -*-

import base64, binascii, json, time, hashlib, os, sys, random

from PyQt5.QtNetwork import QUdpSocket, QHostAddress


def test1():
	
	host = QHostAddress("::ffff:127.0.0.1")
	host = QHostAddress("127.0.0.1")
	
	#host.
	
	print( host.toIPv4Address() )
	print( host.toIPv6Address() )
	print( host.toString() )
	

def test2():
	
	remove_list = []
	remove_list.append(50)
	remove_list.append(10)
	
	for index in remove_list:
		print(index)
	
	
def test3():
	
	for index in range(1, 0, -1):
		print(index)
	

def append(s, msg):
	return s + msg + "\n"

	
def test4():
	
	s = ""
	s = append(s, "Test 1")
	s = append(s, "Test 2")
	s = append(s, "Test 3")
	s = append(s, "Test 4")
	s = append(s, "Test 5")
	s = append(s, "Test 6")
	s = append(s, "Test 7")
	
	lines = s.split("\n")
	lines = lines[-6:-1]
	s2 = "\n".join(lines)
	
	print (s2)
	print (len(lines))
	
	
def test5():
	
	ip1 = random.randint(0,200)
	ip2 = random.randint(0,200)
	ip = "10.5." + str(ip1) + "." + str(ip2)
	
	print ( ip )
	
	
	
	
#test5()
#test4()

#print( os.path.curdir )

#print( sys.base_prefix )

client_ip = "10.5.11.22"
print ( client_ip[0:3] == "10." )

#print( sys.platform[0:5] == "linux" )
#print( sys.platform[0:5] == "win32" )
#if sys.platform == "win32"
