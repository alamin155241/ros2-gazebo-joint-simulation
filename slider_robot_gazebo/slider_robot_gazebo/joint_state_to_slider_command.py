import math

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray


class JointStateToSliderCommand(Node):
    """Convert joint_state_publisher_gui output into a ros2_control command."""

    def __init__(self):
        super().__init__('joint_state_to_slider_command')

        self.declare_parameter('joint_name', 'slider_joint')
        self.declare_parameter('joint_states_topic', '/joint_states_gui')
        self.declare_parameter('command_topic', '/slider_position_controller/commands')
        self.declare_parameter('min_position', 0.0)
        self.declare_parameter('max_position', 0.5)

        self.joint_name = self.get_parameter('joint_name').value
        joint_states_topic = self.get_parameter('joint_states_topic').value
        command_topic = self.get_parameter('command_topic').value
        self.min_position = float(self.get_parameter('min_position').value)
        self.max_position = float(self.get_parameter('max_position').value)

        self.publisher = self.create_publisher(Float64MultiArray, command_topic, 10)
        self.subscription = self.create_subscription(
            JointState,
            joint_states_topic,
            self._joint_state_callback,
            10,
        )

        self.get_logger().info(
            f'Forwarding {self.joint_name} from {joint_states_topic} to {command_topic}'
        )

    def _joint_state_callback(self, msg):
        if self.joint_name not in msg.name:
            return

        index = msg.name.index(self.joint_name)
        if index >= len(msg.position):
            return

        position = msg.position[index]
        if not math.isfinite(position):
            return

        position = min(max(position, self.min_position), self.max_position)
        self.publisher.publish(Float64MultiArray(data=[position]))


def main(args=None):
    rclpy.init(args=args)
    node = JointStateToSliderCommand()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
