import numpy as np
import math


rps = [1.1,1.55,1.6,1.62,1.7]
wheelRadius = 30 #mm
speeds = []
LwheelBase = 150 #mm



def init():
    global speeds
    speeds =[2*3.14*wheelRadius*i for i in rps ]

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

    irc_v = np.array([[int(x0)],[int(y0)]])
    P_old = np.array([[int(x)],[int(y)]])
    P_offset =  P_old - irc_v

    cos_dt = math.cos(dOmega)
    sin_dt = math.sin(dOmega)
    R_dt = np.array([[cos_dt, -sin_dt], [sin_dt, cos_dt]])
    P_new = np.dot(R_dt, P_offset) + irc_v

    x1 = P_new[0][0]
    y1 = P_new[1][0]
    return x1, y1

