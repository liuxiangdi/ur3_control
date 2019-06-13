#!/usr/bin/env python

import rospy
import time
from turtle_action.msg import movetoAction

def actionServer(tar):
    start_time = time.time()
    tarx = tar.tarx
    tary = tar.tary
    x = tar.x
    y = tar.y
    
    xvel = tarx - x
    yvel = tary -y

    result = rospy.Duration.from_sec(time.time() - start_time)
    server.set_succeeded(result)

if __name__ == '__main__':
    rospy.init_node('action_server')
    server = actionlib.SIimpleActioServer('moveto', movetoAction, actionServer, False) 
    server.start()
    rospy.spin()
