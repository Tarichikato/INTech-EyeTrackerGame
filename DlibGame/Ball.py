


class Ball():
    def __init__(self,position,speed,color,radius):
        self.speed = speed
        self.color = color
        self.radius = radius
        self.position = position
        self.enable = True

    def update(self):
        if (self.enable):
            if((self.position[0] + self.speed[0]) > 3000 or self.position[0] + self.speed[0] < 0):
                self.speed[0] = -self.speed[0]
            if ((self.position[1] + self.speed[1]) > 2000 or self.position[1] + self.speed[1] < 0):
                self.speed[1] = -self.speed[1]
            self.position = (self.position[0] + self.speed[0],self.position[1] + self.speed[1])
    def disable(self):
        self.enable = False