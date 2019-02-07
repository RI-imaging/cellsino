import numpy as np
import qpsphere

from .base_propagator import BasePropagator


class Rytov(BasePropagator):
    """Rytov approximation"""

    def propagate_sphere(self, sphere, grid_sampling=150):
        center = self.center + sphere.points[0]/self.pixel_size
        # speed up computation for smaller spheres on large grid
        n = np.max(self.grid_size) * self.pixel_size / sphere.radius
        radius_sampling = grid_sampling / n
        qpi = qpsphere.models.rytov(radius=sphere.radius,
                                    sphere_index=sphere.object_index,
                                    medium_index=sphere.medium_index,
                                    wavelength=self.wavelength,
                                    pixel_size=self.pixel_size,
                                    grid_size=self.grid_size,
                                    center=center[:2],
                                    focus=-center[2]*self.pixel_size,
                                    radius_sampling=radius_sampling,
                                    )
        return qpi
