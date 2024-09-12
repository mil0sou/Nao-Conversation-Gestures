# -*- coding: UTF-8 -*-

# ===============================================
#  File       : NAOMover.py
#  Author     : Milo Soulard
#  Python     : 2.7
#  Date       : Summer 2024
#  Description: Makes the robot move using the joints data given by the camera program
# ===============================================


"""import matplotlib.pyplot as plt
import matplotlib.animation as animation"""
#from naoqi import ALProxy
import socket
import time 

nao_ip = "192.168.1.240"
nao_port = 9559

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(1)
conn, addr = server_socket.accept() #connects to the socket 

armjoints = ["RShoulderRoll", "RShoulderPitch", "RElbowYaw", "RElbowRoll","LShoulderRoll", "LShoulderPitch", "LElbowYaw", "LElbowRoll"]
#motionProxy = ALProxy("ALMotion", nao_ip, nao_port)
movespeed = 0.2 # 0 slow 1 fast 

LIMITS = {
    'HeadYaw': [-2.0, 2.0], 
    'HeadPitch': [-0.67, 0.51],
    'LShoulderPitch': [-2.0, 2.0], 
    'LShoulderRoll': [-0.31, 1.32],
    'RShoulderPitch': [-2.0, 2.0], 
    'RShoulderRoll': [-1.32, 0.31],
    'LElbowYaw': [-2.0, 2.0], 
    'LElbowRoll': [-1.54, -0.03],
    'RElbowYaw': [-2.0, 2.0],
    'RElbowRoll': [0.03, 1.54],
}


'''for joint in armjoints:
    motionProxy.setStiffnesses(joint, 1.0)
    motionProxy.setAngles(joint, 0, 0.5)


def set_angle_with_limits(joint_name, angle):
    if joint_name in LIMITS:
        min_limit, max_limit = LIMITS[joint_name]
        angle = float(round(max(min_limit, min(max_limit, angle)),2))
        print(angle)
        motionProxy.setAngles(joint_name, angle, movespeed)
    else:
        print(joint_name, "OUT OF BOUNDS")'''

def set_angles_within_limits(anglelist):
    for joint_name in anglelist:
        if joint_name in LIMITS:
            min_limit, max_limit = LIMITS[joint_name]
            angle = float(round(max(min_limit, min(max_limit, angle)),2))
            print(angle)
        else:
            print(joint_name, "OUT OF BOUNDS")


def main(): # TESTING PHASE
    while 1:
        data = conn.recv(1024)
        #print(data)
        angles = [float(x) for x in data.split(',')]
        
        angle2= [x for x in angles]
        angle2[0] = float(round((-0.31 + (angles[0] - 0.15) * 10.73),2)) #RShoulderRoll
        angle2[4] = float(round((-0.31 + (angles[4] - 0.15) * 10.73),2)) #LShoulderRoll


        # angle2[1] = -truc + (angles[1] - truc) * truc #RShoulderPitch
        # angle2[2] = -truc + (angles[2] - truc) * truc #RElbowYaw
        # angle2[3] = -truc + (angles[3] - truc) * truc #RElbowRoll
        #angle2[4] = float(round((-0.31 + (angles[4] - 0.15) * 10.73) ,2)) #LShoulderRoll
        #angle2[4] = float(round((-0.31 + ((angles[4] - 1.5)/ -6.5)  *1.67), 2))
        # angle2[5] = -truc + (angles[5] - truc) * truc #LShoulderPitch   
        # angle2[6] = -truc + (angles[6] - truc) * truc #LElbowYaw
        # angle2[7] = -truc + (angles[7] - truc) * truc #LElbowRoll
        
        # print(angle2)
        #set_angle_with_limits("RShoulderRoll", angle2[0])

        # 
        #set_angle_with_limits("LShoulderPitch", angle2[4])s
        # motionProxy.setAngles(armjoints, angles, movespeed)
        print(armjoints[4],angles[4],angle2[4])
        set_angles_within_limits(angle2)
        """set_angle_with_limits("RShoulderPitch", angle2[0])"""

main()
conn.close()
server_socket.close()

"""used_joints = [
    "HeadYaw", "HeadPitch", "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw",
    "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand", "LHand"
]
unused_joints = [
    "LHipYawPitch", "LHipRoll", "LHipPitch", "LKneePitch", "LAnklePitch", "LAnkleRoll",
    "RHipYawPitch", "RHipRoll", "RHipPitch", "RKneePitch", "RAnklePitch", "RAnkleRoll"
]

for joint in used_joints:
    motionProxy.setStiffnesses(joint, 1.0)
for joint in unused_joints:
    motionProxy.setStiffnesses(joint, 0.0)"""




"""angles = []
times = []
start_time = time.time()

fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.set_ylim(-2, 2)  
ax.set_xlim(0, 10)  
ax.grid()
ax.set_xlabel('Time (s)')
ax.set_ylabel('Angle (rad)')
ax.set_title('Real-time Angle Tracking')"""

"""def init():
    line.set_data([], [])
    return line,"""



"""for value in raw_values:
        if value.count('.') == 1:
            angle = round(float(value), 2)
            print(angle)
            joint_name = "RShoulderRoll"
            motionProxy.setAngles(joint_name, angle, 0.2)
            angles.append(angle)
            times.append(current_time)

            if times[-1] > 10:
                del times[0]
                del angles[0]

            ax.set_xlim(times[0], times[-1] if times[-1] > 10 else 10)
            line.set_data(times, angles)
    
    return line,"""

"""ani = animation.FuncAnimation(fig, update, frames=range(1000), init_func=init, blit=True, interval=10)

plt.show()
"""




"""from naoqi import ALProxy
import socket 
nao_ip = "192.168.1.240"
nao_port = 9559     #SKFXHZKR

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(1)

conn, addr = server_socket.accept()

motionProxy = ALProxy("ALMotion", nao_ip, nao_port)

used_joints = ["RShoulderRoll","RShoulderPitch","RElbowYaw","RElbowRoll"]
for joint in used_joints:
    motionProxy.setStiffnesses(joint, 1.0)
    motionProxy.setAngles(joint, 0, 0.5)

while 1:
    joint_name = "RShoulderRoll"
    data = conn.recv(1024)
    print(data)
    angle = round(float(data),2)
    print(angle)
    motionProxy.setStiffnesses(joint_name, 1.0)
    motionProxy.setAngles(joint_name, angle, 1)
"""

"""motionProxy.setStiffnesses("RShoulderRoll", 1.0)
motionProxy.setStiffnesses("RShoulderPitch", 1.0)
motionProxy.setStiffnesses("RElbowYaw", 1.0)
motionProxy.setStiffnesses("RElbowRoll", 1.0)
motionProxy.setAngles('RShoulderRoll', 0, 0.5)
motionProxy.setAngles('RShoulderPitch', 0, 0.5)
motionProxy.setAngles('RElbowYaw', 0, 0.5)
motionProxy.setAngles('RElbowRoll', 0, 0.5)"""