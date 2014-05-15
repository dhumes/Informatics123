import sys
from random import choice
from time import sleep
from random import randint
from network import Handler, poll
from pygame.event import get as get_pygame_events
from pygame.display import set_mode, update as update_pygame_display
from pygame import Rect, init as init_pygame
from pygame.draw import rect as draw_rect
import os

def collide_boxes(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    return x1 < x2 + w2 and y1 < y2 + h2 and x2 < x1 + w1 and y2 < y1 + h1
    

################### CONTROLLER #############################

class NetworkController():
    def __init__(self, m):
        self.m = m
        self.cmds = ['up', 'down', 'left', 'right']

       
    def poll(self):
       poll() 
       if len(self.m.players) > 0:
          p = self.m.pellets[0]  # always target the first pellet
          b = self.m.mybox
          if p[0] > b[0]:
              cmd = 'right'
          elif p[0] + p[2] < b[0]: # p[2] to avoid stuttering left-right movement
              cmd = 'left'
          elif p[1] > b[1]:
              cmd = 'down'
          else:
              cmd = 'up'
          msg = {'input': cmd}
          self.m.do_send(msg)
        


################### CONSOLE VIEW #############################

class ConsoleView():
    def __init__(self, m):
        self.m = m
        self._frameCounter = 0
        
    def display(self):
        self._frameCounter += 1
        if self._frameCounter == 50:
            for name, p in self.m.players.items():
              print "Position " + str(self.m.players[self.m.myname][0]) + ", " + str(self.m.players[self.m.myname][1])
              self._frameCounter = 0



################### MODEL ##################################

class Model(Handler):

    cmd_directions = {'up': (0, -1),
                      'down': (0, 1),
                      'left': (-1, 0),
                      'right': (1, 0)}


    def __init__(self):
        Handler.__init__(self,'localhost', 8888)
        print "Server is connected."
        self.players = {}
        self.borders = [[0, 0, 2, 300],
                        [0, 0, 400, 2],
                        [398, 0, 2, 300],
                        [0, 298, 400, 2]]
        self.pellets = [ [randint(10, 380), randint(10, 280), 5, 5] 
                        for _ in range(4) ]
        self.myname = None
        self.game_over = False
        self.mydir = self.cmd_directions['down']  # start direction: down
        self.mybox = [200, 150, 10, 10]  # start in middle of the screen

    def make_rect(self, quad):  # make a pygame.Rect from a list of 4 integers
        x, y, w, h = quad
        return Rect(x, y, w, h)
        
    def on_close(self):
        print "Server has been closed."
        os._exit(0)
    
    def on_msg(self, data):
        self.players = {name: self.make_rect(player) for name, player in data['players'].items()}
        self.myname = data['myname']
        self.borders = [self.make_rect(border) for border in data['borders']]
        self.pellets = [self.make_rect(pellet) for pellet in data['pellets']]

    def update(self):
        # move me
        self.mybox[0] += self.mydir[0]
        self.mybox[1] += self.mydir[1]
        # potential collision with a border
        for b in self.borders:
            if collide_boxes(self.mybox, b):
                self.mybox = [200, 150, 10, 10]
        # potential collision with a pellet
        for index, pellet in enumerate(self.pellets):
            if collide_boxes(self.mybox, pellet):
                print "ate pellet"
                self.mybox[2] *= 1.2
                self.mybox[3] *= 1.2
                self.pellets[index] = [randint(10, 380), randint(10, 280), 5, 5]
            

################### LOOP #############################
model = Model()
c = NetworkController(model)
v = ConsoleView(model)

while 1:
    sleep(0.02)
    c.poll()
    model.update()
    v.display()

