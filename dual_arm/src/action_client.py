#!/usr/bin/env python

import rospy
import actionlib
import time
from dual_arm.msg import movetoAction, movetoGoal

def move_client():
    rospy.init_node('moveto_client')
    client = actionlib.SimpleActionClient('moveto', movetoAction)
    client.wait_for_server()
    
    print('get action server')
    goal = movetoGoal()
    #mode 0 mean back to home, mode 1 mean relative move
    goal.mode = 0
    goal.x = 0.1
    goal.y = 0
    goal.z = 0
    client.send_goal(goal)
    client.wait_for_result()
    print('result : {}'.format(client.get_result()))
    
    for i in range(5):
        goal.mode = 1
        goal.x = 0.5
        goal.y = 0
        goal.z = 0
        client.send_goal(goal)
        time.sleep(0.5)
    for i in range(5):
        goal.x = 0
        goal.y = 0.5
        goal.z = 0
        client.send_goal(goal)
        time.sleep(0.5)
    for i in range(5):
        goal.x = 0
        goal.y = 0
        goal.z = 0.5
        client.send_goal(goal)
        time.sleep(0.5)


    goal.mode = 10
    goal.x = 0
    goal.y = 0
    goal.z = 0
    client.send_goal(goal)


if __name__ == '__main__':
    move_client()
