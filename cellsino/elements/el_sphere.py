import numpy as np

from .base_element import BaseElement


class Sphere(BaseElement):
    def __init__(self, object_index, medium_index, fl_brightness,
                 center, radius):
        """Sphere element

        Parameters
        ----------
        object_index: float
            Refractive index of the element
        medium_index: float
            Refractive index of surrounding medium
        fl_brightness: float
            Fluorescence brightness
        center: list-like
            Center coordinates (x, y, z) of the sphere [m]
        radius:
            Radius of the sphere [m]
        """
        #: radius of the sphere
        self.radius = radius
        points = np.atleast_2d(center)
        super(Sphere, self).__init__(object_index=object_index,
                                     medium_index=medium_index,
                                     fl_brightness=fl_brightness,
                                     points=points)

    def draw(self, pixel_size, grid_size):
        ri = self.medium_index * np.ones(grid_size, dtype=float)
        center = np.array(grid_size) / 2 - .5
        x = (np.arange(grid_size[0]) - center[0]) * pixel_size
        y = (np.arange(grid_size[1]) - center[1]) * pixel_size
        z = (np.arange(grid_size[2]) - center[2]) * pixel_size

        xx, yy, zz = np.meshgrid(x, y, z, indexing="ij")
        cx, cy, cz = self.center

        volume = (cx-xx)**2 + (cy-yy)**2 + (cz-zz)**2
        inside = volume <= self.radius**2
        ri[inside] = self.object_index
        return ri
