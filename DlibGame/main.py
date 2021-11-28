import cv2
from Orientation import get_orientation,get_up_down
from skimage.io import imread
from get_dlib_pts import PtsGetter
from Ball import Ball
import math


def scale(shape, position):
    return (int(position[0] / 2000 * shape[0]),int(position[1] / 3000 * shape[1]))

my_radius = 50
player_speed = 15
cap= cv2.VideoCapture(0)
a_gaze_status = ''
gaze_status = ''
up_down = ''
pts_getter = PtsGetter()

position =[1500,1000]
ball1 = Ball((2500,500),[-16,5],(255,0,0),25)
ball2 = Ball((2500,750),[-7,10],(255,0,0),25)
ball3 = Ball((2500,1000),[-10,5],(255,0,0),25)
ball4 = Ball((2500,1250),[-11,3],(255,0,0),25)
ball5 = Ball((2500,1500),[-12,8],(255,0,0),25)
ball6 = Ball((2500,1750),[-5,0],(255,0,0),25)

balls = [ball1,ball2,ball3,ball4,ball5,ball6]
while True:
    img = imread('./Data/fondTable21.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    ret, frame= cap.read()
    pts = pts_getter.get_pts(frame)

    if(len(pts) == 68):
        gaze_status = get_orientation(pts)
        up_down = get_up_down(pts)

    if(gaze_status == 'l' and position[0] > 10):
        position[0]-=player_speed
    if (gaze_status == 'r' and position[0]< 2990):
        position[0] += player_speed
    if (up_down == 'd' and position[1] < 1990):
        position[1] += player_speed
    if (up_down == 'u' and position[1] >10):
        position[1] -= player_speed
    gaze_status = ''
    up_down = ''
    f1 = scale(img.shape,position)
    cv2.circle(img, f1, my_radius, (0, 0, 255), -1)
    for ball in balls:
        if(ball.enable):
            f_ball = scale(img.shape, ball.position)
            if ((f1[0]-f_ball[0])**2 + (f1[1]-f_ball[1])**2) < (my_radius + ball.radius)**2:
                #angle =
                ball.speed = [-ball.speed[0],-ball.speed[1]]
                ball.disable()
            '''print(f"Distance  y: {(f1[0]-ball.position[0])} x{ (position[1]-ball.position[1])} vs {(my_radius + ball.radius)**2}")
            print('')'''

            cv2.circle(img, f_ball, ball.radius, ball.color, -1)
            ball.update()

    x_mid = frame.shape[1]

    for i in range(len(pts)):
        cv2.circle(img, pts[i], 2, (0, 255, 0), -1, 8)


    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()


