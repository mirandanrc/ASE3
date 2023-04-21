import cv2
import pyrealsense2 as rs
import numpy as np
from realsense_depth import *
from time import sleep
#import Jetson.GPIO as GPIO
import math
import cv2.aruco


#Realsense activation
dc = DepthCamera()

#Webcam activation
#Trigger = 37
#Bit1 = 35
#Bit2 = 33

#GPIO.setmode(GPIO.BOARD)
#GPIO.setwarnings(False)
#GPIO.setup(Trigger, GPIO.OUT, initial=GPIO.LOW)
#GPIO.setup(Bit1, GPIO.OUT, initial=GPIO.LOW)
#GPIO.setup(Bit2, GPIO.OUT, initial=GPIO.LOW)

x1 = 0
y1 = 0
x2 = 0
y2 = 0

##WEBCAM FUNCTIONS
def change_brightness(img, value):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.add(v, value)
    v[v > 255] = 255
    v[v < 0] = 0
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

    return img

def mid_points(matrix, pt1, pt2):
    matrix[0][0] = (pt1[0] + pt2[0]) / 2
    matrix[0][1] = (pt1[1] + pt2[1]) / 2
    return matrix

def get_angle(bottomRight, bottomLeft):
    x = (bottomRight[0] - bottomLeft[0])
    y = (bottomRight[1] - bottomLeft[1])
    angle = math.atan2(y, x)
    angle = math.degrees(angle)
    angle *= -1

    if angle < 0:
        angle += 360
    angle = round(angle, 2)
    angle = abs(angle)
    return angle

def get_anglerad(bottomRight, bottomLeft):
    x = (bottomRight[0] - bottomLeft[0])
    y = (bottomRight[1] - bottomLeft[1])
    angle = math.atan2(y, x)
    angle = math.degrees(angle)
    angle *= -1

    if angle < 0:
        angle += 360

    angle = abs(angle)
    angle = math.radians(angle)
    angle = round(angle, 2)
    return angle

def draw_aruco(frame, topLeft, topRight, bottomLeft, bottomRight, MidP, X, Y, angle):

     #Se dibuja el cuadrado
    cv2.line(frame, topLeft, topRight, (0, 255, 0), 2)
    cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
    cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
    cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)

    line_thickness = 3
    cv2.line(frame, X[0], MidP[0], (0, 0, 255), thickness=line_thickness)
    cv2.line(frame, Y[0], MidP[0], (255, 0, 0), thickness=line_thickness)

    cv2.putText(frame, str(MidP[0]), (MidP[0][0], MidP[0][1] - 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 204, 204), 2, cv2.LINE_AA)

    cv2.putText(frame, f'ID: {markerID}', (MidP[0][0] - 150, MidP[0]
                [1] - 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 204, 204), 2, cv2.LINE_AA)

    cv2.putText(frame, f'ID: {markerID}', (MidP[0][0] - 150, MidP[0]
                [1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    


def get_coordenates(markerCorner):
    # extract the marker corners (which are always returned in
    # top-left, top-right, bottom-right, and bottom-left order)
    corners = markerCorner.reshape((4, 2))
    (topLeft, topRight, bottomRight, bottomLeft) = corners

    # convert each of the (x, y)-coordinate pairs to integers
    topRight = (int(topRight[0]), int(topRight[1]))
    bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
    bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
    topLeft = (int(topLeft[0]), int(topLeft[1]))

    return topLeft, topRight, bottomLeft, bottomRight

def get_ArucoInfo(markerCorner, markerID):

    topLeft, topRight, bottomLeft, bottomRight = get_coordenates(markerCorner)

    angle = get_anglerad(bottomRight, bottomLeft)

    info = {"coordenadas": [topLeft, topRight, bottomLeft,
                           bottomRight], "angulo": (angle), "ID": (markerID)}

    return info


visual = True

if __name__ == "__main__":

    capture = cv2.VideoCapture(1, cv2.CAP_V4L2)
    qrCodeDetector = cv2.aruco

    window_name = 'Camara detector qr'  # Nombre de la ventana

    # nuevoooo
    width = 640
    height = 480

    # resolucion HDHD
    capture.set(3, width)
    capture.set(4, height)

    points = np.arange(8).reshape(4, 2)
    MidP = np.arange(2).reshape(1, 2)
    Y = np.arange(2).reshape(1, 2)
    X = np.arange(2).reshape(1, 2)

   


    while True:
        #ret1, frame = capture.read()
        ret, depth_frame, color_frame = dc.get_frame()
        qr_frame = color_frame

        
        qr_frame = cv2.resize(qr_frame, (640, 480))
        qr_frame = change_brightness(qr_frame, 10)


        gray = cv2.cvtColor(qr_frame, cv2.COLOR_BGR2GRAY)

        arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50)

        arucoParams = cv2.aruco.DetectorParameters()

        detector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)

        points, ids, rejected = detector.detectMarkers(gray)

        if len(points) > 0:
            ids = ids.flatten()
            for (markerCorner, markerID) in zip(points, ids):

                #GPIO.output(Trigger, GPIO.HIGH)

                topLeft, topRight, bottomLeft, bottomRight = get_coordenates(
                    markerCorner)
                mid_points(MidP, topRight, bottomLeft)
                mid_points(Y, topRight, bottomRight)
                mid_points(X, bottomLeft, bottomRight)

                x1 = topLeft[0]
                y1 = topLeft[1]
                x2 = bottomRight[0]
                y2 = bottomRight[1]

                camera_centerx = width/2
                camera_centery = height/2

                angle = get_angle(bottomRight, bottomLeft)

                value1 = X[0][0]
                                
                if (288 <= value1 <= 352): 
                    print('Center')
                    #print('ADE')
                    #GPIO.output(Bit1, GPIO.LOW)
                    #GPIO.output(Bit2, GPIO.LOW)
                   
                elif (value1 > 352):
                    print('RIGHT')
                    #UARTprint("Giro2")
                    #GPIO.output(Bit1, GPIO.HIGH)
                    #GPIO.output(Bit2, GPIO.HIGH)
                   
                elif (value1 < 288): 
                    print('LEFT')
                    #print("Giro1")
                    #GPIO.output(Bit1, GPIO.HIGH)
                    #GPIO.output(Bit2, GPIO.LOW)
                   

                if visual == True:
                    draw_aruco(qr_frame, topLeft, topRight, bottomLeft,
                               bottomRight, MidP, X, Y, angle)
                    


        prom=[]
        print("Coord:",x1,x2)
        xmtz=int((x1-x2)/5)
        ymtz=int((y2-y1)/5)

        if xmtz < 5:
            xmtz = 5
        if ymtz < 5:
            ymtz = 5
        
        print(xmtz, ymtz)

        #int((x2-x1))

        matriz = [[(x*5+x2, y*5+y1) for x in range(xmtz)] for y in range(ymtz)]
        for fila in matriz:
            for x, y in fila:
                cv2.circle(color_frame, (x, y), 2, (0, 0, 255))
                distance = depth_frame[y, x]
                cv2.putText(color_frame, "{}mm".format(distance), (x, y), cv2.FONT_HERSHEY_PLAIN, 0.5, (0, 255, 0), 1)
                prom.append(distance/10)
  

        #get_coordenates(markerCorner)

        avg = sum(prom)/len(prom)
        print(avg)
        # x1 = topLeft
        # y1 = topRight
        # x2 = bottomLeft
        # y2 = bottomRight
        
        if avg < 180:
            cv2.rectangle(color_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            print("Too close")
        elif avg > 180:
            cv2.rectangle(color_frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            print("Secure distance")

        # if avg < 500:
        #     cv2.rectangle(color_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        #     print("Too close")
        # elif avg > 500:
        #     cv2.rectangle(color_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        #     print("Secure distance")

        #cv2.imshow("Frame", color_frame)

        #ret, frame = capture.read()
        if ret == False:
            break
        


        if visual == True:
            cv2.imshow(window_name, qr_frame)  # Despliega la ventana
            cv2.imshow("Frame", color_frame)

        key = cv2.waitKey(1)
        if key ==27:
            break

capture.release()
cv2.destroyAllWindows()