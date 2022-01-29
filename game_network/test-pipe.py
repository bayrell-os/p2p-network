#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io, os, sys, datetime, random, subprocess, threading, fcntl, pty, time, random

current_dir = os.path.dirname(os.path.realpath(__file__))
#print(current_dir)


def process_output(stdout:io.TextIOWrapper):
	while True:		
		out = stdout.read(5)
		#stdout.
		
		print (out, end="")
		#print (out, end='')
		#print ("\r", end='')
		#print ("random=" + str(random.random()), end='')
		#print ("\r" + "random=" + str(random.random()), end='')		
		
		#print ( str(ord(out)) + " ", end='')
		#print (out + ",code=" + str(ord(out)))
		sys.stdout.flush()
	
script_name = "test-app.py"
print ("Run " + current_dir + '/' + script_name)


# Start thread
first, second = pty.openpty()
stdout = io.open(first, 'r', encoding='UTF-8', newline='\n')
p1 = threading.Thread(target=process_output, args=(stdout,))
p1.daemon = True
p1.start()

# Start app
def start_app():
	proc = subprocess.Popen(
		[current_dir + '/' + script_name, "a", "b"],
		#shell=True,
		stdout=second, 
		stderr=second, 
		close_fds=True, 
		bufsize=0
	)

	while True:
		output_result = proc.poll()
		if (output_result == 0):
			break
		time.sleep(1)


print ("Start app 1")

start_app()

print ("Start app 2")

start_app()


print ("End")
sys.exit()