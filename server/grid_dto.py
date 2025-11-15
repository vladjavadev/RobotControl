from dstar.grid import OccupancyGridMap 
from threading import Lock
class GridDto:
    def __init__(self,
                 x_dim=10,
                 y_dim=10,
                 start=(1, 1),
                 goal=(8, 8),
                 viewing_range=3):
        
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.start = start
        self.current = start
        self.observation = {"pos": None, "type": None}
        self.goal = goal
        self.viewing_range = viewing_range
        self.path = None
        self._lock = Lock()


        self.world = OccupancyGridMap(x_dim=x_dim,
                                      y_dim=y_dim,
                                      exploration_setting='8N')


    def set_path(self, path=None):
        self.path = path
    def get_path(self):
        with self._lock:
            return self.path
    
    def get_position(self):
        return self.current

    def set_position(self, pos: (int, int)):
        with self._lock:
            self.current = pos

    def get_goal(self):
        return self.goal

    def set_goal(self, goal: (int, int)):
        self.goal = goal

    def set_start(self, start: (int, int)):
        self.start = start

    def set_obs(self, grid_cell: (int, int)):
        with self._lock:
            if self.world.is_unoccupied(grid_cell):
                self.world.set_obstacle(grid_cell)
                self.observation = {"pos": grid_cell, "type": "OBSTACLE"}

    def rem_obs(self, grid_cell: (int, int)):
        with self._lock:
            if not self.world.is_unoccupied(grid_cell):
                print("grid cell: ".format(grid_cell))
                self.world.remove_obstacle(grid_cell)
                self.observation = {"pos": grid_cell, "type": "UNOCCUPIED"}