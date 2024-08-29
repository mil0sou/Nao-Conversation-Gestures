# -*- coding: UTF-8 -*-

# ===============================================
#  File       : NAOMover.py
#  Author     : Milo Soulard
#  Python     : 3.x
#  Date       : Summer 2024
#  Description: Starts the program
#  Credits    : https://github.com/Oswualdo/Teleoperation-and-control-of-a-humanoid-robot-NAO-through-body-gestures
# ===============================================


#import cv2
import time
import argparse
import numpy as np
import pykinect_azure as pykinect
import socket 

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))
# for sending data 

def get_quaternion(joint): #return quaterions
    orientation = joint.orientation
    return orientation.wxyz

# maths

def get_angles(KneeLeftPos, HipLeftPos, AnkleLeftPos):
    trans_a = HipLeftPos - KneeLeftPos
    trans_b = AnkleLeftPos - KneeLeftPos
    angles = np.arccos(np.sum(trans_a * trans_b, axis = 0)/(np.sqrt(np.sum(trans_a ** 2, axis = 0)) * np.sqrt(np.sum(trans_b ** 2, axis = 0))))
    return (angles) * (180/np.pi)

def angles_2D(base,point):
    orientation=point-base
    if orientation[0]<0:
        angle_x = np.arctan(orientation[2] / orientation[0])-np.pi
        if orientation[2]>0:
            angle_x = np.arctan(orientation[2] / orientation[0]) + np.pi
    else:
        angle_x=np.arctan(orientation[2]/orientation[0])
    return (angle_x) * (180/np.pi)

def angles_2D_zy1(base,point):
    orientation=point-base
    if orientation[2]>0:
        angle_x = np.arctan(orientation[1] / orientation[2])-np.pi
        if orientation[1]<0:
            angle_x = np.arctan(orientation[1] / orientation[2]) + np.pi
    else:
        angle_x=np.arctan(orientation[1]/orientation[2])
    return (angle_x) * (180/np.pi)

def rotation(base, point):
    orientation = point - base
    if orientation[2] > 0:
        angle_x = -(np.arctan(orientation[1] / orientation[2])) + np.pi
        if orientation[1] < 0:
            angle_x = -(np.arctan(orientation[1] / orientation[2])) - np.pi
    else:
        angle_x = -(np.arctan(orientation[1] / orientation[2]))
    return (angle_x) * (180 / np.pi)

def angles_2D_zy2(base,point):
    orientation=point-base
    if orientation[0]>0:
        angle_x = np.arctan(orientation[1] / orientation[0])-np.pi
        if orientation[1]<0:
            angle_x = np.arctan(orientation[1] / orientation[0]) + np.pi
    else:
        angle_x=np.arctan(orientation[1]/orientation[0])
    return (angle_x) * (-180/np.pi)

def angles_2D_zy(base,point):
    orientation=point-base
    angle_x=np.arctan(orientation[2]/orientation[1])
    return (angle_x) * (180/np.pi)

def angles_2D_yx(base,point):
    orientation=point-base
    angle_x=np.arctan(orientation[0]/orientation[1])
    return (angle_x) * (180/np.pi)

def angle_lateral(base,point,trans_b):
    trans_a=point-base
    if trans_a[0]>0:
        angle_x = -np.arccos(np.sum(trans_a * trans_b, axis=0) / (np.sqrt(np.sum(trans_a ** 2, axis=0)) * np.sqrt(np.sum(trans_b ** 2, axis=0))))
    else:
        angle_x = np.arccos(np.sum(trans_a * trans_b, axis=0) / (np.sqrt(np.sum(trans_a ** 2, axis=0)) * np.sqrt(np.sum(trans_b ** 2, axis=0))))
    return (angle_x) * (180/np.pi)

def angle_lateral2(base,point,trans_b):
    trans_a=point-base
    angle_x = np.arccos(np.sum(trans_a * trans_b, axis=0) / (np.sqrt(np.sum(trans_a ** 2, axis=0)) * np.sqrt(np.sum(trans_b ** 2, axis=0))))
    return (angle_x) * (180/np.pi)

def Gestos(Origen, Punto_1, unitario):
    A = Punto_1 - Origen
    B = unitario
    angle = np.arccos(np.sum(A * B, axis=0) / (np.sqrt(np.sum(A ** 2, axis=0)) * np.sqrt(np.sum(B ** 2, axis=0))))
    return (angle) * (180 / np.pi)

def main():
    #cv2.namedWindow('Depth image with skeleton', cv2.WINDOW_NORMAL)
    while True:
        capture = device.update()
        body_frame = bodyTracker.update()
        skeleton = body_frame.get_body_skeleton(0)
        if True:

            Centro_Cadera = get_quaternion(skeleton.joints[0])  # Centre de la hanche / pelvis
            Espina = get_quaternion(skeleton.joints[1])         # Colonne vertébrale / spine
            Hombro_C = get_quaternion(skeleton.joints[2])       # epaule centrale / neck ?
            Cabeza = get_quaternion(skeleton.joints[3])         # tete / head

            Hombro_I = get_quaternion(skeleton.joints[pykinect.K4ABT_JOINT_SHOULDER_LEFT])       # epaule gauche / shoulder left 
            Codo_I = get_quaternion(skeleton.joints[pykinect.K4ABT_JOINT_ELBOW_LEFT])         # coude gauche / elbox left
            Muneca_I = get_quaternion(skeleton.joints[pykinect.K4ABT_JOINT_WRIST_LEFT])       # poignet gauche / wrist left
            Mano_I = get_quaternion(skeleton.joints[7])         # main gauche / hand left

            Hombro_D = get_quaternion(skeleton.joints[pykinect.K4ABT_JOINT_SHOULDER_RIGHT])       # epaule droit / shoulder right 
            Codo_D = get_quaternion(skeleton.joints[pykinect.K4ABT_JOINT_ELBOW_RIGHT])         # coude droit / elbox right
            Muneca_D = get_quaternion(skeleton.joints[pykinect.K4ABT_JOINT_WRIST_RIGHT])      # poignet droit / wrist right
            Mano_D = get_quaternion(skeleton.joints[11])        # main droit / hand right

            Cadera_I = get_quaternion(skeleton.joints[12])      # hanche gauche / hip left
            Rodilla_I = get_quaternion(skeleton.joints[13])     # genou gauche / knee left 
            Tobillo_I = get_quaternion(skeleton.joints[14])     # cheville gauche / ankle left
            Pie_I = get_quaternion(skeleton.joints[15])         # pied gauche / foot left

            Cadera_D = get_quaternion(skeleton.joints[16])      # hanche droit / hip right
            Rodilla_D = get_quaternion(skeleton.joints[17])     # genou droit / knee right 
            Tobillo_D = get_quaternion(skeleton.joints[18])     # cheville droit / ankle right
            Pie_D = get_quaternion(skeleton.joints[19])         # pied droit / foot right

            #Vectorization of points

            Vector_Hombro_D = np.array([Hombro_D.x, Hombro_D.y, Hombro_D.z])
            Vector_Codo_D = np.array([Codo_D.x, Codo_D.y, Codo_D.z])
            Vector_Muneca_D = np.array([Muneca_D.x, Muneca_D.y, Muneca_D.z])

            Vector_Hombro_I = np.array([Hombro_I.x, Hombro_I.y, Hombro_I.z])
            Vector_Codo_I = np.array([Codo_I.x, Codo_I.y, Codo_I.z])
            Vector_Muneca_I = np.array([Muneca_I.x, Muneca_I.y, Muneca_I.z])

            Vector_Cadera_D = np.array([Cadera_D.x, Cadera_D.y, Cadera_D.z])
            Vector_Rodilla_D = np.array([Rodilla_D.x, Rodilla_D.y, Rodilla_D.z])
            Vector_Tobillo_D = np.array([Tobillo_D.x, Tobillo_D.y, Tobillo_D.z])

            Vector_Cadera_I = np.array([Cadera_I.x, Cadera_I.y, Cadera_I.z])
            Vector_Rodilla_I = np.array([Rodilla_I.x, Rodilla_I.y, Rodilla_I.z])
            Vector_Tobillo_I = np.array([Tobillo_I.x, Tobillo_I.y, Tobillo_I.z])

            Vec_U_X=np.array([1,0,0])
            Vec_U_NegX = np.array([-1,0,0])
            Vector_Hombro_DF = np.array([Hombro_D.x + 0.03, Hombro_D.y, Hombro_D.z])
            sombra_x = Vector_Codo_D - Vector_Hombro_DF
            sombra_x[0] = 0

            sombra_z=Vector_Codo_D - Vector_Hombro_DF
            sombra_z[2] = 0

            Hombro_V2 = angles_2D_zy1(np.array(Vector_Hombro_D), np.array(Vector_Codo_D))* (np.pi / 180)
            if Hombro_V2 > 119* (np.pi / 180):
                Hombro_V2 = 119* (np.pi / 180)
            if Hombro_V2 < -119* (np.pi / 180):
                Hombro_V2 = -119* (np.pi / 180)

            HombroCodo_V2 = angle_lateral(np.array(Vector_Hombro_DF), np.array(Vector_Codo_D), np.array(sombra_x))* (np.pi / 180)
            if HombroCodo_V2 < -76* (np.pi / 180):
                HombroCodo_V2 = -76* (np.pi / 180)
            if HombroCodo_V2 > 18* (np.pi / 180):
                HombroCodo_V2 = 18* (np.pi / 180)

            Angle_codo_D = get_angles(np.array(Vector_Codo_D), np.array(Vector_Hombro_D),
                              np.array(Vector_Muneca_D))

            Angle_HCC_D = get_angles(np.array(Vector_Hombro_D), np.array(Vector_Codo_D),
                                np.array(Vector_Cadera_D))

            Angle_hombrozx_D = angles_2D(np.array(Vector_Hombro_D), np.array(Vector_Codo_D))

            Rota_codo_D = angles_2D_zy2(np.array(Vector_Codo_D), np.array(Vector_Muneca_D))* (np.pi / 180)

            Giro_D = Gestos(Vector_Hombro_DF, Vector_Codo_D, Vec_U_X)


            complemento = angle_lateral2(np.array(Vector_Hombro_DF), np.array(Vector_Codo_D), np.array(sombra_z))
            if complemento < 20:
                Rota_codo_D = rotation(np.array(Vector_Codo_D), np.array(Vector_Muneca_D)) * (np.pi / 180)+Hombro_V2

            if Giro_D < 20:
                Hombro_V2 = 0
                Rota_codo_D = rotation(np.array(Vector_Codo_D), np.array(Vector_Muneca_D)) * (np.pi / 180)
            

            if Rota_codo_D < -119* (np.pi / 180):
                Rota_codo_D = -119* (np.pi / 180)
            if Rota_codo_D > 119* (np.pi / 180):
                Rota_codo_D = 119 * (np.pi / 180)

            z_2D = (((47.0 / 54.0) * Angle_hombrozx_D) + 76.0) * (np.pi / 180)
            if z_2D < -18* (np.pi / 180):
                z_2D = -18* (np.pi / 180)
            if z_2D > 1.32:
                z_2D = 1.32

            z = (((-44.0 / 45.0) * Angle_codo_D) + 176) * (np.pi / 180)
            if z > 1.53:
                z = 1.53

            w = (((-6.0 / 5.0) * Angle_HCC_D) + 114.0) * (np.pi / 180)


            Vector_Hombro_IF = np.array([Hombro_I.x - 0.03, Hombro_I.y, Hombro_I.z])
            sombra_xI = Vector_Codo_I - Vector_Hombro_IF
            sombra_xI[0] = 0

            Hombro_V2I = angles_2D_zy1(np.array(Vector_Hombro_I), np.array(Vector_Codo_I)) * (np.pi / 180)
            if Hombro_V2I > 119 * (np.pi / 180):
                Hombro_V2I = 119 * (np.pi / 180)
            if Hombro_V2I < -119 * (np.pi / 180):
                Hombro_V2I = -119 * (np.pi / 180)

            HombroCodo_V2I = angle_lateral(np.array(Vector_Hombro_IF), np.array(Vector_Codo_I), np.array(sombra_xI)) * (
            np.pi / 180)
            if HombroCodo_V2I > 76 * (np.pi / 180):
                HombroCodo_V2I = 76 * (np.pi / 180)
            if HombroCodo_V2I < -18 * (np.pi / 180):
                HombroCodo_V2I = -18 * (np.pi / 180)

            Angle_codo_I = get_angles(np.array(Vector_Codo_I), np.array(Vector_Hombro_I),
                                np.array(Vector_Muneca_I))

            Angle_HCC_I = get_angles(np.array(Vector_Hombro_I), np.array(Vector_Codo_I),
                                  np.array(Vector_Cadera_I))

            Angle_hombrozx_I = angles_2D(-np.array(Vector_Hombro_I), -np.array(Vector_Codo_I))

            Rota_codo_I = -angles_2D_zy1(np.array(Vector_Codo_I), np.array(Vector_Muneca_I)) * (np.pi / 180)
            if Rota_codo_I > 119 * (np.pi / 180):
                Rota_codo_I = 119 * (np.pi / 180)
            if Rota_codo_I < -119 * (np.pi / 180):
                Rota_codo_I = -119 * (np.pi / 180)

                
            z_2D_2 = (((47.0 / 54.0) * Angle_hombrozx_I) - 76.0) * (np.pi / 180)
            if z_2D_2 > 18* (np.pi / 180):
                z_2D_2 = 18* (np.pi / 180)
            if z_2D_2 < -1.32:
                z_2D_2 = -1.32

            z_2 = (((44.0 / 45.0) * Angle_codo_I) - 176.0) * (np.pi / 180)
            if z_2 < -1.53:
                z_2 = -1.53

            w_2 = (((-6.0 / 5.0) * Angle_HCC_I) + 114.0) * (np.pi / 180)


            Angle_RCT_I = get_angles(Vector_Rodilla_I,Vector_Cadera_I,Vector_Tobillo_I)
            Angle_caderayz_I = angles_2D_zy(Vector_Cadera_I, Vector_Rodilla_I)
            Angle_caderayx_I = angles_2D_yx(Vector_Cadera_I, Vector_Rodilla_I)


            rod_D = (((-25.0 / 26.0) * Angle_RCT_I) + 2185.0 / 13.0) * (np.pi / 180)  # 50=120  y 180=-5
            mus_frente = (((-23.0 / 24.0) * Angle_caderayz_I) - 7.0 / 4.0) * (np.pi / 180)  # -30=27 y 90=-88
            mus_lateral = Angle_caderayx_I * (np.pi / 180)  # -21 a 45

            if rod_D > 2.09:  # 120:
                rod_D = 2.09  # 120
            if rod_D < -.087:  # -5:
                rod_D = -.087  # -5

            if mus_frente > .47:  # 27:
                mus_frente = .47  # 27
            if mus_frente < -1.53:  # -88:
                mus_frente = -1.53  # -88

            if mus_lateral < -.36:  # -21:
                mus_lateral = -.36  # -21
            if mus_lateral > .78:  # 45:
                mus_lateral = .78  # 45

            Angle_RCT_D = get_angles(Vector_Rodilla_D, Vector_Cadera_D, Vector_Tobillo_D)
            Angle_caderayz_D = angles_2D_zy(Vector_Cadera_D, Vector_Rodilla_D)
            Angle_caderayx_D = angles_2D_yx(Vector_Cadera_D, Vector_Rodilla_D)


            rod_D_2 = (((-25.0 / 26.0) * Angle_RCT_D) + 2185.0 / 13.0) * (np.pi / 180)  # 50=120  y 180=-5
            mus_frente_2 = (((-23.0 / 24.0) * Angle_caderayz_D) - 7.0 / 4.0) * (np.pi / 180)  # -30=27 y 90=-88
            mus_lateral_2 = Angle_caderayx_D * (np.pi / 180)  # -21 a 45

            if rod_D_2 > 2.09:  # 120:
                rod_D_2 = 2.09  # 120
            if rod_D_2 < -.087:  # -5:
                rod_D_2 = -.087  # -5

            if mus_frente_2 > .47:  # 27:
                mus_frente_2 = .47  # 27
            if mus_frente_2 < -1.53:  # -88:
                mus_frente_2 = -1.53  # -88

            if mus_lateral_2 > .36:  # 21:
                mus_lateral_2 = .36  # 21
            if mus_lateral_2 < -.78:  # -45:
                mus_lateral_2 = -.78  # -45
            
            angles = [HombroCodo_V2, Hombro_V2, Rota_codo_D, z, HombroCodo_V2I,Hombro_V2I, 0, z_2]
            for i in range(len(angles)): 
                angle2 = round(float(angles[i]), 2)
                angles[i] = angle2
            array_str = ','.join([str(x) for x in angles])
            # print(array_str)
            client_socket.sendall(array_str.encode())
            time.sleep(0.05)

if __name__ == "__main__":
    pykinect.initialize_libraries(track_body=True)
    device_config = pykinect.default_configuration
    device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_OFF
    device_config.depth_mode = pykinect.K4A_DEPTH_MODE_WFOV_2X2BINNED
    device = pykinect.start_device(config=device_config)
    bodyTracker = pykinect.start_body_tracker(model_type=pykinect.K4ABT_DEFAULT_MODEL)
    capture = device.update()
    body_frame = bodyTracker.update()
    num_bodies = body_frame.get_num_bodies()
    skeleton = body_frame.get_body_skeleton(0)  
    raised = False
    #cv2.namedWindow('Depth image with skeleton', cv2.WINDOW_NORMAL)
    main()







"""Centro_Cadera = get_quaternion(skeleton.joints[0])
Espina = get_quaternion(skeleton.joints[1])
Hombro_C = get_quaternion(skeleton.joints[2])
Cabeza = get_quaternion(skeleton.joints[26])

Hombro_I = get_quaternion(skeleton.joints[5])
Codo_I = get_quaternion(skeleton.joints[6])
Muneca_I = get_quaternion(skeleton.joints[7])
Mano_I = get_quaternion(skeleton.joints[8])

Hombro_D = get_quaternion(skeleton.joints[12])
Codo_D = get_quaternion(skeleton.joints[13])
Muneca_D = get_quaternion(skeleton.joints[14])
Mano_D = get_quaternion(skeleton.joints[15])

Cadera_I = get_quaternion(skeleton.joints[18])
Rodilla_I = get_quaternion(skeleton.joints[19])
Tobillo_I = get_quaternion(skeleton.joints[20])
Pie_I = get_quaternion(skeleton.joints[21])

Cadera_D = get_quaternion(skeleton.joints[22])
Rodilla_D = get_quaternion(skeleton.joints[23])
Tobillo_D = get_quaternion(skeleton.joints[24])
Pie_D = get_quaternion(skeleton.joints[25])
#Cuenta = skeleton.joints[20]

FRAMES = [
'head',
'neck',
'torso',
'left_shoulder',
'left_elbow',
'left_hand',
'left_hip',
'left_knee',
'left_foot',
'right_shoulder',
'right_elbow',
'right_hand',
'right_hip',
'right_knee',
'right_foot',
] 
    
"""


"""
# Puntos del Kinect
Centro_Cadera = skeleton.joints[0]  # Centre de la hanche / pelvis
Espina = skeleton.joints[1]         # Colonne vertébrale / spine
Hombro_C = skeleton.joints[2]       # epaule centrale / neck ?
Cabeza = skeleton.joints[3]         # tete / head

Hombro_I = skeleton.joints[4]       # epaule gauche / shoulder left 
Codo_I = skeleton.joints[5]         # coude gauche / elbox left
Muneca_I = skeleton.joints[6]       # poignet gauche / wrist left
Mano_I = skeleton.joints[7]         # main gauche / hand left

Hombro_D = skeleton.joints[8]       # epaule droit / shoulder right 
Codo_D = skeleton.joints[9]         # coude droit / elbox right
Muneca_D = skeleton.joints[10]      # poignet droit / wrist right
Mano_D = skeleton.joints[11]]       # main droit / hand right

Cadera_I = skeleton.joints[12]      # hanche gauche / hip left
Rodilla_I = skeleton.joints[13]     # genou gauche / knee left 
Tobillo_I = skeleton.joints[14]     # cheville gauche / ankle left
Pie_I = skeleton.joints[15]         # pied gauche / foot left

Cadera_D = skeleton.joints[16]      # hanche droit / hip right
Rodilla_D = skeleton.joints[17]     # genou droit / knee right 
Tobillo_D = skeleton.joints[18]     # cheville droit / ankle right
Pie_D = skeleton.joints[19]         # pied droit / foot right

#Cuenta = skeleton.joints[20] 

Centre de la hanche
Colonne vertébrale 
Épaule_C
Tête 

Epaule
Coude
Poignet
Main

Hanche
Genou
Cheville
Pied

Perle 


"""
# Kinect Points

"""Hip_Center = skeleton.joints[0]
Spine = skeleton.joints[1]
Shoulder_Center = skeleton.joints[2]
Head = skeleton.joints[26]

Shoulder_Left = skeleton.joints[5]
Elbow_Left = skeleton.joints[6]
Wrist_Left = skeleton.joints[7]
Hand_Left = skeleton.joints[8]
Shoulder_Right = skeleton.joints[12]
Elbow_Right = skeleton.joints[13]
Wrist_Right = skeleton.joints[14]
Hand_Right = skeleton.joints[15]

Hip_Left = skeleton.joints[18]
Knee_Left = skeleton.joints[19]
Ankle_Left = skeleton.joints[20]
Foot_Left = skeleton.joints[21]

Hip_Right = skeleton.joints[22]
Knee_Right = skeleton.joints[23]
Ankle_Right = skeleton.joints[24]
Foot_Right = skeleton.joints[25]
# Counter = skeleton.joints[20]"""


"""Centro_Cadera = skeleton.joints[0]
Espina = skeleton.joints[1]
Hombro_C = skeleton.joints[2]
Cabeza = skeleton.joints[26]

Hombro_I = skeleton.joints[5]
Codo_I = skeleton.joints[6]
Muneca_I = skeleton.joints[7]
Mano_I = skeleton.joints[8]

Hombro_D = skeleton.joints[12]
Codo_D = skeleton.joints[13]
Muneca_D = skeleton.joints[14]
Mano_D = skeleton.joints[15]

Cadera_I = skeleton.joints[18]
Rodilla_I = skeleton.joints[19]
Tobillo_I = skeleton.joints[20]
Pie_I = skeleton.joints[21]

Cadera_D = skeleton.joints[22]
Rodilla_D = skeleton.joints[23]
Tobillo_D = skeleton.joints[24]
Pie_D = skeleton.joints[25]
#Cuenta = skeleton.joints[20]"""

#Cuenta = skeleton.joints[20]

"""
0	PELVIS	-
1	SPINE_NAVAL	PELVIS
2	SPINE_CHEST	SPINE_NAVAL
26	HEAD	NECK

5	SHOULDER_LEFT	CLAVICLE_LEFT
6	ELBOW_LEFT	SHOULDER_LEFT   
7	WRIST_LEFT	ELBOW_LEFT
8	HAND_LEFT	WRIST_LEFT

12	SHOULDER_RIGHT	CLAVICLE_RIGHT
13	ELBOW_RIGHT	SHOULDER_RIGHT
14	WRIST_RIGHT	ELBOW_RIGHT
15	HAND_RIGHT	WRIST_RIGHT

18	HIP_LEFT	PELVIS
19	KNEE_LEFT	HIP_LEFT
20	ANKLE_LEFT	KNEE_LEFT
21	FOOT_LEFT	ANKLE_LEFT

22	HIP_RIGHT	PELVIS
23	KNEE_RIGHT	HIP_RIGHT
24	ANKLE_RIGHT	KNEE_RIGHT
25	FOOT_RIGHT	ANKLE_RIGHT

26	HEAD	NECK
27	NOSE	HEAD
28	EYE_LEFT	HEAD
29	EAR_LEFT	HEAD
30	EYE_RIGHT	HEAD
31	EAR_RIGHT	HEAD
            """