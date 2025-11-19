from robot import kinematic as rk
# from robot import motor_driver as rd
from data.grid_dto import GridDto
import time
import math

class Controller:
    speed_mode_max = 4
    speed_mode_min = 1
    unit = 500#mm

    

    def __init__(self, dto:GridDto):
        self.totalDistance = 0
        self.dto=dto
        rk.init()


    def clamp_speed(self, value, default=1):
        if value < self.speed_mode_min or value > self.speed_mode_max:
            return default
        return value
        
    def turnLeft(self, speed_mode=1,step=1):
        self.dto._lock_dist.acquire()
        cM = self.clamp_speed(speed_mode)
        vl = rk.speeds[cM-1]
        turnTime = rk.get_deltaT(vl, 0, 45*step)

        dOmega, irc = rk.get_robot_turn(vl,0,turnTime)
        x1, y1 =rk.calcRobotPos(0,0,0,dOmega,irc)
        dist=math.sqrt(x1**2 + y1**2)
        print(f"<<<< LEFT New POS(x:{x1},y:{y1})")
        print(f"<<<< Distance {dist} mm")
        print("Turning left")
        time.sleep(turnTime)
        self.totalDistance+=dist
        self.dto._lock_dist.release()


    def turnRight(self, speed_mode=1,step=1):
        self.dto._lock_dist.acquire()
        
        cM = self.clamp_speed(speed_mode)
        vr = rk.speeds[cM-1]
        turnTime = rk.get_deltaT(0, vr, 45*step)

        dOmega, irc = rk.get_robot_turn(0,vr,turnTime)
        x1, y1 =rk.calcRobotPos(0,0,0,dOmega,irc)
        dist=math.sqrt(x1**2 + y1**2)
        print(f"<<<< RIGHT New POS(x:{x1},y:{y1})")
        print(f"<<<< Distance {dist} mm")
        print("Turning right")
        time.sleep(turnTime)
        self.totalDistance+=dist
        self.dto._lock_dist.release()

 

    def forward(self, speed_mode=1):
        self.dto._lock_dist.acquire()

        cM = self.clamp_speed(speed_mode)
        print("!!!Move forward")
        timeSleep = self.unit/rk.speeds[cM]
        time.sleep(timeSleep)
        self.totalDistance+=self.unit
        self.dto._lock_dist.release()



    def reverse(self, speed_mode=1):
        self.dto._lock_dist.acquire()

        cM = self.clamp_speed(speed_mode)
        timeSleep = self.unit/rk.speeds[cM]
        time.sleep(timeSleep)
        self.totalDistance+=self.unit
        self.dto._lock_dist.release()

    
    def stop(self):
        print("RD stop")