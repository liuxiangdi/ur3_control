#!/usr/bin/env python
import rospy
import time
import urx
from dual_arm.srv import leftArmState
from std_msgs.msg import Int8
from sensor_msgs.msg import Joy

class State():
    def __init__(self):
        self.state = 'free'
        rospy.init_node('stateServer')
        
        self.state = 'free'
        self.analogval = [0, 0, 0, 0, 0, 0, 0]
        self.time = time.time()
        
        self.lastx = 0
        self.lasty = 0
        self.xvel = 0
        self.yvel = 0
        self.rob = urx.Robot('192.168.1.10')
        self.sub = rospy.Subscriber('/joy', Joy, self.stateWatch)
        self.mainloop()
        

    def stateWatch(self, joymsg):
        if time.time() - self.time > 0.1:
            self.analogval = joymsg.axes
            print(self.analogval)
            
            self.xvel = 0.1*self.analogval[1]*0.5 + self.lastx*0.5
            self.yvel = 0.1*self.analogval[0]*0.5 + self.lasty*0.5
            self.lastx = self.xvel
            self.lasty = self.yvel

    def mainloop(self):
        while True:
            if self.xvel or self.yvel:
                self.rob.speedj([self.xvel, self.yvel, 0 ,0 ,0 ,0], 0.1, 0.5)
            time.sleep(0.1)

if __name__ == '__main__':
    State()
