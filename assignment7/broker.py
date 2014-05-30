from network import Listener, Handler, poll



handlers = {}  # map client handler to user name
names = {} # map name to handler
subs = {} # map tag to handlers

def broadcast(msg):
    for h in handlers.keys():
        h.do_send(msg)


class MyHandler(Handler):
    
    def on_open(self):
        handlers[self] = None
        
    def on_close(self):
        name = handlers[self]
        del handlers[self]
        broadcast({'leave': name, 'users': handlers.values()})
        
    def on_msg(self, msg):
        if 'join' in msg:
            name = msg['join']
            handlers[self] = name
            names[name] = self
            broadcast({'join': name, 'users': handlers.values()})
            print msg
        elif 'speak' in msg:
            name, txt = msg['speak'], msg['txt']
            publish = [word[1:] for word in txt.split() if word.startswith("#") ]
            subscribe =  [word[1:] for word in txt.split() if word.startswith("+") ]
            unsubscribe =  [word[1:] for word in txt.split() if word.startswith("-") ]
            private =  [word[1:] for word in txt.split() if word.startswith("@") ]
            if len(subscribe) > 0: #this means that there is a word starting with +
                for s in subscribe:
                    if s in subs:
                        subs[s].append(self)
                    else:
                        subs[s] = [self]
                print "subs"
                print subs
            if len(publish) > 0: #this means that there is a word starting with #
                broadcastTo = []
                for p in publish:
                    if p in subs:
                        for h in subs[p]:
                            broadcastTo.append(h)
                    else:
                        pass
                for h in list(set(broadcastTo)):
                    h.do_send({'speak': name, 'txt': txt})
            if len(unsubscribe) > 0: #this means that there is a word starting with -
                for p in unsubscribe:
                    print p
                    if p in subs:
                        if self in subs[p]:
                            subs[p].remove(self)
                        else:
                            print "not subscribed!"
                    else:
                        pass
            if len(private) > 0: #this means that there is a word starting with @
                names[private[0]].do_send({'speak': name, 'txt': txt})
            elif (len(subscribe) ==0) and (len(publish) == 0) and (len(unsubscribe) == 0) and (len(private)==0): #no subscriptions or publishing
                broadcast({'speak': name, 'txt': txt})



Listener(8888, MyHandler)
while 1:
    poll(0.05)