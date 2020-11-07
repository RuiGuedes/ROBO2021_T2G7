#!/usr/bin/env python

import math
import rospy

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class WallFollower:
    _TARGET_DISTANCE = 0.2      # Desired distance between the wall and the robot

    _ANGLE_FACTOR = 2.5  # Propotional factor of the error of the angle between wall and robot
    _DISTANCE_FACTOR = 8  # Propotional factor of the error of the distance between wall and robot

    def __init__(self):
        self.rate = rospy.Rate(10)

        self.scan_sub = rospy.Subscriber('scan', LaserScan, self.update_scan)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

        self.scan = LaserScan(ranges=[math.inf])
        self.loop()

    def update_scan(self, data: LaserScan):
        self.scan = data

    def loop(self):
        while not rospy.is_shutdown():
            min_range, min_angle = min((range, i) for (i, range) in enumerate(self.scan.ranges))

            angular_direction = -1 if min_angle > 180 else 1
            right_angle = 270 if min_angle > 180 else 90

            new_twist = Twist()
            new_twist.linear.x = 0.2; new_twist.linear.y = 0.0; new_twist.linear.z = 0.0

            if min_range < 1:
                distance = min_range - self._TARGET_DISTANCE

                if self.scan.ranges[0] < 1.75 * self._TARGET_DISTANCE:
                    delta_angle = math.pi/2 if self.scan.ranges[90] > self.scan.ranges[270] else 3 * math.pi/2
                else:
                    delta_angle = (min_angle - right_angle) * math.pi / 180

                new_twist.angular.x = 0.0; new_twist.angular.y = 0.0; 
                new_twist.angular.z = max(-3, min(self._ANGLE_FACTOR * delta_angle + self._DISTANCE_FACTOR * angular_direction * distance, 3))
                self.cmd_vel_pub.publish(new_twist)
            
            self.rate.sleep()


if __name__ == '__main__':
    try:
        rospy.init_node('srr_wall_follow')
        WallFollower()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
