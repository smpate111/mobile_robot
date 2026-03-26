# mobile_robot: ROS2 SLAM and Navigation Robot
`mobile_robot` is a custom-made robotics project built on ROS2 that is designed for autonomous navigation and environment mapping. It uses a 2D LiDAR sensor and odometry using the `slam_toolbox` to perform Serialized Localization and Mapping (SLAM). This allows the robot to build highly accurate maps of its surroundings and reliably navigate within them.

## Features:
1. **2D Mapping (SLAM)**: Generates a detailed occupancy grid map of unknown environments in real-time.
2. **Localization**: Tracks the robot's position within an existing map using either the Adaptive Monte Carlo Localization (AMCL) module or the SLAM toolbox localization mode.
3. **Autnomous Navigation**: Uses the Nav2 stack for path planning, obstacle avoidance, and goal-reaching.
4. **Teleoperation**: Supports manual control via keyboard.

## Software Requirements:
1. **Operating System**: Linux Mint 22.3
2. **ROS2**: Jazzy Jalisco
3. **ROS2 Dependencies**:
    * `slam_toolbox`
    * `navigation2`
    * `nav2_bringup`
    * `robot_state_publisher`

## Prerequisites:
```
sudo apt install ros-dev-tools
sudo apt install ros-jazzy-desktop
sudo apt install ros-jazzy-ros-gz
sudo apt install ros-jazzy-gazebo-ros-pkgs
sudo apt install ros-jazzy-image-transport-plugins
sudo apt install ros-jazzy-rqt-image-view
sudo apt install ros-jazzy-ros2-control
sudo apt install ros-jazzy-ros2-controllers
sudo apt install ros-jazzy-gz-ros2-control
sudo apt install ros-jazzy-slam-toolbox
sudo apt install ros-jazzy-navigation2 ros-jazzy-nav2-bringup
sudo apt install ros-jazzy-twist-mux
```

## Installation:
```
mkdir -p ~/ros2_ws/src && cd ~/ros2_ws/src
git clone https://github.com/smpate111/mobile_robot.git
cd ~/ros2_ws
colcon build --symlink-install
source ~/ros2_ws/install/setup.bash
```

Add to `~/.bashrc`:
```
source /opt/ros/jazzy/setup.bash
export LIBGL_ALWAYS_SOFTWARE=1
export GZ_PARTITION=default
export QT_QPA_PLATFORM=xcb
source ~/ros2_ws/install/setup.bash
export GZ_SIM_RESOURCE_PATH=~/my-local-models/
```

Go to `https://app.gazebosim.org/fuel/models` and search for `Construction Barrel`.
![Screenshot of the Construction Barrel model in Gazebo.](/assets/construction_barrel_screenshot_1.jpeg)

Add to your `~` folder (`/home` folder):
```
/home
└── my-local-models/
    ├── construction_barrel/    
    └── construction_cone/    
```