import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, EmitEvent
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import LifecycleNode
from ament_index_python.packages import get_package_share_directory
import launch_ros.events.lifecycle
import lifecycle_msgs.msg
import launch.events

def generate_launch_description():
    slam_params_file = LaunchConfiguration('slam_params_file')

    declare_slam_params_file_cmd = DeclareLaunchArgument(
        'slam_params_file',
        default_value= '/var/novelte/config/nav_config.yaml',
        description='Full path to the ROS2 parameters file to use for the slam_toolbox node')

    start_sync_slam_toolbox_node = LifecycleNode(
        parameters=[
          slam_params_file,
          {'use_sim_time': False}
        ],
        package='slam_toolbox',
        executable='sync_slam_toolbox_node',
        name='slam_toolbox',
        namespace='',
        output='screen')

    configure_transition = EmitEvent(
        event=launch_ros.events.lifecycle.ChangeState(
            lifecycle_node_matcher=launch.events.matches_action(start_sync_slam_toolbox_node),
            transition_id=lifecycle_msgs.msg.Transition.TRANSITION_CONFIGURE,
        )
    )

    ld = LaunchDescription()

    ld.add_action(declare_slam_params_file_cmd)
    ld.add_action(start_sync_slam_toolbox_node)
    ld.add_action(configure_transition)

    return ld
