import flimage
import numpy as np

from .elements import Sphere


class Fluorescence(object):

    def __init__(self, phantom, grid_size, pixel_size, displacement=(0, 0)):
        """Fluorescence projector

        Notes
        -----
        - The origin of the coordinate system is the center of the grid.
          For even grid sizes, the origin is between two pixels. For odd
          grid sizes the origin coincides with the center pixel.
        """
        self.phantom = phantom
        self.pixel_size = pixel_size
        self.grid_size = grid_size
        gx, gy = grid_size
        #: center of the volume used
        self.center = np.array([gx, gy, 0]) / 2 - .5
        self.center[0] += displacement[0]
        self.center[1] += displacement[1]

    def project(self):
        fluor = np.zeros(self.grid_size, dtype=float)
        for element in self.phantom:
            if isinstance(element, Sphere):
                fluor += self.project_sphere(element)

        flifull = flimage.FLImage(
                    data=fluor,
                    meta_data={
                        "pixel size": self.pixel_size,
                        }
                    )
        return flifull

    def project_sphere(self, sphere):
        center = self.center + sphere.center/self.pixel_size
        # grid
        x = np.arange(self.grid_size[0]).reshape(-1, 1)
        y = np.arange(self.grid_size[1]).reshape(1, -1)
        cx, cy, _ = center
        # sphere location
        rpx = sphere.radius / self.pixel_size
        r = rpx**2 - (x - cx)**2 - (y - cy)**2
        # distance
        z = np.zeros_like(r)
        rvalid = r > 0
        z[rvalid] = 2 * np.sqrt(r[rvalid])

        fluor = z * sphere.fl_brightness
        return fluor
