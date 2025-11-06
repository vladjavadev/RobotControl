import numpy as np
from robot.RobotMotorDriver import duty_levels
import math

T = 0.6#s
wheelRadius = 30 #mm
vLinearMax = 2*3.14*wheelRadius/T #mm/s
speeds = [vLinearMax * d/100 for d in duty_levels]
LwheelBase = 150 #mm
Kdc = 0.7


def get_deltaT(vL, vR, deg):
    omega = (vR - vL)/LwheelBase
    turnRad = math.radians(deg)
    absOmega = abs(omega)
    deltaT = turnRad/absOmega
    return deltaT

def get_robot_turn(vL, vR, deltaT):
    irc= (vL+vR)*LwheelBase/(2*(vR - vL))
    omega = (vR - vL)/LwheelBase
    dOmega = omega*deltaT
    return dOmega, irc


def calcRobotPos(x, y,curTeta, dOmega, irc):
    x0 = x - irc*math.sin(curTeta)
    y0 = y + irc*math.cos(curTeta)

    irc_v = np.array([[x0][y0]])
    P_old = np.array([[x],[y]])
    P_offset =  P_old - irc_v

    cos_dt = math.cos(dOmega)
    sin_dt = math.sin(dOmega)
    R_dt = np.array([[cos_dt, -sin_dt], [sin_dt, cos_dt]])
    P_new = np.dot(R_dt, P_offset) + irc_v

    x1 = P_new[0][0]
    y1 = P_new[1][0]
    return x1, y1

