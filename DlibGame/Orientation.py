# coding=utf-8
import cv2
import dlib
import numpy as np
from math import hypot


def get_orientation(pts):

    #Projetion de l'écart de 2 - 31
    d = pts[1][0] - pts[30][0]
    #Projetion de l'écart de 16 - 31
    g = pts[15][0] - pts[31][0]
    status = ''
    if(g != 0):
        r = abs(d)/abs(g)
        if(r<0.8):
            status = 'r'
        elif(r>1.2):
            status = 'l'
        else:
            status = 'c'
    return status

def get_up_down(pts):
    # Projetion de l'écart de 2 - 31
    l = abs(pts[27][1] - pts[30][1])
    if(l>60):
        return('d')
    if(l<50):
        return('u')
    return ''

