##################################################
# LIBRARIES
##################################################
import os

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

from ament_index_python.packages import get_package_share_directory
##################################################

def generate_launch_description():
    ##################################################
    # Package
    ##################################################
    package_name='mobile_robot' #<--- CHANGE ME
    ##################################################



    ##################################################
    # Gamepad configuration
    ##################################################
    use_sim_time = LaunchConfiguration('use_sim_time')
    joy_params = os.path.join(get_package_share_directory(package_name),'config/yaml','joystick.yaml')
    joy_node = Node(
        package='joy',
        executable='joy_node',
        parameters=[
            {
                'use_sim_time': use_sim_time
            }, 
            joy_params
        ],
    )
    ##################################################



    ##################################################
    # Gamepad node
    ##################################################
    use_ros2_control = LaunchConfiguration('use_ros2_control')
    teleop_node = Node(
        package='teleop_twist_joy', 
        executable='teleop_node',
        name = 'teleop_node',
        parameters=[
            joy_params,
            {
                'use_sim_time': use_sim_time,
                'publish_stamped_twist': ParameterValue(use_ros2_control, value_type=bool)
            }
        ],
        remappings=[
            (
                '/cmd_vel',
                '/cmd_vel_joy'
            )
        ],
    )
    ##################################################



    ##################################################
    # Launch everything
    ##################################################
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                'use_sim_time',
                default_value='false',
                description='Use sim time if true'
            ),

            DeclareLaunchArgument(
                'use_ros2_control',
                default_value='true',
                description='Use ros2_control if true'
            ),

            joy_node,
            teleop_node
        ]
    )
    ##################################################