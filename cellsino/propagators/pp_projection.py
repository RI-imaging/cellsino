import qpsphere

from .base_propagator import BasePropagator


class Projection(BasePropagator):
    """Projection approximation"""

    def propagate_sphere(self, sphere):
        center = self.center + sphere.points[0]/self.pixel_size
        qpi = qpsphere.models.projection(radius=sphere.radius,
                                         sphere_index=sphere.object_index,
                                         medium_index=sphere.medium_index,
                                         wavelength=self.wavelength,
                                         pixel_size=self.pixel_size,
                                         grid_size=self.grid_size,
                                         center=center[:2],
                                         )
        return qpi
