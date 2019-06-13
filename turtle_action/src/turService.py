#!/usr/bin/env python
import rospy
from turtle_action.srv import turtleSrv

def cal(request):
    x = request.x
    y = request.y
    tarx = request.tarx
    tary = request.tary
    return float(tarx - x), float(tary - y)

rospy.init_node('service_server')
service = rospy.Service('turtleVal', turtleSrv, cal)
rospy.spin()
