#!/usr/bin/env python

import rospy
from turtle_action.srv import turtleSrv

rospy.init_node('service')
rospy.wait_for_service('turtleVal')

turtlenode = rospy.ServiceProxy('turtleVal', turtleSrv)

ans = turtlenode(1,1,2,3)
print(ans)
