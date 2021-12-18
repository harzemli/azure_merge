# Standard imports
import cv2
import math
import matplotlib.pyplot as plt
import numpy as np
import socket
import time
from matplotlib.widgets import Button

LAPTOP_CAMERA_ID = 0
EXTERNAL_CAMERA_ID = 1
global keepWidget


def callbackStop(event):
    plt.close()


def calculateDistTravel(init_x, init_y, final_x, final_y, coords):
    total_coordinates = len(coords)
    min_dist_start = 10
    min_dist_final = 10
    start_index = 0
    final_index = 0
    for index in range(0, total_coordinates):
        current_x = coords[index][0]
        current_y = coords[index][1]
        dist_start = math.sqrt(((current_x-init_x)*pixelX)**2+((current_y-init_y)*pixelY)**2)
        dist_final = math.sqrt(((current_x-final_x)*pixelX)**2+((current_y-final_y)*pixelY)**2)
        if dist_start < min_dist_start:
            min_dist_start = dist_start
            start_index = index
        if dist_final < min_dist_final:
            min_dist_final = dist_final
            final_index = index
    dist_travelled = 0
    s = start_index
    if start_index < final_index:
        for pts in range(start_index+1, final_index+1):
            dist_travelled = dist_travelled + \
                math.sqrt(((coords[index][0]-coords[s][0])*pixelX)**2 +
                          ((coords[index][1]-coords[s][1])*pixelY)**2)
            s = pts
    elif start_index > final_index:
        for pts in range(start_index+1, total_coordinates):
            dist_travelled = dist_travelled + \
                math.sqrt(((coords[index][0]-coords[s][0])*pixelX)**2 +
                          ((coords[index][1]-coords[s][1])*pixelY)**2)
            s = pts
        for pts in range(0, final_index+1):
            dist_travelled = dist_travelled + \
                math.sqrt(((coords[index][0]-coords[s][0])*pixelX)**2 +
                          ((coords[index][1]-coords[s][1])*pixelY)**2)
            s = pts
    elif start_index == final_index:
        dist_travelled = 0

    return dist_travelled


def getTrackCoordinates():
    # image=cv2.imread("C:/Users/srrajago/Pictures/Camera Roll/CompleteImage.jpg",0)
    # add the path to the image or image fro video cam
    image = cv2.imread(r"C:\Users\patluu\Documents\slotRacer\map2.png", 0)
    if image is None:
        print("Image not found.")
        exit()
    ret, thresh_img = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    num_labels, labels_im, stats, centroid = cv2.connectedComponentsWithStats(thresh_img, 8)
    img2 = np.zeros(image.shape)
    i = 0
    img2[labels_im == i] = 1
    img_size = img2.shape
    coordinates = []
    for index_y in range(0, img_size[0]):
        for index_x in range(0, img_size[1]):
            if labels_im[index_y][index_x] == 0:
                indices = [index_x, index_y]
                coordinates.append(indices)
    print(coordinates)
    return coordinates


CAMERA_ID = EXTERNAL_CAMERA_ID
# CAMERA_ID = LAPTOP_CAMERA_ID
cam_distance = 39.9
keepWidget = True
# Camera Properties
if CAMERA_ID == 0:

    # distance of the camera from track (in cms)
    resX = 1280
    resY = 720

    # Initialize distances
    ratioX = 20.25/30.5
    ratioY = 11.5/30.5
    half_distX = ratioX*cam_distance
    half_distY = ratioY*cam_distance
    pixelX = half_distX/(resX/2)
    pixelY = half_distY/(resY/2)
elif CAMERA_ID == 1:
    FOV = 77
    resX = 1920
    resY = 1080
    ratioX = math.tan(math.radians(FOV/2))
    ratioY = ratioX*resY/resX
    half_distX = ratioX*cam_distance
    half_distY = ratioY*cam_distance
    pixelX = half_distX/(resX/2)
    pixelY = half_distY/(resY/2)

# initialize plot properties
xdata = []
ydata = []
i = 0
plt.show()
plt.xlabel("Time  (in seconds)")
plt.ylabel("Velocity of the object (in cm/s)")
axes = plt.gca()
axes.set_xlim(0, 100)
axes.set_ylim(0, 5)
l, = axes.plot(xdata, ydata, 'r-')
baxis = plt.axes([0.7, 0.05, 0.1, 0.075])
bstop = Button(baxis, 'STOP')
bstop.on_clicked(callbackStop)

# Initialize image capture
video = cv2.VideoCapture(CAMERA_ID)
ok, im = video.read()
starttime = time.time()
simstarttime = starttime
im1 = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
lower_blue = np.array([110, 50, 50])
upper_blue = np.array([130, 255, 255])
# lower_blue=np.array([255,40,0])
# upper_blue=np.array([255,255,255])
# play around
mask1 = cv2.inRange(im1, (0, 50, 20), (5, 255, 255))
mask2 = cv2.inRange(im1, (175, 50, 20), (180, 255, 255))
# mask = cv2.inRange(im, lower_blue, upper_blue)
mask = cv2.bitwise_or(mask1, mask2)
croped = cv2.bitwise_and(im1, im1, mask=mask)

# mask = cv2.inRange(im, lower_blue, upper_blue)

im2 = cv2.bitwise_and(im1, im1, mask=mask)

cnts, img = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
maxArea = 0
index = 0
for c in cnts:
    M = cv2.moments(c)
    if M["m00"] == 0:
        pass
    else:
        if cv2.contourArea(c) > maxArea:
            maxArea = cv2.contourArea(c)
            cX_start = int(M["m10"] / M["m00"])
            cY_start = int(M["m01"] / M["m00"])

# velocity=0
# coo=getTrackCoordinates()
UDP_IP = "127.0.0.1"
UDP_PORT = 4242
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))
while True:
    data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
    if data:
        print("received message:", data)
        while(keepWidget):
            # Read a new frame
            ok, im = video.read()
            endtime = time.time()
            im1 = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
            lower_blue = np.array([110, 50, 50])
            upper_blue = np.array([130, 255, 255])
            # mask of yellow (15,0,0), (36, 255, 255)
            # play around
            mask1 = cv2.inRange(im1, (0, 50, 20), (5, 255, 255))  # red
            mask2 = cv2.inRange(im1, (175, 50, 20), (180, 255, 255))  # red
            # mask = cv2.inRange(im, lower_blue, upper_blue)
            mask = cv2.bitwise_or(mask1, mask2)
            # crop the video
            cropped = cv2.bitwise_and(im1, im1, mask=mask)
            # cv2.imshow("croped", croped)
            cv2.imshow("Webcam Image", im)
            cv2.waitKey(1)
            im2 = cv2.bitwise_and(im1, im1, mask=mask)

            cnts, img = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            maxArea = 0

            tdelta = endtime-starttime
            for c in cnts:
                M = cv2.moments(c)
                if M["m00"] == 0:
                    pass
                else:
                    if cv2.contourArea(c) > maxArea:
                        maxArea = cv2.contourArea(c)
                        # Acquiring the cooridnates of center of blob
                        cX = int(M["m10"] / M["m00"])
                        cY = int(M["m01"] / M["m00"])
                        print(cX, cY)
                        coordinates = str(cX) + "," + str(cY)
                        sock.sendto(coordinates.encode('utf-8'), addr)
                        time.sleep(.2)

            '''
            dist=calculateDistTravel(cX_start,cY_start,cX,cY,coo)
            velocity=dist/tdelta
            xdata.append(endtime-simstarttime)
            ydata.append(velocity)
            axes.set_xlim(0,max(xdata))
            axes.set_ylim(0,max(ydata))
            l.set_xdata(xdata)
            l.set_ydata(ydata)
            plt.draw()
            plt.pause(0.00001)
            starttime=endtime
            cX_start=cX
            cY_start=cY
            '''
