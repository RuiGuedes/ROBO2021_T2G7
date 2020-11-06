#!/usr/bin/env python

import math
import rospy

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class WallFollower:
    _TARGET_DISTANCE = 0.2      # Desired distance between the wall and the robot

    _PROPOTIONAL_FACTOR = 2  # Propotional factor of the error
    _INTEGRAL_FACTOR = 0.1     # Integral factor of the error

    def __init__(self):
        self.rate = rospy.Rate(10)

        self.scan_sub = rospy.Subscriber('scan', LaserScan, self.update_scan)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

        self.scan = LaserScan(ranges=[math.inf])
        self.error_integral = 0.0

        self.loop()

    def update_scan(self, data: LaserScan):
        self.scan = data

    def loop(self):
        while not rospy.is_shutdown():
            min_range, min_angle = min((range, i) for (i, range) in enumerate(self.scan.ranges))

            angular_direction = -1 if min_angle > 180 else 1
            right_angle = 270 if min_angle > 180 else 90

            new_twist = Twist()
            new_twist.linear.x = 0.4; new_twist.linear.y = 0.0; new_twist.linear.z = 0.0

            if min_range < 1:
                # self.scan.ranges[right_angle]
                distance = self.scan.ranges[right_angle] - self._TARGET_DISTANCE
                delta_angle = (min_angle - right_angle) * math.pi / 180

                # if min_angle > 90 and min_angle < 270:
                    # x_mirror_range = self.scan.ranges[right_angle - delta_angle]

                    # if x_mirror_range < min_range + 0.1:
                        # Compensate rotation on inner curve
                        # delta_angle *= 2

                # error_value = delta_angle
                # error_value = angular_direction * distance
                error_value = max(-3.5, min(delta_angle + angular_direction * distance, 3.5))
                self.error_integral += max(-0.5, min(error_value * 0.1, 0.5))

                new_twist.angular.x = 0.0; new_twist.angular.y = 0.0; 
                new_twist.angular.z = self._PROPOTIONAL_FACTOR * error_value + self._INTEGRAL_FACTOR * self.error_integral
                self.cmd_vel_pub.publish(new_twist)
            
            self.rate.sleep()


if __name__ == '__main__':
    try:
        rospy.init_node('srr_test')
        WallFollower()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
