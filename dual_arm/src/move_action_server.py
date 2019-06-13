#!/usr/bin/env python

import rospy
import time
import actionlib
from ur3.arm_control import RightArm
from dual_arm.msg import movetoAction, movetoResult

#relative move
class MoveToAction():
    def __init__(self):
        rospy.init_node('move_action')
        self.arm = RightArm()
        self.state = 0
        self.server = actionlib.SimpleActionServer('move_action_server', movetoAction, self.moves, False)


        self.server.start()
        rospy.spin()

    def moves(self, moveinfo):
        start_time = time.time()
        mode = moveinfo.mode
        if mode == 1:
            self.arm.backhome(True)
            result = movetoResult()
            result.state = 1
            self.server.set_succeeded(result)
            print('back to home')

        elif mode == 2:
            speed_x = moveinfo.x
            speed_y = moveinfo.y
            speed_z = moveinfo.z
            maxVal = 0.1

            self.arm.moves(maxVal, speed_x, speed_y, speed_z, 0.4)

            result = movetoResult()
            result.state = 1
            self.server.set_succeeded(result)
            print('move to {}'.format(moveinfo))
        elif mode == 10:
            print('break')
            self.arm.close()

if __name__ == '__main__':
    move = MoveToAction()
