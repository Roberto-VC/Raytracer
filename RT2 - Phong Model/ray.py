from code import interact
from gl import *
from vector import *
from sphere import *
from intersect import *
from light import *
from material import *


def reflect(I, N):
    return (I - N * 2 * (N @ I)).normalize()


class Raytracer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.spheres = [
            Sphere(
                V3(-3, 0, -12),
                1,
                Material(diffuse=(255, 255, 255), albedo=[0.8, 0.2], spec=0),
            ),
            Sphere(
                V3(-2.5, 0.25, -10),
                0.40,
                Material(diffuse=(255, 255, 255), albedo=[0.8, 0.2], spec=0),
            ),
            Sphere(
                V3(-4.75, -1.5, -25),
                1,
                Material(diffuse=(255, 255, 255), albedo=[0.8, 0.2], spec=0),
            ),
            Sphere(
                V3(-7.75, -1.5, -25),
                1,
                Material(diffuse=(255, 255, 255), albedo=[0.8, 0.2], spec=0),
            ),
            Sphere(
                V3(-3.25, 1.75, -13),
                1.15,
                Material(diffuse=(240, 255, 210), albedo=[0.7, 0.2], spec=20),
            ),
            Sphere(
                V3(-8.55, 2.5, -25),
                1,
                Material(diffuse=(255, 255, 255), albedo=[0.8, 0.2], spec=0),
            ),
            Sphere(
                V3(-3.55, 2.45, -25),
                1,
                Material(diffuse=(255, 255, 255), albedo=[0.8, 0.2], spec=0),
            ),
            Sphere(
                V3(-8.55, 5.5, -25),
                1,
                Material(diffuse=(255, 255, 255), albedo=[0.8, 0.2], spec=0),
            ),
            Sphere(
                V3(-4.00, 5.45, -25),
                1,
                Material(diffuse=(255, 255, 255), albedo=[0.8, 0.2], spec=0),
            ),
            Sphere(
                V3(-1.45, -0.20, -5),
                0.075,
                Material(diffuse=(0, 0, 0), albedo=[0.6, 0.1], spec=1),
            ),
            Sphere(
                V3(-1.07, -0.20, -5),
                0.075,
                Material(diffuse=(0, 0, 0), albedo=[0.6, 0.1], spec=1),
            ),
            Sphere(
                V3(3.25, 1.75, -13),
                1.15,
                Material(diffuse=(165, 42, 42), albedo=[0.6, 0.3], spec=50),
            ),
            Sphere(
                V3(3, 0, -12),
                1,
                Material(diffuse=(210, 125, 45), albedo=[0.95, 0.3], spec=10),
            ),
            Sphere(
                V3(2.5, 0.25, -10),
                0.40,
                Material(diffuse=(210, 125, 45), albedo=[0.6, 0.3], spec=10),
            ),
            Sphere(
                V3(4.75, -1.5, -25),
                1,
                Material(diffuse=(210, 125, 45), albedo=[0.6, 0.3], spec=10),
            ),
            Sphere(
                V3(7.75, -1.5, -25),
                1,
                Material(diffuse=(210, 125, 45), albedo=[0.6, 0.3], spec=10),
            ),
            Sphere(
                V3(8.55, 2.5, -25),
                1,
                Material(diffuse=(210, 125, 45), albedo=[0.95, 0.2], spec=10),
            ),
            Sphere(
                V3(3.55, 2.45, -25),
                1,
                Material(diffuse=(210, 125, 45), albedo=[0.95, 0.2], spec=10),
            ),
            Sphere(
                V3(8.55, 5.5, -25),
                1,
                Material(diffuse=(210, 125, 45), albedo=[0.95, 0.2], spec=10),
            ),
            Sphere(
                V3(4.00, 5.45, -25),
                1,
                Material(diffuse=(210, 125, 45), albedo=[0.95, 0.2], spec=10),
            ),
            Sphere(
                V3(1.45, -0.20, -5),
                0.075,
                Material(diffuse=(60, 60, 60), albedo=[0.6, 0.1], spec=1),
            ),
            Sphere(
                V3(1.07, -0.20, -5),
                0.075,
                Material(diffuse=(60, 60, 60), albedo=[0.6, 0.1], spec=1),
            ),
            Sphere(
                V3(1.25, 0.10, -5),
                0.075,
                Material(diffuse=(60, 60, 60), albedo=[0.6, 0.1], spec=20),
            ),
            Sphere(
                V3(-1.25, 0.10, -5),
                0.075,
                Material(diffuse=(60, 60, 60), albedo=[0.6, 0.1], spec=20),
            ),
        ]
        self.clear_color = (0, 0, 0)
        self.current_color = (255, 255, 255)
        self.light = Light(V3(0, 0, 0), 1, (255, 255, 255))
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
        material, intersect = self.scene_intersect(origin, direction)
        if not material:
            return self.clear_color

        light_dir = (self.light.position - intersect.point).normalize()
        diff_intensity = light_dir @ intersect.normal
        diffuse = (
            int(material.diffuse[0] * diff_intensity * material.albedo[0]),
            int(material.diffuse[1] * diff_intensity * material.albedo[0]),
            int(material.diffuse[2] * diff_intensity * material.albedo[0]),
        )

        light_reflection = reflect(light_dir, intersect.normal)
        reflection_intensity = max(0, light_reflection @ direction)
        specular_intensity = (
            self.light.intensity * reflection_intensity**material.spec
        )
        specular = tuple(
            [x * specular_intensity * material.albedo[1] for x in self.light.c]
        )
        end = (
            int(specular[0] + diffuse[0]),
            int(specular[1] + diffuse[1]),
            int(specular[2] + diffuse[2]),
        )

        return end

    def scene_intersect(self, origin, direction):
        zBuffer = 999999
        material = None
        intersect = None
        for o in self.spheres:
            objintersect = o.ray_intersect(origin, direction)
            if objintersect:
                if objintersect.distance < zBuffer:
                    zBuffer = objintersect.distance
                    material = o.material
                    intersect = objintersect
        return material, intersect

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
                            min(255, self.framebuffer[x][y][0]),
                            min(255, self.framebuffer[x][y][1]),
                            min(255, self.framebuffer[x][y][2]),
                        )
                    )


ray = Raytracer(500, 500)
ray.render()
ray.write("TeddyBear.bmp")
