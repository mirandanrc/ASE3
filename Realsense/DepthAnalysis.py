import cv2
import pyrealsense2 as rs
import numpy as np
from realsense_depth import *
from time import sleep


# Initialize Camera Intel Realsense
dc = DepthCamera()

#Create mouse event
#cv2.namedWindow("Color frame")

while True:
    ret, depth_frame, color_frame = dc.get_frame()


    matriz = [[(x*32, y*24) for x in range(20)] for y in range(20)]
    for fila in matriz:
        for x, y in fila:
            cv2.circle(color_frame, (x, y), 2, (0, 0, 255))
            distance = depth_frame[y, x]
            cv2.putText(color_frame, "{}mm".format(distance), (x, y), cv2.FONT_HERSHEY_PLAIN, 0.5, (0, 255, 0), 1)
            #print("distancia", distance/10)

    #Una vez obtenido el frame de color se cambia a escala de grises
    gray = cv2.cvtColor(color_frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow("Depth frame", depth_frame)
    print(depth_frame)

    cv2.imshow("Color frame", gray)
    #cv2.imshow("Color frame", color_frame)
    key = cv2.waitKey(1)
    if key ==27:
        break
    sleep(0.5)

