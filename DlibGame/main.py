import cv2
from KeyPoints import Gaze
from skimage.io import imread


def scale(shape, position):
    return (int(position[0] / 3000 * shape[1]), int(position[1] / 2000 * shape[0]))

cap= cv2.VideoCapture(0)
a_gaze_status = ''


position =[1500,1000]
while True:
    img = imread('fondTable21.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    ret, frame= cap.read()
    gaze_status, new_frame = Gaze.gaze_aversion(frame)

    if(gaze_status != a_gaze_status):
        print(gaze_status)
    if(gaze_status == 'Right' and position[0] > 10):
        position[0]-=10
    if (gaze_status == 'Left' and position[0]< 2990):
        position[0] += 10
    a_gaze_status = gaze_status
    f1 = scale(img.shape,position)
    cv2.circle(img, f1, 50, (0, 0, 255), -1)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()


