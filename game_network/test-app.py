#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, datetime, random, asyncio,  subprocess, threading, fcntl, pty, time


#mylist = [1,2,3,4,5,6,7,8]

#bar = IncrementalBar('Countdown', max = len(mylist))

#for item in mylist:
#    bar.next()
#    time.sleep(1)

#bar.finish()



import sys, time


print (sys.argv)

print ("Start")
print ("Begin")

#arr = [ 10, 105, 61, 48, 10, 105, 61, 49, 10, 105, 61, 50, 10, 105, 61, 51, 10, 105, 61, 52, 10, 105, 61, 53 ]
arr = [ "\r", "i", "=", "1", "\r", "i", "=", "2", "\r", "i", "=", "3", "\r", "i", "=", "4", "\r", "i", "=", "5", ]

for i in arr:
  
  c = ord(i)
  s = chr(c)
  
  print ( s, end='' )
  #print ( str(c) + " ", end='' )
  
  #print ("\r{}%".format(i), end='')
  #print ("\r", end='')
  #print ("i=" + str(i), end='')
  
  sys.stdout.flush()
  time.sleep(0.1)
  
pass