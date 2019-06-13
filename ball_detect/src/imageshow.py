#!/usr/bin/env python

import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

bridge = CvBridge()
def image_callback(ros_image):
    global bridge

    cv_image = bridge.imgmsg_to_cv2(ros_image, 'bgr8')
    (rows, cols, channels) = cv_image.shape

    cv2.imshow('image', cv_image)
    cv2.waitKey(1)

def main():
    rospy.init_node('imagereceiver', anonymous=True)
    image_sub = rospy.Subscriber('/usb_cam/image_raw/', Image, image_callback)
    rospy.spin()

if __name__ == '__main__':
    main()
