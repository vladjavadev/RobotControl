
from dstar.d_star_lite import DStarLite
from dstar.grid import OccupancyGridMap, SLAM
import server as srv
import robot.move_logic as lgc
import time

OBSTACLE = 255
UNOCCUPIED = 0


def run_algorithm(dto):

    """
    set initial values for the map occupancy grid
    |----------> y, column
    |           (x=0,y=2)
    |
    V (x=2, y=0)
    x, row
    """
    x_dim = 10
    y_dim = 10
    start = (1, 1)
    goal = (8, 8)
    view_range = 2


    new_map = dto.world
    
    # Add obstacles
    obstacles = [
        (4, 4), (3, 4), (3, 5),  # Horizontal wall
         (7, 3), (7, 4),  # Another wall
        (5, 7), (6, 7), (7, 7),  # Vertical wall
    ]
    
    # Place obstacles
    for obs in obstacles:
        new_map.set_obstacle(obs)
    
    old_map = new_map

    new_position = start
    last_position = start

    # new_observation = None
    # type = OBSTACLE

    # D* Lite (optimized)
    dstar = DStarLite(map=new_map,
                      s_start=start,
                      s_goal=goal)

    # SLAM to detect vertices
    slam = SLAM(map=new_map,
                view_range=view_range)

    # Initial path planning
    path, g, rhs = dstar.move_and_replan(robot_position=new_position)
    
    if path is None:
        print("No valid path found from start to goal!")
        exit(1)
        
    print(f"Initial path found: {path}")
    
    logic = lgc.Logic(pos=new_position, dir=(0,1), vMode=2)
    for obs in obstacles:
        new_map.set_obstacle(obs)
    # Only proceed if we have a valid path
    if path:
        
        while True:
            time.sleep(1.0)
            dto.set_path(path)
            # update the map
            # print(path)
            # drive gui
            if path[0]==dto.get_goal():
                logic.move_robot(path[0])
                print("Reached goal!")
                break

            new_position = dto.get_position()
            new_observation = dto.observation
            new_map = dto.world

            logic.move_robot(new_position)
            print("current pos", new_position)
            if new_observation is not None:
                old_map = new_map
                slam.set_ground_truth_map(gt_map=new_map)

            print("new_pos and last_pos",new_position,last_position)
            if new_position != last_position:
                last_position = new_position

                # slam
                new_edges_and_old_costs, slam_map = slam.rescan(global_position=new_position)

                dstar.new_edges_and_old_costs = new_edges_and_old_costs
                dstar.sensed_map = slam_map

                # d star

                path, g, rhs = dstar.move_and_replan(robot_position=new_position)

if __name__ == "__main__":
    run_algorithm(srv.g_dt)