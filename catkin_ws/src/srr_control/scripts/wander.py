#!/usr/bin/env python

import random, math
import rospy
from geometry_msgs.msg import Twist

def changeHeading(_timerevent):
    new_heading = random.uniform(0, 2*math.pi)
    rospy.loginfo(new_heading)

    twist = Twist()
    twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
    twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = new_heading
    cmd_vel_pub.publish(twist)

    rospy.sleep(rospy.Duration(1))

    twist.linear.x = 1.0; twist.linear.y = 0.0; twist.linear.z = 0.0
    twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
    cmd_vel_pub.publish(twist)


if __name__ == '__main__':
    try:
        rospy.init_node('srr_test')
        cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        rospy.Timer(rospy.Duration(10), changeHeading)
        changeHeading()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
