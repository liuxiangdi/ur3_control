#!/usr/bin/env python

import rospy
import actionlib
import time
from std_msgs.msg import Int8
from sensor_msgs.msg import Joy
from dual_arm.msg import movetoAction, movetoGoal

class Grasp():
    
    def __init__(self):
        rospy.init_node('grasp')
        self.move_client = actionlib.SimpleActionClient('move_action_server', movetoAction)
        self.goal = movetoGoal()
        print('wait for move server')
        self.move_client.wait_for_server()
        print('move action server success')
        sub = rospy.Subscriber('arm_state', Int8, self.updateState)
        
        self.analogsub = rospy.Subscriber('/joy', Joy, self.updateVal)
        
        self.contorl_time = 0
        self.xvel = 0
        self.yvel = 0
        self.lastx = 0
        self.lasty = 0
        self.state = 0
        self.laststate = 0

        self.mainloop()

    def updateState(self, msg):
        self.laststate = self.state
        self.state = msg.data
        print('update state {}'.format(self.state))
    
    def updateVal(self, msg):
        self.analogval = msg.axes
        self.xvel = self.analogval[1]
        self.yvel = self.analogval[0]
    
        if abs(self.analogval[1]) < 0.3:
            self.xvel = 0
        if abs(self.analogval[0]) <0.3:
            self.yvel = 0

    def mainloop(self):
        while self.state != 10:
            if self.state == 1 and not self.goal.mode:
                self.goal.mode = 1
                self.move_client.send_goal(self.goal)
                self.move_client.wait_for_result()
                print('result : {}'.format(self.move_client.get_result()))
            elif self.state == 2 and self.goal.mode != 2:
                self.goal.mode = 2
                print('----- unlock ----- \n FreeMove')

            if self.goal.mode == 2:
                maxdv = (time.time() - self.contorl_time)*0.2
                self.control_time = time.time()
                if abs(self.xvel - self.goal.x) > maxdv:
                    self.goal.x = self.goal.x + maxdv if self.xvel > self.goal.x else self.goal.x - maxdv
                else:
                    self.goal.x = self.xvel
                
                if abs(self.yvel - self.goal.y) > maxdv:
                    self.goal.y = self.goal.y + maxdv if self.xvel > self.goal.y else self.goal.y - maxdv
                else:
                    self.goal.y = self.yvel
                self.goal.z = 0
                self.move_client.send_goal(self.goal)
                print('send move speed {}'.format(self.goal))
                time.sleep(0.1)

if __name__ == '__main__':
    Grasp()
