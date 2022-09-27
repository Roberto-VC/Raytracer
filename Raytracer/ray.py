import this
from gl import *
from vector import *
from sphere import *


class Raytracer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.spheres = [
            Sphere(V3(0, -1.75, -13), 2, (255, 255, 255)),
            Sphere(V3(0, 3, -13), 3, (255, 255, 255)),
            Sphere(V3(0, -1.5, -13), 0.33, (255, 150, 0)),
            Sphere(V3(1, -2, -13), 0.33, (0, 0, 0)),
            Sphere(V3(-1, -2, -13), 0.33, (0, 0, 0)),
            Sphere(V3(0, -0.53, -13), 0.25, (0, 0, 0)),
            Sphere(V3(-0.5, -0.66, -13), 0.25, (0, 0, 0)),
            Sphere(V3(0.5, -0.66, -13), 0.25, (0, 0, 0)),
            Sphere(V3(-1.0, -0.86, -13), 0.25, (0, 0, 0)),
            Sphere(V3(1.0, -0.86, -13), 0.25, (0, 0, 0)),
            Sphere(V3(0, 2, -13), 0.25, (0, 0, 0)),
            Sphere(V3(0, 3, -13), 0.25, (0, 0, 0)),
            Sphere(V3(0, 4, -13), 0.25, (0, 0, 0)),
        ]
        self.clear_color = (0, 0, 0)
        self.current_color = (255, 255, 255)
        self.clear()

    def point(self, x, y, c=None):
        if y > 0 and y < self.height and x > 0 and x < self.width:
            self.framebuffer[y][x] = c or self.current_color

    def color(self, r, g, b):
        return (b, g, r)

    def clear(self):
        self.framebuffer = [
            [self.clear_color for x in range(self.width)] for y in range(self.height)
        ]

    def render(self):
        fov = int(pi / 2)
        ar = self.width / self.height
        tana = tan(fov / 2)
        for y in range(self.height):
            for x in range(self.width):
                i = ((2 * (x + 0.5) / self.width) - 1) * ar * tana
                j = (1 - (2 * (y + 0.5) / self.height)) * tana
                direction = V3(i, j, -1).normalize()
                origin = V3(0, 0, 0)
                c = self.cast_ray(origin, direction)
                c = tuple(reversed(c))
                self.point(x, y, c)

    def cast_ray(self, origin, direction):

        m = self.clear_color
        for x in self.spheres:
            if x.ray_intersect(origin, direction):
                m = x.color
        return m

    def write(self, file):
        with open(file, "wb") as f:
            f.write(
                struct.pack(
                    "<hlhhl",
                    19778,
                    14 + 40 + self.height * self.width * 3,
                    0,
                    0,
                    40 + 14,
                )
            )  # Writing BITMAPFILEHEADER
            f.write(
                struct.pack(
                    "<lllhhllllll",
                    40,
                    self.width,
                    self.height,
                    1,
                    24,
                    0,
                    self.width * 3 * self.height,
                    0,
                    0,
                    0,
                    0,
                )
            )  # Writing BITMAPINFO
            for x in range(self.width):
                for y in range(self.height):
                    f.write(
                        struct.pack(
                            "<BBB",
                            self.framebuffer[x][y][0],
                            self.framebuffer[x][y][1],
                            self.framebuffer[x][y][2],
                        )
                    )


ray = Raytracer(500, 500)
ray.render()
ray.write("Snowman.bmp")
