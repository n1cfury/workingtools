import socket, sys

usage = "Usage: python banner.py <hostname>"

def banner():
	print "#####################################"
	print "#   Banner Grabber  by: n1cfury     #"
	print "#####################################"
	print ""

def portscan(hostname,ports):
	try:
		for port in ports:
			s = socket.socket()
			s.connect((hostname, port))
			s.send("GET / HTTP/1.0\r\n\r\n")							
			banner = s.recv(1024)
			print "\n[+] Banner for port [+] " + str(port) + "\n" + " %s " %banner
	except Exception, e:
			print 'Error: %s' % e
			print "\n"				

def main():
	if len(sys.argv) == 2:
		hostname = sys.argv[1]
		ports = [21,80,443,8080,83]
		banner()
		portscan(hostname,ports)
	else:
		print usage

if __name__ == "__main__":
  main()