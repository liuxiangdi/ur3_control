import numpy as np
import urx

def rightArmRecord():
    right = urx.Robot('192.168.1.11')

    pose = right.getj()

    fp = open('right_home.py', 'w')

    entry = 'home = ' + str(pose) + '\n'
    fp.write(entry)
    print(entry)
    fp.close()

    right.close()

def leftArmRecord():
    left = urx.Robot('192.168.1.10')

    pose = left.getj()

    fp = open('left_home.py', 'w')

    entry = 'home = ' + str(pose) + '\n'
    fp.write(entry)
    print(entry)
    fp.close()

    left.close()

if __name__ == "__main__":
    rightArmRecord()
