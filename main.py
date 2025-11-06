from robot import RobotController as rc
import sys
import termios
import tty




def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch1 = sys.stdin.read(1)
        if ch1 == '\x1b':  # ESC
            ch2 = sys.stdin.read(1)
            if ch2 == '[':
                ch3 = sys.stdin.read(1)
                return ch3
        else:
            return ch1
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


if __name__ == "__main__":
    rc.init()
    mode = 1
    try:
        while True:
            key = get_key()
            if key == '+':       # ↑
                mode += 1
                print("Speed mode: {}".format(mode))
            if key == '-':       # ↑
                mode -= 1
                print("Speed mode: {}".format(mode))
            if key == 'A':       # ↑
                rc.forward(mode)
            elif key == 'B':     # ↓
                rc.reverse(mode)
            elif key == 'C':     # →
                rc.turnRight(mode)
            elif key == 'D':     # ←
                rc.turnLeft(mode)            
            elif key == ' ':     # ←
                rc.stop()
            elif key == 'q':     # выход
                rc.stop()
                break
    except:
        rc.stop()
