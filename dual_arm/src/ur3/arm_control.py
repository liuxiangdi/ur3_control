import urx
import pickle
import time
from cfg.home_cfg import righthome
import numpy as np
import math3d

class LeftArm():
    def __init__(self):
        self.leftArm = urx.Robot('192.168.1.10')
        left_fp = open('./ur3/cfg/left_ref_cfg', 'rb')
        l_csys = pickle.load(left_fp)
        self.leftArm.set_csys(l_csys)
        self.backhome(True)

    def backhome(self, flag):
        self.leftArm.movej(lefthome, vel=0.2, acc=0.1, wait=flag)
        self.location = [0, 0, 0]
        print('Back To Home')
        print(lefthome)

    def move(self, x, y, z, flag):
        z = -z
        trans = [x-self.location[0], y-self.location[1], z-self.location[2]]
        self.leftArm.translate(trans, vel=0.2, acc=0.1, wait=flag)
        self.location = [x, y, z]
    
    def trans(self, x, y, z, flag):
        trans = [x, y, z]
        self.leftArm.translate(trans, vel=0.1, acc=0.1, wait=flag)
    
    def speedmove(self, maxVal, x, y, z):
        self.leftArm.speedl([x*maxVal, y*maxVal, z*maxVal, 0, 0, 0], 0.1, 0.3)
    
    def movetopix(self, imagewidth, imageheight, pixx, pixy, z, flag):
        ypix_y = 0.8/imagewidth
        xpix_x = 0.6/imageheight

        y = pixx*ypix_y
        x = (imageheight- pixy)*xpix_x
        self.move(x, y, z, flag)

    # negetive when clockwise
    def rotate(self, angle, flag):
        ori = math3d.Orientation()
        ori.rotateZ(angle)
        #reference orientation
        ori_ref = self.leftArm.get_orientation()
        ori_new = ori.__mul__(ori_ref) 
        self.leftArm.set_orientation(ori_new, vel=0.2, acc=0.1, wait=flag)
        print("rotation")

    def close(self):
        self.leftArm.close()

class RightArm():
    def __init__(self):
        self.rightArm = urx.Robot('192.168.1.11')
        right_fp = open('./ur3/cfg/right_ref_cfg.pkl', 'rb')
        r_csys = pickle.load(right_fp)
        self.rightArm.set_csys(r_csys)

    def backhome(self, flag):
        self.rightArm.movej(righthome, vel=0.3, acc=0.1, wait=flag)
        print('Back To Home')
        print(righthome)
        self.location = [0, 0, 0]

    def move(self, x, y, z, flag):
        trans = [x-self.location[0], y-self.location[1], z-self.location[2]]
        self.rightArm.translate(trans, vel=0.2, acc=0.1, wait=flag)
        self.location = [x, y, z]
        print('move to target')
     
    def moves(self, maxVal, x, y, z, min_t):
        self.rightArm.speedl([x*maxVal, y*maxVal, z*maxVal, 0, 0, 0], 0.05, min_t)

    def movetopix(self, imagewidth, imageheight, pixx, pixy, z, flag):
        ypix_y = 0.8/imagewidth
        xpix_x = 0.6/imageheight

        y = (imagewidth - pixx)*ypix_y
        x = (imageheight- pixy)*xpix_x
        self.move(x, y, z, flag)

    # negetive when clockwise
    def rotate(self, angle, flag):
        ori = math3d.Orientation()
        ori.rotateZ(-angle)
        #reference orientation
        ori_ref = self.rightArm.get_orientation()
        ori_new = ori.__mul__(ori_ref) 
        self.rightArm.set_orientation(ori_new, vel=0.2, acc=0.1, wait=flag)
        print("rotation")

    def close(self):
        self.rightArm.close()

if __name__ == '__main__':
    right = RightArm()
    right.backhome(True)
    print('Back To Home')
    '''
    right.moves(0.1, 0.5, 0, 0, 3)
    time.sleep(1)
    right.moves(0.1, 0.3, 0, 0, 3)
    time.sleep(1)
    right.moves(0.1, 0.1, 0, 0, 3)
    print('Move S x++')
    right.moves(0.1, 0, 0.5, 0, 3)
    time.sleep(1)
    right.moves(0.1, 0, 0.2, 0, 3)
    time.sleep(1)
    right.moves(0.1, 0, 0, 0.1, 1)
    print('Move S y++')
    right.moves(0.1, 0, 0, 0.3, 3)
    time.sleep(1)
    right.moves(0.1, 0, 0, 0.2, 3)
    time.sleep(1)
    right.moves(0.1, 0, 0, 0.1, 0.5)
    print('Move S x++')
    '''
    #test max a for smooth move
    v = 0.6
    t = time.time()
    for i in range(30):
        right.moves(0.1, v, 0, 0, 0.5)
        v -= 0.02
        print(time.time() - t)
        t = time.time()
    ##########################################################
    #
    # ur3 robot.sppedl method has a min duration time about 0.1s
    # a = 0.2 m/s^2 is smooth
    #
    ###########################################################
    right.close()
