# from robot import controller as rc
from robot import motion_accum as mcc



DIRECTIONS = [
    (0, 1),    # 0: N
    (1, 1),    # 1: NE
    (1, 0),    # 2: E
    (1, -1),   # 3: SE
    (0, -1),   # 4: S
    (-1, -1),  # 5: SW
    (-1, 0),   # 6: W
    (-1, 1)    # 7: NW
]



mAObj = mcc.MotionAccumulator()
mAObj.dir = (0,1)

class Logic:
    def __init__(self, pos=(0, 0), dir=(0,0), vMode = 3):
        self.dir = dir
        self.pos = pos
        self.vMode = vMode
        # rc.init()



    def move_robot(self, path, pos):
        if mAObj.pos != pos:
            mAObj.path = path
            mAObj.pos = pos
            mAObj.accumulateMotion()
            trajectory = mAObj.get_trajectory()
            print(trajectory)
            mAObj.old_path = path

            for node in trajectory:
                if node.rotateStep > 0:
                    if node.side == "right":
                        print("Turn right: ",node.rotateStep)
                        # rc.turnRight(self.vMode,node.rotateStep)
                    elif node.side == "left":
                        print("Turn left: ",node.rotateStep)
                        # rc.turnLeft(self.vMode,node.rotateStep)
                if node.moveStep>0:
                    print("move forward: ",node.moveStep)
                    # rc.forward(self.vMode, node.moveStep)
            mAObj.trjList = []


    





