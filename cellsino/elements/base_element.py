import copy

import numpy as np


class BaseElement(object):
    def __init__(self, object_index, medium_index, fl_brightness,
                 points):
        """Initialize a basic element

        Parameters
        ----------
        object_index: float
            Refractive index of the element
        medium_index: float
            Refractive index of surrounding medium
        fl_brightness: float
            Fluorescence brightness
        points: 2d ndarray
            Coordinates of the element [m]

        Notes
        -----
        When subclassing this class, override this method with
        additional parameters (e.g. position, size) and call it
        with super(ClassName, self).__init__(...).
        """
        #: refractive index of the object
        self.object_index = object_index
        #: refractive index of the medium
        self.medium_index = medium_index
        #: brightness of the fluorescence signal
        self.fl_brightness = fl_brightness
        #: 2D array of points describing the geometrical object. This
        #: variable is used for affine transforms (e.g. when rotating
        #: the object).
        self.points = np.array(points)

    def draw(self, grid_size, pixel_size):
        ri = np.ones(grid_size, dtype=float) * self.medium_index
        fl = np.zeros(grid_size, dtype=float)
        for pp in self.points:
            # ODTbrain convention
            cy, cz, cx = np.array(pp/pixel_size, dtype=int)
            ri[cx, cy, cz] = self.object_index
            fl[cx, cy, cz] = self.fl_brightness
        return ri, fl

    def transform(self, x=0, y=0, z=0, rot_main=0, rot_in_plane=0,
                  rot_perp_plane=0):
        """Rotate and translate self.points

        Notes
        -----
        - By convention, sinogram generation in cellsino is performed by
          modifying the pitch (rotation about y-axis).
        - Rotation is performed prior to translation. First, the points
          are rotated about the y-axis (``rot_main``, the main sinogram
          acquisition angle). Second, the points are rotated about the
          x-axis (``rot_perp_plane``, perpendicular to the imaging plane).
          Third, the points are rotated about the z-axis (``rot_in_plane``,
          within the imaging plane).
        """
        # The definition of the angles are such that the sinogram
        # can be plugged right into ODTbrain/radontea without
        # transposing it (when only `rot_main` is set).
        alpha = -rot_main
        beta = rot_perp_plane
        gamma = rot_in_plane
        Rx = np.array([
                      [1,             0,              0],
                      [0, np.cos(alpha), -np.sin(alpha)],
                      [0, np.sin(alpha),  np.cos(alpha)],
                      ])

        Ry = np.array([
                      [np.cos(beta),  0, np.sin(beta)],
                      [0,             1,            0],
                      [-np.sin(beta), 0, np.cos(beta)],
                      ])

        Rz = np.array([
                      [np.cos(gamma), -np.sin(gamma), 0],
                      [np.sin(gamma),  np.cos(gamma), 0],
                      [0,          0,                 1],
                      ])

        R = np.dot(np.dot(Ry, Rz), Rx)
        rotated = np.dot(R, self.points.T).T
        rotated_pad = np.pad(rotated, ((0, 0), (0, 1)), mode="constant",
                             constant_values=1)

        T = np.array([[1, 0, 0, x],
                      [0, 1, 0, y],
                      [0, 0, 1, z],
                      [0, 0, 0, 1],
                      ])
        translated = np.dot(T, rotated_pad.T)[:-1].T

        # return a copy of the current instance with points transformed
        telement = copy.copy(self)
        telement.points = translated
        return telement
