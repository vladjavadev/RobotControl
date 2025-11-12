from robot import mock_controller as rc
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
        self.old_trajectory = []
        self.is_interrupt = False
        rc.init()
        rc.run(self)


              
    def is_sub_trj(self,trj,sub_trj):
        size_s = len(sub_trj)
        if len(trj)<size_s or len(trj)==0:
            return False
        for i,el in enumerate(trj[size_s-1::1]):
            if(el!=sub_trj[i]):
                return False
        return True
    
    def move_robot(self, trajectory):
        for node in trajectory:
            if node.rotateStep > 0:
                if node.side == "right":
                    print("Turn right: ",node.rotateStep)
                    rc.turnRight(self.vMode,node.rotateStep)
                elif node.side == "left":
                    print("Turn left: ",node.rotateStep)
                    rc.turnLeft(self.vMode,node.rotateStep)
            if node.moveStep>0:
                print("move forward: ",node.moveStep)
                rc.forward(self.vMode, node.moveStep)
            if self.is_interrupt:
                mAObj.trjList = []
                return
        mAObj.trjList = []
            
    def build_route(self, path, pos):
        if mAObj.pos != pos:
            mAObj.path = path
            mAObj.pos = pos
            mAObj.accumulateMotion()
            mAObj.print_trajectory()
            trajectory = mAObj.get_trajectory()
            mAObj.old_path = path

            self.move_robot(trajectory=trajectory)




    





