#!/usr/bin/env python

import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import copy

bridge = CvBridge()
def image_callback(ros_image):
    global bridge

    cv_image = bridge.imgmsg_to_cv2(ros_image, 'bgr8')
    (rows, cols, channels) = cv_image.shape

    cv_image = colorfilter(cv_image)

    cv2.imshow('image', cv_image)
    cv2.waitKey(3)


def colorfilter(image):
    image_raw = copy.deepcopy(image)
    if image is not None:
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower = (18, 20, 102)
        upper = (36, 40, 255)
        
        mask = cv2.inRange(hsv, lower, upper)
        res = cv2.bitwise_and(image, image, mask=mask)
        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)

        contours, heriachy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            if w*h > 500:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0,0,255), 2)

        return image


def main():
    rospy.init_node('imagereceiver', anonymous=True)
    image_sub = rospy.Subscriber('/usb_cam/image_raw/', Image, image_callback)
    rospy.spin()

if __name__ == '__main__':
    main()
