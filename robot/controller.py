from robot import kinematic as rk
from robot import motor_driver as rd

speed_mode_max = 4
speed_mode_min = 1


def init():
    rk.init()
    rd.init()


def clamp_speed(value, default=1):
    if value < speed_mode_min or value > speed_mode_max:
        return default
    return value
    
def turnLeft(speed_mode=1,step=1):
    cM = clamp_speed(speed_mode)
    vl = rk.speeds[cM-1]
    turnTime = rk.get_deltaT(vl, 0, 45*step)
    print("Turning left")
    rd.turnLeft(turnTime,cM)
    rd.stop()


def turnRight(speed_mode=1,step=1):
    cM = clamp_speed(speed_mode)
    vr = rk.speeds[cM-1]
    turnTime = rk.get_deltaT(0, vr, 45*step)
    print("Turning right")
    rd.turnRight(turnTime, cM)
    rd.stop()

def forward(speed_mode=1,step=1):
    rd.stop()
    cM = clamp_speed(speed_mode)
    print("Moving forward")
    rd.forward(2*step, cM)
    rd.stop()

def reverse(speed_mode=1,step=1):
    rd.stop()
    cM = clamp_speed(speed_mode)
    print("Moveing reverse")
    rd.reverse(2*step, cM)
    rd.stop()

def stop():
    rd.stop()