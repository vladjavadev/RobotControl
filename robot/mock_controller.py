
from core.work import DoWork
import time

speed_mode_max = 4
speed_mode_min = 1


def init():
    print("mockController: Init")

def run(logic):
    task = DoWork(shared=logic, task_func=_check_interrupt, name='check_interrupt')
    task.start()

def _check_interrupt(logic):
    while True:
        time.sleep(1.0)
        print("check_interrupt")
        if logic.is_interrupt:
            print("Interruption")



def clamp_speed(value, default=1):
    if value < speed_mode_min or value > speed_mode_max:
        return default
    return value
    
def turnLeft(speed_mode=1,step=1):
    cM = clamp_speed(speed_mode)

    print("Turning left")



def turnRight(speed_mode=1,step=1):
    cM = clamp_speed(speed_mode)

    print("Turning right")


def forward(speed_mode=1,step=1):

    cM = clamp_speed(speed_mode)
    print("Moving forward")

def reverse(speed_mode=1,step=1):

    cM = clamp_speed(speed_mode)
    print("Moveing reverse")

def stop():
    print("Mock Stop")