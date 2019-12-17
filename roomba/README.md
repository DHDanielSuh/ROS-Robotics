# Roomba Assignment

### Description

* The robot avoids obstacles and provides the ability to move.
* When a robot encounters an obstacle, the robot rotates and avoids it.

### Algorithm
* Subscribing laser scan data.
* Rotate() function, publishing 'cmd_vel'. is implemented.
* Move() function, publishing 'cmd_vel'. is implemented.
* min_range_index() function is implemented.
* max_range_index() function is implemented.
* average_range() function is implemented.
* average_between_indices() function is implemented.
  
### Test Flow

0. Opening simulator
```console
  $ roslaunch turtlebot3_gazebo turtlebot3_world.launch (or roslaunch turtlebot3_gazebo turtlebot3_stage_3.launch)
```
1. Initiate roomba program
```console
  $ cd {DIRECTORY OF roomba.py}
  $ ./roomba.py
```
2. Check output in both terminal and simulator.
