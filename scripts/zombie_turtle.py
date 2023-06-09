import rospy
import math
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import Spawn, SpawnRequest
from geometry_msgs.msg import Twist


class Zombie:
    def __init__(self):
        self.x = rospy.get_param('~x', 1)
        self.y = rospy.get_param('~y', 1)
        self.phi = rospy.get_param('~theta', 1)
        self.lin_speed = rospy.get_param('~speed_linear', 1.0)
        self.ang_speed = rospy.get_param('~speed_angular', 1.0)

        rospy.wait_for_service('spawn', 10)
        try: 
            spawner = rospy.ServiceProxy('spawn', Spawn)
            spawn_arg = SpawnRequest()
            
            spawn_arg.x = self.x
            spawn_arg.y = self.y
            spawn_arg.theta = self.phi
            spawn_arg.name = "turtle2"

            spawner(spawn_arg)
            self.pub = rospy.Publisher('turtle2/cmd_vel', Twist, queue_size=10)
            self.listener()
        except rospy.ServiceException as e:
            print ('Service call fail: %s', e)

    def go_to_goal(self, x_goal, y_goal):
        velocity_message = Twist()
        
        distance = abs(math.sqrt(((x_goal - self.x) ** 2) + (y_goal - self.y) ** 2))
        linear_speed = distance * self.lin_speed

        desired_agle_goal = math.atan2(y_goal - self.y, x_goal - self.x)
        angular_speed = (desired_agle_goal - self.phi) * self.ang_speed
        rospy.loginfo('%s, %s', desired_agle_goal, angular_speed)
    

        velocity_message.linear.x = linear_speed
        velocity_message.angular.z = angular_speed

        if ((linear_speed < 4) | (angular_speed < 4) | ((distance > 0.5) & (distance < 4))):
            self.pub.publish(velocity_message)

    def callback(self, data):
        self.go_to_goal(data.x, data.y)

    def ack(self, data):
        self.x = data.x
        self.y = data.y
        self.phi = data.theta

    def listener(self):
        rospy.init_node('listener', anonymous=True)
        rospy.Subscriber('turtle1/pose', Pose, self.callback)
        rospy.Subscriber('turtle2/pose', Pose, self.ack)
        rospy.spin()


if __name__ == '__main__':
    try:
        Zombie()
    except rospy.ROSInterruptException:
        pass
