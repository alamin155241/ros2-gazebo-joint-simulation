# ROS 2 Gazebo Joint Simulation

A ROS 2 Humble / Gazebo Classic learning project with a prismatic slider and a two-axis universal-joint robot. URDF models, ros2_control configuration, launch files and Python command adapters are included.

## Run in a ROS 2 workspace

Use a Linux environment with ROS 2 Humble, Gazebo Classic, rosdep and colcon installed. Clone this repository into a workspace's `src/` directory. From the workspace root:

```bash
source /opt/ros/humble/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install --packages-select slider_robot_gazebo
source install/setup.bash
ros2 launch slider_robot_gazebo gazebo.launch.py
```

For the alternative robot, close the first simulation and run:

```bash
ros2 launch slider_robot_gazebo universal_joint.launch.py
```

The launch files start Gazebo, robot_state_publisher, joint-state GUI, controller spawners and command adapters. The adapters convert GUI joint states into controller position commands. Inspect `config/` and `urdf/` for controller names and joint limits.

This source targets Gazebo Classic, not newer Gazebo releases. Python syntax and XML structure can be checked without ROS, but successful simulation requires the matching ROS/Gazebo environment. No physical robot operation is claimed.
