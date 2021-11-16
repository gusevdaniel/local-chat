import socket, threading, time

port = 9090

def client(IP):
    server = (IP,port)

    shutdown = False
    join = False

    def receive (name, sock):
	    while not shutdown:
		    try:
			    while True:
				    data, addr = sock.recvfrom(1024)
				    print(data.decode("utf-8"))

				    time.sleep(0.2)
		    except:
			    pass

    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.connect(server)
    s.setblocking(0)

    alias = input("Name: ")

    rT = threading.Thread(target = receive, args = ("RecvThread",s))
    rT.start()

    while shutdown == False:
	    if join == False:
		    s.sendto(("["+alias + "] => join chat ").encode("utf-8"),server)
		    join = True
	    else:
		    try:
			    message = input()

			    if message != "":
				    s.sendto(("["+alias + "] :: "+message).encode("utf-8"),server)
			
			    time.sleep(0.2)
		    except:
			    s.sendto(("["+alias + "] <= left chat ").encode("utf-8"),server)
			    shutdown = True

    rT.join()
    s.close()

def server():
    host = socket.gethostbyname(socket.gethostname())

    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind((host,port))

    print("IP Server: " + host)

    print("[ Server Started ]")

    clients = []
    quit = False

    while not quit:
	    try:
		    data, addr = s.recvfrom(1024)

		    if addr not in clients:
			    clients.append(addr)

		    itsatime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())

		    print("["+addr[0]+"]=["+str(addr[1])+"]=["+itsatime+"]/",end="")
		    print(data.decode("utf-8"))

		    for client in clients:
			    if addr != client:
				    s.sendto(data,client)
	    except:	
		    print("\n[ Server Stopped ]")
		    quit = True
		
    s.close()

answerFlag = True

while answerFlag:
    print ("What do you want to start? [client/server]")
    answer = input()
    if answer == "client":
        answerFlag = False
        print ("Server IP?")
        IP = input()
        client(IP)
    if answer == "server":
        answerFlag = False
        server()
