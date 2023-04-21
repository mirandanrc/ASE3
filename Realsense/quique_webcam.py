import cv2
import numpy as np
#import Jetson.GPIO as GPIO
import math
import time

Trigger = 37
Bit1 = 35
Bit2 = 33

# GPIO.setmode(GPIO.BOARD)
# GPIO.setwarnings(False)
# GPIO.setup(Trigger, GPIO.OUT, initial=GPIO.LOW)
# GPIO.setup(Bit1, GPIO.OUT, initial=GPIO.LOW)
# GPIO.setup(Bit2, GPIO.OUT, initial=GPIO.LOW)


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

    capture = cv2.VideoCapture(2, cv2.CAP_V4L2)
    qrCodeDetector = cv2.aruco

    window_name = 'Camara detector qr'  # Nombre de la ventana

    # nuevoooo
    width = 640
    height = 480

    # resolucion HD
    capture.set(3, width)
    capture.set(4, height)

    points = np.arange(8).reshape(4, 2)
    MidP = np.arange(2).reshape(1, 2)
    Y = np.arange(2).reshape(1, 2)
    X = np.arange(2).reshape(1, 2)

    while True:
        ret, frame = capture.read()
        if ret == False:
            break
        frame = cv2.resize(frame, (640, 480))
        frame = change_brightness(frame, 10)


        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

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

                camera_centerx = width/2
                camera_centery = height/2

                angle = get_angle(bottomRight, bottomLeft)

                value1 = X[0][0]
                                
                if (288 <= value1 <= 352): 
                    print('CENTER')
                    # GPIO.output(Bit1, GPIO.LOW)
                    # GPIO.output(Bit2, GPIO.LOW)
                   
                elif (value1 > 352):
                    print('RIGHT')
                    # GPIO.output(Bit1, GPIO.HIGH)
                    # GPIO.output(Bit2, GPIO.HIGH)
                   
                elif (value1 < 288): 
                    print('LEFT')
                    # GPIO.output(Bit1, GPIO.HIGH)
                    # GPIO.output(Bit2, GPIO.LOW)
                   

                if visual == True:
                    draw_aruco(frame, topLeft, topRight, bottomLeft,
                               bottomRight, MidP, X, Y, angle)

        if visual == True:
            cv2.imshow(window_name, gray)  # Despliega la ventana

            if cv2.waitKey(1) & 0xFF == 27:  # Presiona esc para salir
                break

    capture.release()
    cv2.destroyAllWindows()
