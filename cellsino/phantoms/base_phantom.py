class BasePhantom(object):
    def __init__(self):
        self.elements = []

    def __iter__(self):
        for el in self.elements:
            yield el

    def append(self, element):
        self.elements.append(element)

    def transform(self, x=0, y=0, z=0, rot_main=0, rot_in_plane=0,
                  rot_perp_plane=0):
        ph = BasePhantom()
        for el in self:
            ph.append(el.transform(x=x,
                                   y=y,
                                   z=z,
                                   rot_main=rot_main,
                                   rot_in_plane=rot_in_plane,
                                   rot_perp_plane=rot_perp_plane))
        return ph
