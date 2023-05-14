import rospy
import math
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist


class Zombie:
    def __init__(self):
        self.x = 1
        self.y = 1
        self.phi = 0
        self.lin_speed = rospy.get_param('~speed_linear', 1.0)
        self.ang_speed = rospy.get_param('~speed_angular', 1.0)

        rospy.loginfo('init done')
        rospy.wait_for_service('turtlesim1/spawn')
        try: 
            rospy.loginfo('spawning turtle')
            spawner = rospy.ServiceProxy('turtlesim1/spawn', turtlesim/Spawn)
            spawner(self.x, self.y, self.phi, "")
            self.pub = rospy.Publisher('turtle2/cmd_vel', Twist, queue_size=10)
            rospy.loginfo('listen')
            self.listener()
        except rospy.ServiceException as e:
            print ('Service call fail: %s', e)

    def go_to_goal(self, x_goal, y_goal):
        velocity_message = Twist()
        
        distance = abs(math.sqrt(((x_goal - self.x) ** 2) + (y_goal - self.y) ** 2))
        linear_speed = distance * self.lin_speed

        desired_agle_goal = math.atan2(y_goal - self.y, x_goal - self.x)
        angular_speed = (desired_agle_goal - self.phi) * self.ang_speed

        velocity_message.linear.x = linear_speed
        velocity_message.angular.z = angular_speed

        self.pub.publish(velocity_message)

    def callback(self, data):
        rospy.loginfo(rospy.get_caller_id() + ' heard\n x: %s\n y: %s ', data.x, data.y)
        # self.go_to_goal(data.x, data.y)

    def listener(self):
        rospy.init_node('listener', anonymous=True)
        rospy.Subscriber('turtle1/pose', Pose, self.callback)
        rospy.spin()


if __name__ == '__main__':
    try:
        Zombie()
    except rospy.ROSInterruptException:
        pass