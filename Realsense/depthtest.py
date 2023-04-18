import pyrealsense2 as rs
import numpy as np
import time

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)

pipeline.start(config)
count = 0
#try:
while True:
    frames = pipeline.wait_for_frames()
    depth = frames.get_depth_frame()

    if not depth: continue

    count +=1
    x1, y1 = 320, 240
    midx, midy = 640, 480

    #Pixel 1
    dist = depth.get_distance(x1, y1)
    #dist = dist*100
    print("Pixel 1 Distance:", dist)

    #Mid Pixel
    #dist = depth.get_distance(midx, midy)
    #dist = dist*100
    # print("mid Pixel Distance in mm:", dist)

    #pipeline.stop()
   # exit(0)

#except Exception as e:
 #   print(e)
  #  pass
