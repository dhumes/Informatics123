#worked with Rohan Venapusala
from network import Handler, poll
import sys
import os
from threading import Thread
from time import sleep

myname = raw_input('What is your name? ')

class Client(Handler):
    
    def on_close(self):
		os._exit(0)
    
    def on_msg(self, msg):
		print msg
		
        
host, port = 'localhost', 8888
client = Client(host, port)
client.do_send({'join': myname})

def periodic_poll():
    while 1:
        poll()
        sleep(0.05)  # seconds
                            
thread = Thread(target=periodic_poll)
thread.daemon = True  # die when the main thread dies 
thread.start()

while 1:
	try:
	   mytxt = sys.stdin.readline().rstrip()
	   if str(mytxt).lower() == "quit":
		client.do_send({'speak': myname, 'txt': mytxt})
		print("****Disconnected from server**** \n")
		exit()
	   else:
	   	client.do_send({'speak': myname, 'txt': mytxt})
	except KeyboardInterrupt:
		client.do_send({'speak': myname, 'txt': "quit"})
		print("****Disconnected from server**** \n")
		exit()
	except:
		"Looks like your not connected to server"