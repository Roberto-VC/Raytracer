from vector import *


class Sphere(object):
    def __init__(self, center, radius, color):
        self.center = center
        self.radius = radius
        self.color = color

    def ray_intersect(self, origin, direction):
        L = self.center - origin
        tca = L @ direction
        l = L.length()
        d2 = l**2 - tca**2
        if d2 > self.radius**2:
            return False
        thc = (self.radius**2 - d2) ** 0.5
        t0 = tca - thc
        t1 = tca + thc
        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return False
        return True
