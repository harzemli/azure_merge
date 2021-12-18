# Standard imports
import cv2
import matplotlib.pyplot as plt
import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

LAPTOP_CAMERA_ID = 0
EXTERNAL_CAMERA_ID = 1

# CAMERA_ID = EXTERNAL_CAMERA_ID
CAMERA_ID = LAPTOP_CAMERA_ID

# Read image
# im = cv2.imread("blob.jpg", cv2.IMREAD_GRAYSCALE)

video = cv2.VideoCapture(CAMERA_ID)
ok, im = video.read()

im = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
# mask of yellow (15,0,0), (36, 255, 255)
mask1 = cv2.inRange(im, (20, 100, 100), (30, 255, 255))

mask2 = cv2.inRange(im, (78, 158, 124), (110, 255, 255))

mask = cv2.bitwise_or(mask1, mask2)
im = cv2.bitwise_and(im, im, mask=mask)
# im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)


# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

# Change thresholds
params.minThreshold = 10
params.maxThreshold = 200

# Filter by Area.
params.filterByArea = True
params.minArea = 15

# Filter by Circularity
params.filterByCircularity = False
params.minCircularity = 0.5

# Filter by Convexity
params.filterByConvexity = False
params.minConvexity = 0.5

# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.01

# Create a detector with the parameters
ver = (cv2.__version__).split('.')
if int(ver[0]) < 3:
    detector = cv2.SimpleBlobDetector(params)
else:
    detector = cv2.SimpleBlobDetector_create(params)

fig = plt.figure()
i = 0
X = list()
Y = list()

ip_port = ('127.0.0.1', 4242)
sock.bind(ip_port)
print("Bindig is complete")
print("waiting for client")
i = 0

data, addr = sock.recvfrom(1024)
print(data)

starttime = time.time()
endtime = starttime + 20

while time.time() < endtime:
    # Read a new frame
    ok, im = video.read()
    cv2.imshow("image", im)

    im = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    # mask of yellow (15,0,0), (36, 255, 255)
    mask1 = cv2.inRange(im, (20, 100, 100), (30, 255, 255))

    mask2 = cv2.inRange(im, (78, 158, 124), (110, 255, 255))

    mask = cv2.bitwise_or(mask1, mask2)
    im = cv2.bitwise_and(im, im, mask=mask)
    print(im.nonzero()[0].mean())
    print(im.nonzero()[1].mean())
    # im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    # Detect blobs.
    # keypoints = detector.detect(im)

    # if len(keypoints) > 0 :
    X.append(im.nonzero()[0].mean())
    Y.append(im.nonzero()[1].mean())
    # plt.scatter(im.nonzero()[0].mean(), im.nonzero()[1].mean())
    # plt.pause(0.001)

    # i += 1
    # else:
    # cv2.putText(im, "Tracking failure detected",
    #             (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
    # the size of the circle corresponds to the size of blob

    # im_with_keypoints = cv2.drawKeypoints(im, keypoints, numpy.array([]),
    #                                       (0, 0, 255),
    #                                       cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # Show blobs
    # cv2.imshow("Keypoints", im_with_keypoints)

    cv2.imshow("Keypoints", im)

    if 'nan' in str(im.nonzero()[0].mean()) or 'nan' in str(im.nonzero()[1].mean()):
        send_point = False
    else:
        send_point = True

    if data and send_point:
        print("received message:", data)
        final_track = [f"{im.nonzero()[0].mean()},{im.nonzero()[1].mean()}"]
        text = final_track[0]
        print(text)
        sock.sendto(text.encode('utf-8'), addr)
        '''
        time.sleep(.1)
        '''
        data, addr = sock.recvfrom(1024)
        print(data)

    # Exit if ESC pressed
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break

print("plot size = ", len(X))
plt.scatter(X, Y)
plt.show()
