import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from geometry_msgs.msg import Twist
from rpi_bot.motor_interface import RPi_Motors

class Velocity_Subscriber(Node):

    def __init__(self):
        super().__init__('velocity_subscriber')
        self.subscription = self.create_subscription(Twist, 'cmd_vel', self.cmd_to_pwm_callback, 10)
        self.subscription  # prevent unused variable warning

        motors = RPi_Motors()

    def cmd_to_pwm_callback(self, msg):
        right_wheel_vel = (msg.linear.x + msg.angular.x) / 2
        left_wheels_vel = (msg.linear.x - msg.angular.x) / 2

        self.get_logger().info('I heard: "%s" and "%s"' % right_wheel_vel, left_wheels_vel)


def main(args=None):
    rclpy.init(args=args)

    velocity_subscriber = Velocity_Subscriber()

    rclpy.spin(velocity_subscriber)

    velocity_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()