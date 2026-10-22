from glob import glob
import os

from setuptools import setup


package_name = 'slider_robot_gazebo'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.urdf')),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*.world')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ROS 2 User',
    maintainer_email='user@example.com',
    description='Gazebo Classic simulation of a ROS 2 Humble prismatic slider robot.',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'joint_state_to_slider_command = slider_robot_gazebo.joint_state_to_slider_command:main',
            'joint_state_to_universal_command = slider_robot_gazebo.joint_state_to_universal_command:main',
        ],
    },
)
