import cv2
from Orientation import get_orientation,get_up_down
from skimage.io import imread
from get_dlib_pts import PtsGetter
from Ball import Ball
from mouth import mouth_opened
import math
import numpy as np


def scale(shape, position):
    return (int(position[0] / 2000 * shape[0]),int(position[1] / 3000 * shape[1]))

my_radius = 50
player_speed = 15
cap= cv2.VideoCapture(0)
a_gaze_status = ''
gaze_status = ''
up_down = ''
pts_getter = PtsGetter()
my_color = (0, 0, 255)
blink = False
open_mouth = False
previous_open_mouth = False

position =[1500,1000]



bombs = []
while True:
    img = imread('./Data/fondTable21.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    ret, frame= cap.read()
    pts = pts_getter.get_pts(frame)

    if(len(pts) == 68):
        gaze_status = get_orientation(pts)
        up_down = get_up_down(pts)
        # Detect blink
        open_mouth = mouth_opened(pts)




    if(gaze_status == 'l' and position[0] > 10):
        position[0]-=player_speed
    if (gaze_status == 'r' and position[0]< 2990):
        position[0] += player_speed
    if (up_down == 'd' and position[1] < 1990):
        position[1] += player_speed
    if (up_down == 'u' and position[1] >10):
        position[1] -= player_speed
    if (open_mouth and not previous_open_mouth):
        bombs.append(scale(img.shape,position))
    previous_open_mouth = open_mouth
    gaze_status = ''
    up_down = ''
    f1 = scale(img.shape,position)
    cv2.circle(img, f1, my_radius, my_color, -1)

    for bomb in bombs:
        cv2.circle(img, bomb, 25, (0,0,0), -1)

    x_mid = frame.shape[1]

    for i in range(len(pts)):
        cv2.circle(img, pts[i], 2, (0, 255, 0), -1, 8)


    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()


