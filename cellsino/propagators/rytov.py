import qpsphere

from .base_propagator import BasePropagator


class Rytov(BasePropagator):
    """Rytov approximation"""

    def propagate_sphere(self, sphere):
        center = self.center + sphere.points[0]/self.pixel_size
        qpi = qpsphere.models.rytov(radius=sphere.radius,
                                    sphere_index=sphere.object_index,
                                    medium_index=sphere.medium_index,
                                    wavelength=self.wavelength,
                                    pixel_size=self.pixel_size,
                                    grid_size=self.grid_size,
                                    center=center)
        return qpi.field
