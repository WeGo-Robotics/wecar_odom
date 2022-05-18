#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
import tf2_ros

def amcl_to_odom():
    rospy.init_node('amcl_to_odom')
    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)
    odom_pub = rospy.Publisher('/amcl/pose/odom', Odometry, queue_size=1)
    # odom = 
    odom = Odometry()
    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
            trans = tfBuffer.lookup_transform('map', 'base_link', rospy.Time())
            odom.pose.pose.position.x = trans.transform.translation.x
            odom.pose.pose.position.y = trans.transform.translation.y       
            odom.pose.pose.orientation.z = trans.transform.rotation.z
            odom.pose.pose.orientation.w = trans.transform.rotation.w
            odom_pub.publish(odom)
            # print(trans)
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            rate.sleep()
            continue
if __name__ == '__main__':
    amcl_to_odom()
