#!/usr/bin/env python

import math
import rospy

from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist

class WallFollower:
    _PROPOTIONAL_FACTOR = 0.075 # Propotional factor of the error between wall's and robot's angles.

    def __init__(self):
        self.rate = rospy.Rate(10)

        self.scan_sub = rospy.Subscriber('scan', LaserScan, self.update_scan)
        self.odom_sub = rospy.Subscriber('odom', Odometry, self.update_twist)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

        self.scan = LaserScan(ranges=[math.inf])
        self.twist = Twist()

        self.loop()

    def update_scan(self, data: LaserScan):
        self.scan = data

    def update_twist(self, data: Odometry):
        self.twist = data.twist.twist

    def loop(self):
        while not rospy.is_shutdown():
            min_laser, min_angle = min((range, i) for (i, range) in enumerate(self.scan.ranges))

            new_twist = Twist()
            new_twist.linear.x = 0.4; new_twist.linear.y = 0.0; new_twist.linear.z = 0.0

            if min_laser < 1:
                delta_angle = min_angle - (270 if min_angle > 180 else 90)
                rospy.loginfo(f'Lazor: {min_angle}')

                new_twist.angular.x = 0.0; new_twist.angular.y = 0.0; new_twist.angular.z = self._PROPOTIONAL_FACTOR * delta_angle 
                self.cmd_vel_pub.publish(new_twist)

            self.rate.sleep()


if __name__ == '__main__':
    try:
        rospy.init_node('srr_test')
        WallFollower()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
