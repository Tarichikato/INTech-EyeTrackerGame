
import dlib  
import cv2

class PtsGetter():
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("./Data/shape_predictor_68_face_landmarks.dat")


    def get_pts(self,im):
        img_gray = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
        faces = self.detector(img_gray, 0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        pts = []
        x_mid = im.shape[1]
        if (len(faces) != 0):
            #On peut imaginer utiliser tous les visages pour du combat multijoueur
            #for i in range(len(faces)):
            i = 0
            for k, d in enumerate(faces):
                # draw red rectangle on the face
                # cv2.rectangle(im_rd, (d.left(), d.top()), (d.right(), d.bottom()), (0, 0, 255))
                # use the detector to get the 68 points
                shape = self.predictor(im, d)
                # draw a circle in landmark
                for i in range(68):
                    pts.append(((x_mid - shape.part(i).x, shape.part(i).y)))
        return(pts)