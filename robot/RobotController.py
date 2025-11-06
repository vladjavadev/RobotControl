from robot import RobotKinematic as rk
from robot import RobotMotorDriver as rd

speed_mode_max = 4
speed_mode_min = 1


def init():
    rd.init()


def clamp_speed(value, default=1):
    if value < speed_mode_min or value > speed_mode_max:
        return default
    return value
    
def turnLeft(speed_mode=1):
    cM = clamp_speed(speed_mode)
    vl = rk.speeds[cM-1]
    turnTime = rk.get_deltaT(vl, 0, 90)
    print("Turning left")
    rd.turnLeft(turnTime)
    rd.stop()


def turnRight(speed_mode=1):
    cM = clamp_speed(speed_mode)
    vr = rk.speeds[cM-1]
    turnTime = rk.get_deltaT(0, vr, 90)
    print("Turning right")
    rd.turnRight(turnTime)
    rd.stop()

def forward(speed_mode=1):
    rd.stop()
    cM = clamp_speed(speed_mode)
    print("Moving forward")
    rd.forward(cM)

def reverse(speed_mode=1):
    rd.stop()
    cM = clamp_speed(speed_mode)
    print("Moveing reverse")
    rd.reverse(cM)

def stop():
    rd.stop()