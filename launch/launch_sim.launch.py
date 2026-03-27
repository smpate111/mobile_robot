##################################################
# LIBRARIES
##################################################
import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition

from launch_ros.actions import Node
##################################################



def generate_launch_description():
    ##################################################
    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!
    ##################################################
    package_name='mobile_robot' #<--- CHANGE ME
    ##################################################



    ##################################################
    # Robot State Publisher
    ##################################################
    use_ros2_control = LaunchConfiguration('use_ros2_control')
    
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(get_package_share_directory(package_name), 'launch', 'rsp.launch.py')
            ]
        ),
        launch_arguments={
            'use_sim_time': 'true',
            'use_ros2_control': use_ros2_control
        }.items()
    )
    ##################################################
    


    ##################################################
    # Global Environment (World & Gazebo)
    ##################################################
    world = LaunchConfiguration('world')

    world_arg = DeclareLaunchArgument(
        'world',
        #default_value="empty.sdf",
        default_value=os.path.join(get_package_share_directory(package_name), 'worlds', 'obstacles.world'),
        description='World to load'
    )


    # include the Gazebo launch file provided by the ros_gz_sim package

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
            ]
        ),
        launch_arguments={
            'gz_args': [
                '-r -v4 ', world,
            ],
            'on_exit_shutdown': 'true'
        }.items()
    )
    ##################################################



    ##################################################
    # Spawn robot
    ##################################################

    # run the spawner node from the ros_gz_sim package
    # NOTE: the entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'mobile_robot',
            '-z', '0.1'
        ],
        output='screen'
    )
    ##################################################



    ##################################################
    # Launch the ROS-Gazebo bridge for normal topics
    ##################################################
    bridge_params = os.path.join(get_package_share_directory(package_name), 'config/yaml', 'gz_bridge.yaml')

    ros_gz_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            '--ros-args',
            '-p',
            f'config_file:={bridge_params}',
        ]
    )

    # camera
    ros_gz_image_bridge = Node(
        package="ros_gz_image",
        executable="image_bridge",
        arguments=[
            "/camera/image_raw",
            "/depth_camera/image_raw"
        ]
    )
    ##################################################

    ##################################################
    # ros2_control configuration
    ##################################################
    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "diff_cont",
            '--controller-ros-args',
            '-r /diff_cont/cmd_vel:=/cmd_vel'
        ],
        condition=IfCondition(use_ros2_control),
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad"],
        condition=IfCondition(use_ros2_control),
    )
    ##################################################



    ##################################################
    # Twist mux for switching between input sources
    ##################################################
    twist_mux_config = os.path.join(get_package_share_directory(package_name), 'config/yaml', 'twist_mux.yaml')
    twist_mux = Node(
        package='twist_mux',
        executable='twist_mux',
        output='screen',
        remappings={
            (
                '/cmd_vel_out',
                '/cmd_vel'
            )
        },
        parameters=[
            twist_mux_config,
            {
                'use_sim_time': True,
                'use_stamped': use_ros2_control
            }
        ]
    )
    ##################################################



    ##################################################
    # Launch everything
    ##################################################
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                'use_ros2_control',
                default_value='true',
                description='Use ros2_control if true'
            ),
            rsp,
            world_arg,
            gazebo,
            spawn_entity,
            ros_gz_bridge,
            ros_gz_image_bridge,
            diff_drive_spawner,
            joint_broad_spawner,
            twist_mux,
        ]
    )
    ##################################################