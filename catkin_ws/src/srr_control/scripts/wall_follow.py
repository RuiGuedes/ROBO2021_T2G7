#!/usr/bin/env python

import math
import random
import rospy

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class WallFollower:
    _APPROACH_DISTANCE = 0.75 # Distance from which the robot will start following the wall instead of going towards it 
    _FOLLOW_DISTANCE = 0.2 # Desired distance between the wall and the robot when it is following the wall

    _ANGLE_FACTOR = 2.5  # Propotional factor of the error of the angle between wall and robot
    _DISTANCE_FACTOR = 8  # Propotional factor of the error of the distance between wall and robot

    def __init__(self):
        self.rate = rospy.Rate(10)

        self.scan_sub = rospy.Subscriber('scan', LaserScan, self._update_scan)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

        self._scan = LaserScan(ranges=[math.inf])
        self._loop()

    def _update_scan(self, data: LaserScan):
        self._scan = data

    def _loop(self):
        while not rospy.is_shutdown():
            min_range, min_angle = min((range, i) for (i, range) in enumerate(self._scan.ranges))

            angular_direction = -1 if min_angle > 180 else 1
            right_angle = 270 if min_angle > 180 else 90

            new_twist = Twist()
            new_twist.linear.y = 0.0; new_twist.linear.z = 0.0
            new_twist.angular.x = 0.0; new_twist.angular.y = 0.0

            if min_range < self._APPROACH_DISTANCE:
                # Follow wall
                distance = min_range - self._FOLLOW_DISTANCE

                if self._scan.ranges[0] < 1.75 * self._FOLLOW_DISTANCE:                    
                    delta_angle = math.pi/4 if self._scan.ranges[90] > self._scan.ranges[270] else -math.pi/4
                else:
                    delta_angle = (min_angle - right_angle) * math.pi / 180

                new_twist.linear.x = 0.2
                new_twist.angular.z = max(-3, min(self._ANGLE_FACTOR * delta_angle + self._DISTANCE_FACTOR * angular_direction * distance, 3))
            elif min_range < self._scan.range_max:
                # Approach wall
                delta_angle = (min_angle if min_angle < 180 else min_angle - 360) * math.pi / 180

                new_twist.linear.x = 0.5
                new_twist.angular.z = self._ANGLE_FACTOR * delta_angle
            else:
                # Wander
                new_twist.linear.x = 0.5
                new_twist.angular.z = self._ANGLE_FACTOR * random.gauss(0, 1)
            
            self.cmd_vel_pub.publish(new_twist)
            self.rate.sleep()

if __name__ == '__main__':
    try:
        rospy.init_node('srr_wall_follow')
        WallFollower()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
