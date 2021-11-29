import random

def mouth_opened(pts):
    x = random.random()
    d = abs(pts[62][1] - pts[66][1])
    if(d > 20):
        return(True)
    return(False)