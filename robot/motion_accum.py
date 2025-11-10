

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


class TrUnit:
    def __init__(self,side: str,rotateStep:int, moveStep:int):
        self.side=side
        self.moveStep=moveStep
        self.rotateStep = rotateStep

class MotionAccumulator:
    path=None
    old_path=None
    trjList:list[TrUnit] = None
    pos=None

    def __init__(self):
        self.path=None
        
    def start(self):
        while True:
            if self.path != self.old_path:
                self.accumulateMotion()
                 

    def accumulateMotion(self):
        moveStep = 0
        needAccum = True
        for i in range(1,len(self.path)):
            self.cur_pos = self.path[i-1]
            new_pos = self.path[i]
            new_dir = self.get_dir(new_pos)
            
            if new_dir != self.dir:
                needAccum = not needAccum
                if new_dir == (0,0):
                    print("No movement detected.")
                    return
                if needAccum:
                    TrUnit(side=turns[1],rotateStep=turns[0],moveStep=moveStep)
                    moveStep=0

                turns = self.turns_needed(self.dir, new_dir)
            else:
                needAccum = not needAccum
                if needAccum:
                    TrUnit(side=turns[1],rotateStep=turns[0],moveStep=moveStep)
                moveStep += 1



            # rc.forward(self.vMode)
            self.update_dir_pos(new_pos, new_dir)


    def get_dir(self, pos):
        delta_x = pos[0] - self.pos[0]
        delta_y = pos[1] - self.pos[1]
        print("***get_dir***")
        print("delta_x:", delta_x, "delta_y:", delta_y)
        return (delta_x, delta_y)
    
    def get_dir_ix(self, vector):
        for i, dir_vec in enumerate(DIRECTIONS):
            if vector == dir_vec:
                return i
        raise ValueError("Вектор не соответствует допустимому направлению")


    def turns_needed(self, start_vec, target_vec):
        start_idx = self.get_dir_ix(start_vec)
        target_idx = self.get_dir_ix(target_vec)

        spinL = (target_idx - start_idx) % 8
        spinR = (start_idx - target_idx) % 8
        print(">>>tn>>>r:", spinR, "l:", spinL)
        turns = (spinR, "right") if spinR <= spinL else (spinL, "left")
        print("===turns_needed***", turns)
        return turns

    def update_dir_pos(self, new_pos, new_dir): 
        self.pos = new_pos 
        self.dir = new_dir