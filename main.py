from dstar.d_star_lite import DStarLite
from dstar.grid import OccupancyGridMap, SLAM
from robot.move_logic import Logic
import numpy as np

OBSTACLE = 255
UNOCCUPIED = 0

if __name__ == '__main__':
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
    view_range = 1

    # Initialize the map
    new_map = OccupancyGridMap(x_dim=x_dim,
                              y_dim=y_dim,
                              exploration_setting='8N')
    
    # Add obstacles
    obstacles = [
        (3, 3), (3, 4), (3, 5),  # Horizontal wall
        (7, 2), (7, 3), (7, 4),  # Another wall
        (5, 7), (6, 7), (7, 7),  # Vertical wall
    ]
    
    # Place obstacles
    for obs in obstacles:
        new_map.occupancy_grid_map[obs[0]][obs[1]] = OBSTACLE
    
    # Add terrain weights (1.0 is normal, higher values are harder to traverse)
    difficult_terrain = [
        ((2, 2), 2.0),   # Muddy area
        ((4, 4), 1.5),   # Rocky terrain
        ((6, 6), 3.0),   # Very difficult terrain
        ((8, 2), 2.5),   # Rough patch
    ]
    
    # Set terrain weights
    for pos, weight in difficult_terrain:
        new_map.weight_map[pos[0]][pos[1]] = weight
        
    old_map = new_map

    new_position = start
    last_position = start

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
    
    # Initialize robot control logic with start position and initial direction (North)
    logic = Logic(pos=new_position, dir=(0,1), vMode=2)
    
    # Only proceed if we have a valid path
    if path:
        for step in path:
            # Update robot position
            new_position = step
            new_observation = None
            
            # Send movement commands to the robot
            logic.move_robot(path, new_position)

            if new_observation is not None:
                old_map = new_map
                slam.set_ground_truth_map(gt_map=new_map)

            if new_position != last_position:
                last_position = new_position

                # Update SLAM map
                new_edges_and_old_costs, slam_map = slam.rescan(global_position=new_position)
                dstar.new_edges_and_old_costs = new_edges_and_old_costs
                dstar.sensed_map = slam_map

                # Replan path if needed
                path, g, rhs = dstar.move_and_replan(robot_position=new_position)
                
                if path is None:
                    print("Lost path to goal! Stopping robot.")
                    break
                
                print(f"New path segment: {path}")