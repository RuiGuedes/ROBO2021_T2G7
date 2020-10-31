import rospy
#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan

def testLaser(data: LaserScan):
    rospy.loginfo(f'Laser Length: {len(data.ranges)}')

if __name__ == '__main__':
    try:
        rospy.init_node('srr_test')
        rospy.Subscriber('scan', LaserScan, testLaser)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
