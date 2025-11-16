from robot import kinematic as rk
from robot import motor_driver as rd
from server.grid_dto import GridDto
import time


class MockController:
    speed_mode_max = 4
    speed_mode_min = 1
    unit = 2#time in seconds to accross grid cell
    ix=0

    def __init__(self, dto:GridDto):
        self.dto=dto
        rk.init()
        rd.init()


    def clamp_speed(self, value, default=1):
        if value < self.speed_mode_min or value > self.speed_mode_max:
            return default
        return value
        
    def turnLeft(self, speed_mode=1,step=1):
        cM = self.clamp_speed(speed_mode)
        vl = rk.speeds[cM-1]
        turnTime = rk.get_deltaT(vl, 0, 45*step)
        print(f"Turning left{turnTime}")
        rd.turnLeft(turnTime,cM)
        rd.stop()


    def turnRight(self, speed_mode=1,step=1):
        cM = self.clamp_speed(speed_mode)
        vr = rk.speeds[cM-1]
        turnTime = rk.get_deltaT(0, vr, 45*step)
        print(f"Turning right{turnTime}")
        rd.turnRight(turnTime, cM)
        rd.stop()

    def forward(self, speed_mode=1):
        cM = self.clamp_speed(speed_mode)
        print("!!!Move forward")
        rd.forward(cM)
        time.sleep(self.unit)

    def reverse(self,speed_mode=1):
        cM = self.clamp_speed(speed_mode)
        print("Moveing reverse")
        rd.reverse(cM)
        time.sleep(self.unit)


    def stop(self):
        rd.stop()
        print("RD stop")