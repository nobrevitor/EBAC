import math
class Point:

    def __init__(self, initX, initY):

        self.x = initX
        self.y = initY

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def distanceFromOrigin(self):
        return ((self.x ** 2) + (self.y ** 2)) ** 0.5

    def __str__(self):
        return "x=" + str(self.x) + ", y=" + str(self.y)

    def halfway(self, target):
         mx = (self.x + target.x)/2
         my = (self.y + target.y)/2
         return Point(mx, my)

    def distancia (self, point):
        nx = point.getX() - self.x
        ny = point.getY() - self.y
        dist = math.sqrt((nx**2) + (ny**2))
        return dist
    
    def reflect_x (self):
        reflected = self.y - 2*self.y
        return Point(self.x, reflected)
    
    def slope_from_origin(self):
        angle_radians = math.atan2(self.y, self.x)
        angle_degrees = math.degrees(angle_radians)
        return angle_degrees

p = Point(1,3)
q = Point(0,8)
r = Point(3,5)
o =  Point(0,0)
print(o.slope_from_origin())
