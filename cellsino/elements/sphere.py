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
