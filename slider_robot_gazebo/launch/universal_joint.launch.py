import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, RegisterEventHandler, TimerAction
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    package_name = 'slider_robot_gazebo'
    package_share = get_package_share_directory(package_name)
    gazebo_share = get_package_share_directory('gazebo_ros')

    urdf_path = os.path.join(package_share, 'urdf', 'universal_joint_robot.urdf')
    world_path = os.path.join(package_share, 'worlds', 'empty.world')
    controllers_path = os.path.join(package_share, 'config', 'universal_joint_controllers.yaml')

    with open(urdf_path, 'r', encoding='utf-8') as urdf_file:
        robot_description = urdf_file.read()

    robot_description = robot_description.replace(
        '__UNIVERSAL_CONTROLLERS_CONFIG__',
        controllers_path.replace(os.sep, '/'),
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_share, 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={'world': world_path}.items(),
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[
            {
                'robot_description': robot_description,
                'use_sim_time': True,
            }
        ],
    )

    joint_state_publisher_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='universal_joint_state_publisher_gui',
        output='screen',
        parameters=[
            {
                'robot_description': robot_description,
                'use_sim_time': True,
                'rate': 20,
            }
        ],
        remappings=[
            ('joint_states', 'universal_joint_states_gui'),
        ],
    )

    gui_to_controller = Node(
        package=package_name,
        executable='joint_state_to_universal_command',
        name='joint_state_to_universal_command',
        output='screen',
        parameters=[
            {
                'joint_names': ['universal_x_joint', 'universal_y_joint'],
                'joint_states_topic': '/universal_joint_states_gui',
                'command_topic': '/universal_position_controller/commands',
                'min_position': -1.2,
                'max_position': 1.2,
                'use_sim_time': True,
            }
        ],
    )

    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic',
            'robot_description',
            '-entity',
            'universal_joint_robot',
            '-x',
            '0.0',
            '-y',
            '0.0',
            '-z',
            '0.0',
        ],
        output='screen',
    )

    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'joint_state_broadcaster',
            '--controller-manager',
            '/controller_manager',
            '--controller-manager-timeout',
            '60',
        ],
        output='screen',
    )

    universal_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'universal_position_controller',
            '--controller-manager',
            '/controller_manager',
            '--controller-manager-timeout',
            '60',
        ],
        output='screen',
    )

    load_controllers = RegisterEventHandler(
        OnProcessExit(
            target_action=spawn_entity,
            on_exit=[
                TimerAction(
                    period=2.0,
                    actions=[
                        joint_state_broadcaster_spawner,
                        universal_controller_spawner,
                    ],
                )
            ],
        )
    )

    return LaunchDescription(
        [
            gazebo,
            robot_state_publisher,
            joint_state_publisher_gui,
            gui_to_controller,
            spawn_entity,
            load_controllers,
        ]
    )
