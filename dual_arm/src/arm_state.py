#!/usr/bin/env python
import rospy
from dual_arm.srv import leftArmState
from std_msgs.msg import Int8
from sensor_msgs.msg import Joy


class State():
    def __init__(self):
        rospy.init_node('stateWatcher')
        self.key = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.sub = rospy.Subscriber('/joy', Joy, self.stateWatch)
        self.pub = rospy.Publisher('arm_state', Int8, queue_size=1)
        self.state = -1
        rospy.spin()

    def update(self, request):
        print('Update State')
        state = request.state
        self.pub.publish(state)
        return 
    
    def stateWatch(self, joymsg):
        if joymsg.buttons[0] == 1 and self.key[0] == 0:
            print('\n----- right arm back to home mode ------')
            if self.state != 1:
                self.state = 1
            self.pub.publish(1)
        if joymsg.buttons[7] == 1 and self.key[7] == 0:
            print('\n------ right arm unlock ------')
            if self.state != 2:
                self.state = 2
            self.pub.publish(2)
        if joymsg.buttons[6] == 1 and self.key[6] == 0:
            print('\n------ right arm driver off ------')
            if self.state != 10:
                self.state = 10
            self.pub.publish(10)

        self.key = joymsg.buttons

if __name__ == '__main__':
    State()
