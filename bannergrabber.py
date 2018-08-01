#!/usr/bin/python

import socket
import sys

usage = ("Usage: python bannergrabber.py <hostname> <port>")

def logo():
	print ("#"*25)
	print ("#"+" "*9+"@n1c_Fury"+" "*9+"#")
	print ("#"*25)

def scan(THOST, TPORT)
	try:
		for port in TPORT:
			s = socket.socket()
			s.connect((THOST, port))
			s.send("GET / HTTP/1.0\r\n\r\n")							
			banner = s.recv(1024)
			print "\n[+] Banner for port [+] " + str(port) + "\n" + " %s " %banner
	except Exception as e:
			print ('Error: %s') % e
			print ("")

def main():
	if len(sys.argv) == 3:
		THOST = sys.argv[1]			#Specify host name
		TPORT = sys.argv[2]			#Specify Port number
		logo()
	scan(THOST, TPORT)
	else:
		usage()

if __name__ == "__main__":
  main()
