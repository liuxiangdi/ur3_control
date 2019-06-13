#!/usr/bin/env python

import rospy
import time
import actionlib
from ur3.armcontrol import LeftArm
from dual_arm.msg import movetoAction, movetoResult

#relative move
class MoveToAction():
    def __init__(self):
        rospy.init_node('movej_action_test')

        self.leftArm = LeftArm()
        self.state = 0
        
        self.server = actionlib.SimpleActionServer('moveto', movetoAction, self.movej, False)
        self.server.start()
        rospy.spin()

    def movej(self, moveinfo):
        start_time = time.time()
        mode = moveinfo.mode
        if mode == 0:
            self.leftArm.backhome(True)

            result = movetoResult()
            result.state = 1
            self.server.set_succeeded(result)
            print('back to home')

        elif mode == 1:
            speed_x = moveinfo.x
            speed_y = moveinfo.y
            speed_z = moveinfo.z
            maxVal = 0.1

            self.leftArm.speedmove(maxVal, speed_x, speed_y, speed_z)

            result = movetoResult()
            result.state = 1
            self.server.set_succeeded(result)
            print('move to {}'.format(moveinfo))
        elif mode == 10:
            print('break')
            self.leftArm.close()

if __name__ == '__main__':
    move = MoveToAction()
