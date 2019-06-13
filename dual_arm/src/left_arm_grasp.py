#!/usr/bin/env python

import rospy
import actionlib
import time
from std_msgs.msg import Int8
from sensor_msgs.msg import Joy
from dual_arm.msg import movetoAction, movetoGoal

class Grasp():
    
    def __init__(self):
        self.state = 0
        rospy.init_node('grasp')

        self.move_client = actionlib.SimpleActionClient('moveto', movetoAction)
        self.goal = movetoGoal()
        print('wait for move server')
        self.move_client.wait_for_server()
        print('move action server success')
        sub = rospy.Subscriber('left_arm_state', Int8, self.updateState)
        
        self.analogsub = rospy.Subscriber('/joy', Joy, self.updateVal)
        
        self.time = 0
        self.xvel = 0
        self.yvel = 0
        self.lastx = 0
        self.lasty = 0

        self.mainloop()

    def updateState(self, msg):
        self.state = msg.data
        print('update state {}'.format(self.state))
    
    def updateVal(self, msg):
        if time.time() - self.time > 0.1:
            self.analogval = msg.axes
            self.xvel = 0.1*self.analogval[1]*0.5 + self.lastx*0.5
            self.yvel = 0.1*self.analogval[0]*0.5 + self.lasty*0.5
        
            self.lastx = self.xvel
            self.lasty = self.yvel
            if self.analogval[1] == 0:
                self.xvel = 0
            if self.analogval[0] == 0:
                self.yvel = 0
            self.time = time.time()

    def mainloop(self):
        while self.state != 10:
            if self.state == 1:
                print('back to home')
                self.goal.mode = 0
                self.move_client.send_goal(self.goal)
                self.move_client.wait_for_result()
                print('result : {}'.format(self.move_client.get_result()))
            elif self.state == 2 and self.goal.mode == 0:
                self.goal.mode = 1
                print('----- unlock ----- \n FreeMove')
            if self.goal.mode == 1:
                self.goal.x = self.xvel
                self.goal.y = self.yvel
                self.goal.z = 0
                self.move_client.send_goal(self.goal)
                print('send move speed {}'.format(self.goal))
                time.sleep(0.1)


if __name__ == '__main__':
    Grasp()
