#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import time
import math

turtlesim_pose=None #tuetlesim::Pose
goal_pose=None #turtlesim::Pose
vel_msg=None
PI=3.14159265359
x_max=11.0
y_max=11.0

def poseCallback(pose_message): #const turtlesim::Pose::ConstPtr&
    #global turtlesim_pose 
    turtlesim_pose.x=pose_message.x
    turtlesim_pose.y=pose_message.y
    turtlesim_pose.theta=pose_message.theta

def move(speed,distance,isForward):

    #global vel_msg

    if(isForward):
        vel_msg.linear.x=abs(speed) #geometry_msgs::Twist vel_msg

    else:
        vel_msg.linear.x=-abs(speed)

    vel_msg.linear.y=0
    vel_msg.linear.z=0


    vel_msg.angular.x=0
    vel_msg.angular.y=0
    vel_msg.angular.z=0
        
    t0=time.time()
    current_distance=0

    rate=rospy.Rate(10)

    # do while loop

    velocity_publisher.publish(vel_msg) 
    t1=time.time()
    current_distance=speed*(t1-t0)
    rospy.spin #spinOnce
    rate.sleep

    while not (current_distance>distance): #repeat while current_distance<distance
        velocity_publisher.publish(vel_msg) 
        t1=time.time()
        current_distance=speed*(t1-t0)
        rate.sleep

    vel_msg.linear.x=0
    velocity_publisher.publish(vel_msg)


def rotate(angular_speed,relative_angle,clockwise):
    
    #global vel_msg

    current_angle=0.0
    t0=time.time()
    rate=rospy.Rate(10)

    vel_msg.linear.x=0
    vel_msg.linear.y=0
    vel_msg.linear.z=0

    vel_msg.angular.x=0
    vel_msg.angular.y=0

    if(clockwise):
        vel_msg.angular.z=-abs(angular_speed)
    else:
        vel_msg.angular.z=abs(angular_speed)

    #do while loop
    velocity_publisher.publish(vel_msg)
    t1=time.time()
    current_angle=angular_speed*(t1-t0)
    rospy.spin
    rate.sleep

    while not current_angle>relative_angle: #while current_angle<relative_angle
        velocity_publisher.publish(vel_msg)
        t1=time.time()
        current_angle=angular_speed*(t1-t0)
        rospy.spin
        rate.sleep 

    vel_msg.angular.z=0
    velocity_publisher.publish(vel_msg) 

def degrees2radians(angle_in_degrees):
    #global PI
    return angle_in_degrees*PI/180

def setDesiredOrientation(desired_angle_radians):
    #global turtlesim_pose
    relative_angle_radians=desired_angle_radians-turtlesim_pose.theta
    
    if relative_angle_radians<0:
        clockwise=True
    else:
        clockwise=False

    rotate(abs(relative_angle_radians),abs(relative_angle_radians),clockwise)

def getDistance(x1,y1,x2,y2):
    print('getDistance function')

    return math.sqrt(pow((x1-x2),2)+pow((y1-y2),2))

def moveGoal(goal_pose,distance_tolerance):
    global vel_msg
    loop_rate=rospy.Rate(10)

    #do-while loop
    print('do-while loop')

    vel_msg.linear.x=1.5*getDistance(turtlesim_pose.x,turtlesim_pose.y,goal_pose.x,goal_pose.y)
    vel_msg.linear.y=0
    vel_msg.linear.z=0

    vel_msg.angular.x=0
    vel_msg.angular.y=0
    vel_msg.angular.z=4*(math.atan2(goal_pose.y-turtlesim_pose.y,goal_pose.x-turtlesim_pose.x)-turtlesim_pose.theta)

    velocity_publisher.publish(vel_msg)
    print('Velocity published')

    loop_rate.sleep()

    while(getDistance(turtlesim_pose.x,turtlesim_pose.y,goal_pose.x,goal_pose.y)<distance_tolerance):
        print('While loop')

        vel_msg.linear.x=1.5*getDistance(turtlesim_pose.x,turtlesim_pose.y,goal_pose.x,goal_pose.y)
        vel_msg.linear.y=0
        vel_msg.linear.z=0

        vel_msg.angular.x=0
        vel_msg.angular.y=0
        vel_msg.angular.z=4*(math.atan2(goal_pose.y-turtlesim_pose.y,goal_pose.x-turtlesim_pose.x)-turtlesim_pose.theta)

        velocity_publisher.publish(vel_msg)
        loop_rate.sleep()

    print('End move goal')
    vel_msg.linear.x=0
    vel_msg.angular.z=0
    velocity_publisher.publish(vel_msg)
    print('Velocity published')

def gridClean():
    pose=Pose
    loop_rate=rospy.Rate(0.5)

    pose.x=1
    pose.y=1
    pose.theta=0
    moveGoal(pose,0.01)
    loop_rate.sleep()
    setDesiredOrientation(0)
    loop_rate.sleep()

    move(2,9,True)
    loop_rate.sleep()
    rotate(degrees2radians(10),degrees2radians(90),False)
    loop_rate.sleep()
    move(2,9,True)

    rotate(degrees2radians(10),degrees2radians(90),False)
    loop_rate.sleep()
    move(2,1,True)
    rotate(degrees2radians(10),degrees2radians(90),False)
    loop_rate.sleep()
    move(2,9,True)

    rotate(degrees2radians(30),degrees2radians(90),True)
    loop_rate.sleep()
    move(2,1,True)
    rotate(degrees2radians(30),degrees2radians(90),True)
    loop_rate.sleep()
    move(2,9,True)

    #distance=getDistance(turtlesim_pose.x,turtlesim_pose.y,x_max,y_max)

def spiralClean():
    #count=0.0
    constant_speed=4.0
    vk=1.0
    wk=2.0
    rk=0.5
    loop_rate=rospy.Rate(1)

    #do-while loop
    rk=rk+0.5
    vel_msg.linear.x=rk
    vel_msg.linear.y=0
    vel_msg.linear.z=0

    vel_msg.angular.x=0
    vel_msg.angular.y=0
    vel_msg.angular.z=constant_speed #vk/(0.5+rk)

    velocity_publisher.publish(vel_msg)
    rospy.spin
    loop_rate.sleep()
    print(rk,vk,wk)

    while((turtlesim_pose.x<10.5)&(turtlesim_pose.y<10.5)):
        rk=rk+0.5
        vel_msg.linear.x=rk
        vel_msg.linear.y=0
        vel_msg.linear.z=0

        vel_msg.angular.x=0
        vel_msg.angular.y=0
        vel_msg.angular.z=constant_speed #vk/(0.5+rk)

        velocity_publisher.publish(vel_msg)
        rospy.spin
        loop_rate.sleep()
        print(rk,vk,wk)

    vel_msg.linear.x=0
    velocity_publisher.publish(vel_msg)


if __name__ == '__main__':

    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('/turtle1/Pose',Pose,poseCallback,10)
    rospy.init_node('clean', anonymous=True)
    
    vel_msg=Twist()
    turtlesim_pose=Pose
    goal_pose=Pose
    loop_rate=rospy.Rate(0.5)

    goal_pose.x=1
    goal_pose.y=1
    goal_pose.theta=0

    #setDesiredOrientation(degrees2radians(120))
    #loop_rate.sleep()
    #setDesiredOrientation(degrees2radians(-60))
    #loop_rate.sleep()
    #setDesiredOrientation(degrees2radians(0))

    try:
        #speed_key=float(input("Introduce speed: "))
        #distance_key=float(input("Introduce the distance the robot must take: "))
        #isForward_key=float(input("Select if the robot must move forward (1) or backward (!1): "))

        #move(speed_key,distance_key,isForward_key)

        #angular_speed=float(input('Enter angular speed:'))
        #angle=float(input('Enter desired angle:'))
        #clockwise=float(input('Clockwise?:'))

        #rotate(degrees2radians(angular_speed),degrees2radians(angle),clockwise)

        #moveGoal(goal_pose,0.01)
        #loop_rate.sleep()

        #gridClean()

        #spiralClean()

        spiralClean()
        rospy.spin

    except rospy.ROSInterruptException:
        print('something failed during execution') 