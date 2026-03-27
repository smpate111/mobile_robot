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
sudo apt install ros-jazzy-twist-mux
sudo apt install joystick jstest-gtk evtest     # if you want to use a gamepad to control the robot
sudo apt install ros-jazzy-joy ros-jazzy-teleop-twist-joy
sudo apt install ros-jazzy-twist-stamper
sudo apt install ros-jazzy-slam-toolbox
sudo apt install ros-jazzy-navigation2 ros-jazzy-nav2-bringup
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

## Gazebo Models Installation:

To be able to run the `obstacles.world` file in the Gazebo simulation, you will need to download some models onto your computer:

1. Go to the [Gazebo Website](https://app.gazebosim.org/fuel/models) and search for `Construction Barrel`.

![Screenshot of the Construction Barrel model in Gazebo.](/assets/construction_barrel_screenshot_1.jpeg)

2. Click on it and download the model.

![Screenshot of the Construction Barrel model download link.](/assets/construction_barrel_screenshot_2.jpeg)

3. Once it's downloaded, head over to your `Download` folder and extract the contents from the `.zip` file.

![Screenshot of the Construction Barrel unzip button.](/assets/construction_barrel_screenshot_3.jpeg)

4. After extracting the contents out of the `.zip` file, create a folder in your `/home` folder and name it `my-local-models`. Then, copy the `Construction Barrel` folder and paste it inside the `my-local-models` folder. Rename the `Construction Barrel` folder to `construction_barrel`.

![Screenshot of the construction_barrel folder.](/assets/construction_barrel_screenshot_4.jpeg)

5. Repeat Steps 1-4 for the `Construction Cone` model.
<br/><br/>

What the folder structure should look like:
```
/home
└── my-local-models/
    ├── construction_barrel/    
    └── construction_cone/    
```

## Gamepad Installation:
1. To use a gamepad to control the robot, you will need to ensure that it is plugged into your computer and your computer is able to recognize it.
2. Run `evtest` and select the number that is assigned to the gamepad. Then, press any random input from the gamepad to see that the inputs are being registered in the terminal. `Ctrl+C` to exit once you are able to verify this.
3. If you want to use a better visual interface, run `jstest-gtk` and select your gamepad. Verify that the inputs are being registered and record the left and right shoulder buttons' (`L1` and `R1`) ID. Close out the GUI afterwards.
4. To get the gamepad to work in ROS2, run `ros2 run joy joy_enumerate_devices` to find the gamepad's ID.
5. Go to `joystick.yaml` in the `/home/ros2_ws/src/mobile_robot/config/yaml` folder and change the `device_id` value to the ID assigned to the gamepad. Also, change the `enable_button` value to the left shoulder button's ID and the `enable_turbo_button` value to the right shoulder button's ID.

## Usage:
Open **3 terminals** in the following order:

1. **Terminal 1 — Gazebo**:
```
ros2 launch mobile_robot launch_sim.launch.py use_ros2_control:=true
```
If you want to use the `DiffDrive` plugin, then set `use_ros2_control` to `false`. Otherwise, leave it as `true` to use the `ros2_control` plugin.
<br/><br/>

2. **Terminal 2 — Rviz**:
```
rviz2
```
Open the `robot.rviz` configuration file that is located in the `/home/ros2_ws/src/mobile_robot/config/rviz` folder.
<br/><br/>

3. **Terminal 3 — Keyboard**:
```
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p stamped:=true -r /cmd_vel:=/cmd_vel_keyboard -p use_sim_time:=true
```
This is to control the robot via keyboard. If you want to use the `DiffDrive` plugin, then set `stamped` to `false`. Otherwise, leave it as `true` to use the `ros2_control` plugin.
<br/><br/>

**OR**
<br/><br/>

**Terminal 3 — Gamepad**:
```
ros2 launch mobile_robot joystick.launch.py use_ros2_control:=false
```
This is to control the robot via gamepad. If you want to use the `DiffDrive` plugin, then set `use_ros2_control` to `false`. Otherwise, leave it as `true` to use the `ros2_control` plugin.
<br/><br/>