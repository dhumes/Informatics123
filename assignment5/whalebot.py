import random
from time import sleep
from common import Model

            
################### CONTROLLER #############################

class Controller():
    def __init__(self, m):
        self.m = m
    
    def poll(self):
        # Q2
        # command = random.choice(self.m.cmd_directions.keys())
        # if command:
        #     self.m.do_cmd(command)
        cmd = None
        for p in self.m.pellets:
            cmd = None
            px = p[0]
            py = p[1]
            whalex = self.m.mybox[0]
            whaley = self.m.mybox[1]
            # print ("Position: " +str(self.m.mybox[0]) +", "+ str(self.m.mybox[1]))
            # print "px" + str(px)
            # print "py" + str(py)
            if whalex == px and whaley == py:
                pass
            if whalex < px:
                self.m.do_cmd('right')
                cmd = 'right'
            if whaley > py:
                cmd = 'up'
                # print "going up"
            if whaley < py:
                cmd = 'down'
                # print "going down"
            if whalex > px:
                cmd = 'left'
                # print "going left"
        if cmd:
            self.m.do_cmd(cmd)


################### VIEW #############################

class View():
    def __init__(self, m):
        self.m = m
        self._frameCounter = 0
        
    def display(self):
        b = self.m.mybox
        self._frameCounter += 1
        if self._frameCounter == 50:
            print("Position: " + str(b[0]) + ", " + str(b[1]))
            self._frameCounter = 0

    
################### LOOP #############################

model = Model()
c = Controller(model)
v = View(model)

while not model.game_over:
    sleep(0.02)
    c.poll()
    model.update()
    v.display()