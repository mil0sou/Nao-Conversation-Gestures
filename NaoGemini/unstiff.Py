#make sure to hold the robot when launching it
from naoqi import ALProxy
ALProxy("ALMotion", "192.168.1.240", 9559).setStiffnesses("Body", 0)