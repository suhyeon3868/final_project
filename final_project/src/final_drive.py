#!/home/pi/.pyenv/versions/rospy3/bin/python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class SelfDrive:
    def __init__(self, publisher):
        self.publisher = publisher
        self.count = 30

    def lds_callback(self, scan):
        left_sum = 0
        right_sum = 0
        turtle_vel = Twist()
        left_angle = scan.ranges[:20]
        right_angle = scan.ranges[340:]

        for i in range(len(left_angle)):
            left_sum += left_angle[i]
        average_left = left_sum / len(left_angle)

        for i in range(len(right_angle)):
            right_sum += right_angle[i]
        average_right = right_sum / len(right_angle)


        if average_right <= 0.4:
            turtle_vel.linear.x = 0.0
            turtle_vel.angular.z = 2.3
            self.publisher.publish(turtle_vel)
        elif average_left <= 0.4:
            turtle_vel.linear.x = 0.0
            turtle_vel.angular.z = -2.3
            self.publisher.publish(turtle_vel)
        else:
            turtle_vel.linear.x = 0.15
            turtle_vel.angular.z = 0.0
            self.publisher.publish(turtle_vel)


def main():
    rospy.init_node('self_drive')
    publisher = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    driver = SelfDrive(publisher)
    subscriber = rospy.Subscriber('scan', LaserScan,
                                  lambda scan: driver.lds_callback(scan))
    rospy.spin()

if __name__ == "__main__":
    main()

