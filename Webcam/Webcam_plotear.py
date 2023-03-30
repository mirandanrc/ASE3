import cv2
import numpy as np
import math
import matplotlib.pyplot as plt

#pip opencv-contrib-python: descarga libreria cv2, aruco, y si es necesario, numpy

#modifica imagen, le reduce el brillo
def change_brightness(img, value):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.add(v, value)
    v[v > 255] = 255
    v[v < 0] = 0
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

    return img

#funcion que consigue punto medio del eje x y y
def mid_points(matrix, pt1, pt2):
  matrix[0][0] = (pt1[0] + pt2[0]) / 2
  matrix[0][1] = (pt1[1] + pt2[1]) / 2
  return matrix

#conseguir el angulo de rotacion de los codigos aruco
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

#consigue angulo de rotacion de los codigos aruco en radianes
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


#funcion que dibuja e imprime informacion en el frame de opencv
def draw_aruco(frame, topLeft, topRight, bottomLeft, bottomRight, MidP, X, Y,angle):
       
  #Se dibuja el cuadrado 
  cv2.line(frame, topLeft, topRight, (0, 255, 0), 2)
  cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
  cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
  cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)

  #Se dibujan las lineas 
  line_thickness = 3
  cv2.line(frame, X[0], MidP[0], (0, 0, 255), thickness = line_thickness )
  cv2.line(frame, Y[0], MidP[0], (255, 0, 0), thickness = line_thickness )

  #Se imprime la información del texto 
  cv2.putText(frame, str(MidP[0]), (MidP[0][0], MidP[0][1] - 100),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,204,204),2,cv2.LINE_AA )
  cv2.putText(frame, str(f'ID: {markerID}'), (MidP[0][0] - 150, MidP[0][1] - 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 204, 204), 2, cv2.LINE_AA )
  cv2.putText(frame, str(angle) + " grados", (MidP[0][0] - 400, MidP[0][1] - 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 204, 204), 2, cv2.LINE_AA )

#conseguimos las coordenadas del aruco y lo guadamos como pares (x y y) en variables por seccion diferente
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

#almacenamos info de coordenadas y angulo del aruco, y la almacenamos en un diccionario
def get_ArucoInfo(markerCorner, markerID):

    topLeft, topRight, bottomLeft, bottomRight = get_coordenates(markerCorner)
 
    #Calculamos el angulo de inclinación 
    angle = get_anglerad(bottomRight, bottomLeft)

    info = {"coordenadas": [topLeft, topRight, bottomLeft, bottomRight], "angulo": (angle), "ID": (markerID)}

    return info


#si es True, se visualizara la camara y su interfaz, si es falsa ejecutará la camara sin mostrar nada
visual=True

if __name__=="__main__":

  capture = cv2.VideoCapture(1, cv2.CAP_DSHOW)
  qrCodeDetector = cv2.aruco

  window_name = 'Camara detector qr' #Nombre de la ventana

  #nuevoooo
  width=640
  height=480

  #resolucion HD
  capture.set(3, width)
  capture.set(4, height)
  
  points = np.arange(8).reshape(4,2)
  MidP = np.arange(2).reshape(1,2)
  Y = np.arange(2).reshape(1,2)
  X = np.arange(2).reshape(1,2)

  while (True):
    ret, frame = capture.read()
    if ret == False:
      break  #Por si acaso no detecta nada 
    frame = cv2.resize(frame, (640, 480)) #Cambiar el tamaño de la ventana que despliega
    frame = change_brightness(frame, 10)

    gray = cv2.cvtColor (frame, cv2.COLOR_BGR2GRAY)

    arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50)

    arucoParams = cv2.aruco.DetectorParameters()
    
    detector = cv2.aruco.ArucoDetector(arucoDict, arucoParams) ########

    points, ids, rejected = detector.detectMarkers(gray)
    
    if len(points) > 0:
      # flatten the ArUco IDs list
      ids = ids.flatten()
      # loop over the detected ArUCo corners
      for (markerCorner, markerID) in zip(points, ids):

          topLeft, topRight, bottomLeft, bottomRight = get_coordenates(markerCorner)

          #Obtenemos coordenadas para punto medio y lineas
          mid_points(MidP, topRight, bottomLeft)
          mid_points(Y, topRight, bottomRight)
          mid_points(X, bottomLeft, bottomRight)

        #Calculamos el centro de nuestra pantalla
          camera_centerx=width/2
          camera_centery=height/2
          
          #Calculamos el angulo de inclinación 
          angle = get_angle(bottomRight, bottomLeft)

        #Se genera un arreglo para guardar los valores del centro del aruco
          value1 = X[0][0]
          value2= Y[0][1]     
          array_2= np.array([[value1],[value2]])
          print(array_2)


        #Deteccion de los cuadrantes   
          if (288<=value1<=352 and 216<=value2<=264):
             print('CENTER')
          elif (value1>320 and value2<216) or (value1>352 and value2<240):
             print('CUADRANTE I')
          elif (value1<320 and value2<216) or (value1<288 and value2<240):
             print('CUADRANTE II')
          elif (value1<320 and value2>264) or (value1<288 and value2>240):
             print('CUADRANTE III')
          else:
             print('CUADRANTE IV') 

          
          #Limpiar el punto anterior
          #plt.cla()

          # limites de los ejes
          plt.xlim([-320, 320])
          plt.ylim([-240, 240])
                        
          # diibujando el centro de los ejes
          plt.axhline(y=0, color='k')
          plt.axvline(x=0, color='k')

          # datos a plotear
          x = (value1 - 320) * -1
          y = (value2 - 240) * -1
          #array_4= np.array([[x],[y]])
          plt.scatter(x,y)
          plt.draw()
          plt.pause(0.001)
          
          if visual==True:
            draw_aruco(frame, topLeft, topRight, bottomLeft, bottomRight, MidP, X, Y, angle)

            #print("Distancia del centro:", X[0][0], Y[0][1])
  
    if visual ==True:
      cv2.imshow(window_name, frame) #Despliega la ventana 

      if cv2.waitKey(1) & 0xFF == 27: #Presiona esc para salir 
        break
  
  capture.release()
  cv2.destroyAllWindows()
