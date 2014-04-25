#worked with Rohan Venapusala
from network import Listener, Handler, poll
from time import sleep


handlers = {}  # map client handler to user name

def getUsers():
	userString = []
	for i in sorted(handlers):
		userString.append(str(handlers[i]))
	userlist = ','.join([str(item) for item in userString])
	return userlist
		
		
class MyHandler(Handler):
    def on_open(self):
		pass
        
    def on_close(self):
        pass
    
    def on_msg(self, msg):
		if "join" in msg:
			#add in check for the same
			handlers[self] = str(msg["join"])
			for i in handlers:
				i.do_send(str(msg["join"]) + " joined. Users:" + getUsers())
		elif "txt" in msg:
			if str(msg["txt"]).lower() == "quit":
				del handlers[self]
				for i in handlers:
					i.do_send(str(msg["speak"]) + " left the room. Users:" + getUsers())
			else:
				for i in handlers:
					if i != self:
						i.do_send(str(msg["speak"]) + ": " + msg["txt"])
    
class Serv(Listener):
    handlerClass = MyHandler


port = 8888
server = Serv(port)
while 1:
	try:
	    poll()
	    sleep(0.05)  # seconds
	except KeyboardInterrupt:
		for i in handlers:
			i.do_close()
		server.close()
		exit("\n")

