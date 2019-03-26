import flimage
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

    def compute(self, angles, axis_roll=0, displacements=None,
                times=3.0, mode=["field", "fluorescence"], propagator="rytov",
                bleach_decay=0, fluorescence_background=0, path=None,
                count=None, max_count=None):
        """Compute sinogram data

        Parameters
        ----------
        angles: 1d array of size N or int
            If an array, defines the angular positions for each frame
            of the rotation. If an int, defines the number of angles
            of a steady rotation from 0 to 2π.
        axis_roll: float
            In-plane rotation of the rotational axis [rad]
        displacements: 2d ndarray of shape (N, 2) or float
            A float value indicates the standard deviation of a
            Gaussian noise distribution (using
            :func:`numpy.random.normal`) in pixels.
            A 2d array directly specifies the x-y-displacement for each
            frame in pixels.
        times: 1d ndarray of size N or float
            If an array, sets the measurement time of each frame
            of the rotation. If a float, defines the measurement duration.
        mode: list of str
            The imaging modalities to simulate. Valid strings are
            "field" (quantitative phase imaging) and "fluorescence".
        propagator: str
            The propagator to use for field computation. Must be in
            :data:`cellsino.propagators.available`.
        bleach_decay: float
            Photobleaching decay constant [1/s]
        fluorescence_background: float
            Overall fluorescence background signal
        path: str or pathlib.Path
            If not None, the data will be written to this file and
            a :class:`pathlib.Path` object will be returned.
        count: multiprocessing.Value
            May be used for tracking progress. At each computed
            angle `count.value` is incremented by one.
        max_count: multiprocessing.Value
            May be used for tracking progress. This value is
            incremented by `N`.

        Returns
        -------
        sinogram_fields, sinogram_fluorescence: 3d np.ndarray
            Both sinograms are returned if `mode` is set to its
            default value, otherwise, only one sinogram is returned.
            If `path` is set, then the path is returned (no sinogram
            data are written into memory).
        """
        for mm in mode:
            if mm not in ["field", "fluorescence"]:
                raise ValueError("Invalid element in `mode`: `{}`".format(mm))
        if len(mode) == 0:
            raise ValueError("No `mode` specified!")
        do_qps = "field" in mode
        do_fls = "fluorescence" in mode

        if max_count is not None:
            max_count.value += angles.size

        if isinstance(angles, int):
            angles = np.linspace(0, 2*np.pi, angles, endpoint=False)

        if isinstance(times, (int, float)):
            times = np.linspace(0, times, angles.shape[0], endpoint=False)

        if displacements is None:
            displacements = np.zeros((angles.shape[0], 2))
        elif isinstance(displacements, float):
            np.random.seed(47)  # for reproducibility
            displacements = np.random.normal(scale=displacements,
                                             size=(angles.shape[0], 2))

        if path:
            write = True
        else:
            write = False
            if do_qps:
                sino_field = np.zeros((angles.size,
                                       self.grid_size[0],
                                       self.grid_size[1]),
                                      dtype=complex)
            if do_fls:
                sino_fluor = np.zeros((angles.size,
                                       self.grid_size[0],
                                       self.grid_size[1]),
                                      dtype=float)

        for ii, ang in enumerate(angles):
            ph = self.phantom.transform(rot_main=ang, rot_in_plane=axis_roll)
            if do_qps:  # QPI
                pp = prop_dict[propagator](phantom=ph,
                                           grid_size=self.grid_size,
                                           pixel_size=self.pixel_size,
                                           wavelength=self.wavelength,
                                           displacement=displacements[ii])
                qpi = pp.propagate()
                qpi["time"] = times[ii]
            if do_fls:  # Fluorescence
                bleach_factor = np.exp(-bleach_decay*times[ii])
                fli = Fluorescence(phantom=ph,
                                   grid_size=self.grid_size,
                                   pixel_size=self.pixel_size,
                                   displacement=displacements[ii],
                                   bleach_factor=bleach_factor,
                                   background=fluorescence_background,
                                   ).project()
                fli["time"] = times[ii]

            if write:
                with h5py.File(path, "a") as h5:
                    if do_qps:
                        qps = qpimage.QPSeries(
                            h5file=h5.require_group("qpseries"))
                        qps.add_qpimage(qpi)
                    if do_fls:
                        fls = flimage.FLSeries(
                            h5file=h5.require_group("flseries"))
                        fls.add_flimage(fli)
            else:
                if do_qps:
                    sino_field[ii] = qpi.field
                if do_fls:
                    sino_fluor[ii] = fli.fl

            if count is not None:
                count.value += 1

        if write:
            return path
        else:
            if do_qps and do_fls:
                return sino_field, sino_fluor
            elif do_qps:
                return sino_field
            else:
                return sino_fluor
