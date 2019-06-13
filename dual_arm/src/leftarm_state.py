#!/usr/bin/env python
import rospy
from dual_arm.srv import leftArmState
from std_msgs.msg import Int8
from sensor_msgs.msg import Joy


class State():
    def __init__(self):
        self.state = 'free'
        rospy.init_node('stateServer')
        
        self.state = 'free'
        self.key = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.analogval = [0, 0, 0, 0, 0, 0, 0]

        self.sub = rospy.Subscriber('/joy', Joy, self.stateWatch)
        self.pub = rospy.Publisher('left_arm_state', Int8, queue_size=1)
        self.service = rospy.Service('update_leftarmtate', leftArmState, self.update)
        rospy.spin()

    def update(self, request):
        print('update leftArmState')
        state = request.state
        self.pub.publish(state)
        return 
    
    def stateWatch(self, joymsg):
        if joymsg.buttons[0] == 1 and self.key[0] == 0:
            print('----- start ------')
            self.pub.publish(1)
        if joymsg.buttons[7] == 1 and self.key[7] == 0:
            print('------ unlock ------')
            print('free move mode')
            self.pub.publish(2)
        self.key = joymsg.buttons

if __name__ == '__main__':
    State()
