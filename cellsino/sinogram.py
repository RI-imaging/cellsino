import pathlib

import h5py
import numpy as np
import qpimage

from .fluorescence import Fluorescence
from .propagators import prop_dict
from .phantoms import phan_dict


class Sinogram(object):
    def __init__(self, phantom, wavelength, pixel_size, grid_size):
        if isinstance(phantom, str):
            self.phantom = phan_dict[phantom]()
        else:
            self.phantom = phantom
        self.wavelength = wavelength
        self.pixel_size = pixel_size
        self.grid_size = grid_size

    def compute(self, angles, displacements=None, propagator="rytov",
                path=None, count=None, max_count=None):
        """Compute sinogram data

        Parameters
        ----------
        angles: 1d array of size N or int
            If an array, defines the angular positions for each frame
            of the rotation. If an int, defines the number of angles
            of a steady rotation from 0 to 2π.
        displacements: 2d ndarray of shape (N, 2) or float
            A float value indicates the standard deviation of a
            Gaussian noise distribution (using
            :func:`numpy.random.normal`) in pixels.
            A 2d array directly specifies the x-y-displacement for each
            frame in pixels.
        propagator: str
            The propagator to use. Must be in
            :data:`cellsino.propagators.available`.
        path: str or pathlib.Path
            If not None, the data will be written to this file and
            a :class:`pathlib.Path` object will be returned.
        count: multiprocessing.Value
            May be used for tracking progress. At each computed
            angle `count.value` is incremented by one.
        max_count: multiprocessing.Value
            May be used for tracking progress. This value is
            incremented by `N`.
        """
        if max_count is not None:
            max_count.value += angles.size

        if isinstance(angles, int):
            angles = np.linspace(0, 2*np.pi, angles, endpoint=False)

        if displacements is None:
            displacements = np.zeros((angles.shape[0], 2))
        elif isinstance(displacements, float):
            np.random.seed(47)  # for reproducibility
            displacements = np.random.normal(scale=displacements,
                                             size=(angles.shape[0], 2))

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
            ph = self.phantom.transform(rot_main=ang)

            pp = prop_dict[propagator](phantom=ph,
                                       grid_size=self.grid_size,
                                       pixel_size=self.pixel_size,
                                       wavelength=self.wavelength,
                                       displacement=displacements[ii])
            qpi = pp.propagate()
            fluor = Fluorescence(phantom=ph,
                                 grid_size=self.grid_size,
                                 pixel_size=self.pixel_size,
                                 displacement=displacements[ii]).project()

            if write:
                with h5py.File(path, "a") as h5:
                    qps = qpimage.QPSeries(h5file=h5.require_group("qpseries"))
                    qps.add_qpimage(qpi)

                    h5fl = h5.require_group("flseries")
                    h5fl.create_dataset("fl_{}".format(ii),
                                        data=fluor,
                                        fletcher32=True,
                                        compression="gzip")
            else:
                sino_fields[ii] = qpi.field
                sino_fluor[ii] = fluor

            if count is not None:
                count.value += 1

        if write:
            return path
        else:
            return sino_fields, sino_fluor
