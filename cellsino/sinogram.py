import pathlib

import h5py
import numpy as np
import qpimage

from .propagators import dictionary as pp_dict


class Sinogram(object):
    def __init__(self, phantom, wavelength, pixel_size, grid_size):
        self.phantom = phantom
        self.wavelength = wavelength
        self.pixel_size = pixel_size
        self.grid_size = grid_size

    def compute(self, angles, path=None, propagator="rytov"):
        if isinstance(angles, int):
            angles = np.linspace(0, 2*np.pi, angles, endpoint=False)

        if path:
            write = True
            path = pathlib.Path(path)
            if path.exists():
                path.unlink()
        else:
            write = False
            sino_fields = np.zeros((angles.size,
                                    self.grid_size[0],
                                    self.grid_size[1]),
                                   dtype=complex)
            sino_fluor = np.zeros((angles.size,
                                   self.grid_size[0],
                                   self.grid_size[1]),
                                  dtype=float)

        for ii, ang in enumerate(angles):
            print(ii)
            ph = self.phantom.transform(rot_main=ang)

            pp = pp_dict[propagator](phantom=ph,
                                     wavelength=self.wavelength,
                                     pixel_size=self.pixel_size,
                                     grid_size=self.grid_size)

            qpi = pp.propagate()

            if write:
                with h5py.File(path, "a") as h5:
                    qps = qpimage.QPSeries(h5file=h5.require_group("qpseries"))
                    qps.add_qpimage(qpi)
            else:
                sino_fields[ii] = qpi.field

        if write:
            return path
        else:
            return sino_fields, sino_fluor
