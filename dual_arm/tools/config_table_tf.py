import urx
import pickle

def rightArmCord():
    r = urx.Robot('192.168.1.11')
    r.new_csys_from_xpy()

    fp = open('right_ref_cfg.pkl', 'wb')
    pickle.dump(r.csys, fp)
    fp.close()
    r.close()

def leftArmCord():
    l = urx.Robot('192.168.1.10')
    l.new_csys_from_xpy()

    fp = open('left_ref_cfg.pkl', 'wb')
    pickle.dump(l.csys, fp)
    fp.close()
    l.close()

if __name__ == '__main__':
    rightArmCord()
