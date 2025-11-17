from robot import kinematic as rk
# from robot import motor_driver as rd
from data.grid_dto import GridDto
import time


class Controller:
    speed_mode_max = 4
    speed_mode_min = 1
    unit = 0.5#time in seconds to accross grid cell
    ix=0

    def __init__(self, dto:GridDto):
        self.dto=dto
        rk.init()


    def clamp_speed(self, value, default=1):
        if value < self.speed_mode_min or value > self.speed_mode_max:
            return default
        return value
        
    def turnLeft(self, speed_mode=1,step=1):
        cM = self.clamp_speed(speed_mode)
        vl = rk.speeds[cM-1]
        turnTime = rk.get_deltaT(vl, 0, 45*step)
        print("Turning left")
        time.sleep(turnTime)


    def turnRight(self, speed_mode=1,step=1):
        cM = self.clamp_speed(speed_mode)
        vr = rk.speeds[cM-1]
        turnTime = rk.get_deltaT(0, vr, 45*step)
        print("Turning right")
        time.sleep(turnTime)
 

    def forward(self, speed_mode=1):
        cM = self.clamp_speed(speed_mode)
        print("!!!Move forward")
        time.sleep(self.unit)


    def reverse(self, speed_mode=1):
        cM = self.clamp_speed(speed_mode)
        time.sleep(self.unit)

    def stop(self):
        print("RD stop")