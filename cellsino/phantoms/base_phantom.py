import numpy as np


class BasePhantom(object):
    def __init__(self, medium_index):
        self.elements = []
        self.medium_index = medium_index

    def __iter__(self):
        for el in self.elements:
            yield el

    def append(self, element):
        self.elements.append(element)

    def draw(self, grid_size, pixel_size):
        ri = np.ones(grid_size, dtype=float) * self.medium_index
        fl = np.zeros(grid_size, dtype=float)

        for el in self:
            riel, flel = el.draw(grid_size, pixel_size)
            ri += riel - el.medium_index
            fl += flel
        return ri, fl

    def transform(self, x=0, y=0, z=0, rot_main=0, rot_in_plane=0,
                  rot_perp_plane=0):
        ph = BasePhantom(medium_index=self.medium_index)
        for el in self:
            ph.append(el.transform(x=x,
                                   y=y,
                                   z=z,
                                   rot_main=rot_main,
                                   rot_in_plane=rot_in_plane,
                                   rot_perp_plane=rot_perp_plane))
        return ph
