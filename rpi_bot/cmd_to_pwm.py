import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from rpi_bot.rpi_interface import RPi_Motors

class Velocity_Subscriber(Node):

    def __init__(self):
        super().__init__('velocity_subscriber')

        self.declare_parameters(
            namespace='',
            parameters=[
                ('ena_pin', rclpy.Parameter.Type.INTEGER),
                ('in1_pin', rclpy.Parameter.Type.INTEGER),
                ('in2_pin', rclpy.Parameter.Type.INTEGER),
                ('in3_pin', rclpy.Parameter.Type.INTEGER),
                ('in4_pin', rclpy.Parameter.Type.INTEGER),
                ('enb_pin', rclpy.Parameter.Type.INTEGER),
                ('speed', 50),
                ('differential', 50),
            ],
        )

        self.motors = RPi_Motors(
            self.get_parameter('ena_pin').get_parameter_value().integer_value,
            self.get_parameter('in1_pin').get_parameter_value().integer_value,
            self.get_parameter('in2_pin').get_parameter_value().integer_value,
            self.get_parameter('in3_pin').get_parameter_value().integer_value,
            self.get_parameter('in4_pin').get_parameter_value().integer_value,
            self.get_parameter('enb_pin').get_parameter_value().integer_value
        )

        self.speed = self.get_parameter('speed').get_parameter_value().integer_value
        self.differential = self.get_parameter('differential').get_parameter_value().integer_value

        self.right_vel = 0
        self.left_vel = 0

        self.subscription = self.create_subscription(Twist, 'cmd_vel', self.calculate_wheel_velocity_callback, 10)
        self.subscription  # prevent unused variable warning
        self.get_logger().info('Velocity Subscriber Initialized')

    def calculate_wheel_velocity_callback(self, msg):
        left_temp = self.left_vel
        right_temp = self.right_vel

        left_temp = self.speed * msg.linear.x - self.differential * msg.angular.z
        right_temp = self.speed * msg.linear.x + self.differential * msg.angular.z

        if (left_temp != self.left_vel) and (right_temp != self.right_vel):
            self.get_logger().info(f'Setting motors: left_vel={left_temp}, right_vel={right_temp}')
            self.motors.setMotors(left_temp, right_temp)


def main(args=None):
    rclpy.init(args=args)

    velocity_subscriber = Velocity_Subscriber()
    rclpy.spin(velocity_subscriber)

    velocity_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()