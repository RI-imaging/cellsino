import abc

import numpy as np
import qpimage

from ..elements import Sphere


class BasePropagator(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, phantom, grid_size, pixel_size, wavelength,
                 displacement=(0, 0)):
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
        gx, gy = grid_size
        #: center of the volume used
        self.center = np.array([gx, gy, 0]) / 2 - .5
        self.center[0] += displacement[0]
        self.center[1] += displacement[1]

    def propagate(self):
        # dtype was previously np.complex256 which caused tests to
        # fail on Windows (no support). I assume that regular double
        # precision is enough here.
        field = np.ones(self.grid_size, dtype=np.complex128)
        for element in self.phantom:
            if isinstance(element, Sphere):
                field *= self.propagate_sphere(element).field
        qpifull = qpimage.QPImage(
                    data=field,
                    which_data="field",
                    meta_data={
                        "wavelength": self.wavelength,
                        "pixel size": self.pixel_size,
                        "medium index": self.phantom.medium_index,
                        }
                    )
        return qpifull

    @abc.abstractmethod
    def propagate_sphere(self, sphere):
        pass
