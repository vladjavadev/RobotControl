# from robot import controller as rc



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



class Logic:
    def __init__(self, pos=(0, 0), dir=(0,0), vMode = 3):
        self.dir = dir
        self.pos = pos
        self.vMode = vMode
        # rc.init()

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

    def move_robot(self, new_pos):
        new_dir = self.get_dir(new_pos)
        print("<!---move_robot\n","current dir:", self.dir, "new dir:", new_dir)
        if new_dir != self.dir:
            if new_dir == (0,0):
                print("No movement detected.")
                return
            turns = self.turns_needed(self.dir, new_dir)
            turn_side = ""
            if turns[1] == "right":
                turn_side = "right"
                # rotateFunc = rc.turnRight
            else:
                turn_side = "left"
                # rotateFunc = rc.turnLeft

            for _ in range(turns[0]):
                # if turns[1] == "right":
                #     print("Turning right num:", turns[0])
                #     rc.turnRight(self.vMode)
                # else:
                #     print("Turning left num:", turns[0])
                #     rc.turnLeft(self.vMode)
                print("Turning {} num: {}".format(turn_side, turns[0]))
                # rotateFunc(self.vMode)

        # rc.forward(self.vMode)
        self.update_dir_pos(new_pos, new_dir)



    def get_dir(self, pos):
        delta_x = pos[0] - self.pos[0]
        delta_y = pos[1] - self.pos[1]
        print("***get_dir***")
        print("delta_x:", delta_x, "delta_y:", delta_y)
        return (delta_x, delta_y)

