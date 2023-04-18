import cv2
import pyrealsense2 as rs
import numpy as np
from realsense_depth import *
from time import sleep

dc = DepthCamera()

while True:
    ret, depth_frame, color_frame = dc.get_frame()
    prom=[]

    matriz = [[(x*5+270, y*5+190) for x in range(21)] for y in range(21)]
    for fila in matriz:
        for x, y in fila:
            cv2.circle(color_frame, (x, y), 2, (0, 0, 255))
            distance = depth_frame[y, x]
            cv2.putText(color_frame, "{}mm".format(distance), (x, y), cv2.FONT_HERSHEY_PLAIN, 0.5, (0, 255, 0), 1)
            prom.append(distance/10)


    avg = sum(prom)/len(prom)
    print(avg)
    x1 = 270
    y1 = 190
    x2 = 370
    y2 = 290
    
    if avg < 700:
        cv2.rectangle(color_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        print("NO")
    elif avg > 700:
        cv2.rectangle(color_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        print("YES")

    cv2.imshow("Frame", color_frame)


    key = cv2.waitKey(1)
    if key ==27:
        break1700
    #sleep(0.5)

