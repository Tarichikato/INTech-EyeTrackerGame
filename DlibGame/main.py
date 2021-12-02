import cv2
from Orientation import get_orientation,get_up_down
from skimage.io import imread
from get_dlib_pts import PtsGetter
from Ball import Ball
from mouth import mouth_opened
import random
import math
import numpy as np


def scale(shape, position):
    return (int(position[0] / 2000 * shape[0]),int(position[1] / 3000 * shape[1]))


def sort_by_values(dicti):
    dicti = dict(sorted(dicti.items(), key=lambda item: item[1]))
    return (dicti)

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

f = open("leaderboard.txt", "r")
leaderboard = {}
for line in  f.readlines():
    sco = line.split(':')
    sco[1] = int(sco[1].replace("\n",""))
    leaderboard[sco[0]] = sco[1]

score = 0

leaderboard = sort_by_values(leaderboard)
print(leaderboard)


print("Enter your pseudo :")
name = input()

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
        bombs.append(Ball(position,[random.randrange(5,30),random.randrange(5,30)],(0,0,0),15))
        score = len(bombs)
        leaderboard[f"You ({name})"] = score
        leaderboard = sort_by_values(leaderboard)
    previous_open_mouth = open_mouth
    gaze_status = ''
    up_down = ''
    f1 = scale(img.shape,position)
    cv2.circle(img, f1, my_radius, my_color, -1)

    for bomb in bombs:
        if (bomb.enable):
            f_ball = scale(img.shape, bomb.position)
            '''if ((f1[0] - f_ball[0]) ** 2 + (f1[1] - f_ball[1]) ** 2) < (my_radius + bomb.radius) ** 2:
                # angle =
                bomb.speed = [-bomb.speed[0], -bomb.speed[1]]
                bomb.disable()'''
            '''print(f"Distance  y: {(f1[0]-ball.position[0])} x{ (position[1]-ball.position[1])} vs {(my_radius + ball.radius)**2}")
            print('')'''

            cv2.circle(img, f_ball, bomb.radius, bomb.color, -1)
            bomb.update()

    x_mid = frame.shape[1]

    for i in range(len(pts)):
        cv2.circle(img, pts[i], 2, (0, 255, 0), -1, 8)

    # font
    font = cv2.FONT_HERSHEY_SIMPLEX
    # org
    # fontScale
    fontScale = 1
    # Blue color in BGR
    color = (255, 0, 0)
    # Line thickness of 2 px
    thickness = 2
    for id,player in enumerate(list(leaderboard.keys())[::-1]):
        org = (50, 50*(id+1))
        cv2.putText(img, f" {id +1} {player} : {leaderboard[player]}", org, font,fontScale, color, thickness, cv2.LINE_AA)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == 27:
        score = len(bombs)
        f = open("leaderboard.txt", "a")
        f.write(f'{name} : {score}\n')
        f.close()
        break
cap.release()
cv2.destroyAllWindows()


