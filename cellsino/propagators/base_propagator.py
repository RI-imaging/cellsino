import abc

import numpy as np

from ..elements import Sphere


class BasePropagator(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, phantom, wavelength, pixel_size, grid_size):
        """Base propagator

        Notes
        -----
        - The origin of the coordinate system is the center of the grid.
          For even grid sizes, the origin is between two pixels. For odd
          grid sizes the origin coincides with the center pixel.
        """
        self.phantom = phantom
        self.wavelength = wavelength
        self.pixel_size = pixel_size
        self.grid_size = grid_size
        self.center = np.array(self.grid_size) / 2 - .5

    def propagate(self):
        field = np.ones(self.grid_size, dtype=np.complex256)
        for element in self.phantom:
            if isinstance(element, Sphere):
                field *= self.propagate_sphere(element)
        return field

    @abc.abstractmethod
    def propagate_sphere(self, sphere):
        pass
