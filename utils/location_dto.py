class LocationDTO:
    def __init__(self):
        self._latest_pos = (0,0)
        self._latest_path = []
        self.goal = (0,0)
        self._timestamp = None

    def update(self, new_pos, new_path,goal):
        self._latest_pos = new_pos
        self._latest_path = new_path
        self.goal=goal

    def get_pos(self):
        return self._latest_pos

    def get_path(self):
        return self._latest_path
    
    def get_goal(self):
        return self.goal

