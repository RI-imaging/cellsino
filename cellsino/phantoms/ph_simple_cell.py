from .base_phantom import BasePhantom
from ..elements import Sphere


class SimpleCell(BasePhantom):
    def __init__(self,
                 cytoplasm_index=1.365,
                 nucleus_index=1.360,
                 nucleoli_index=1.387,
                 medium_index=1.335,
                 cytoplasm_fl=0,
                 nucleus_fl=3,
                 nucleus_shell_fl=10,
                 nucleoli_fl=0):
        """Simple cell phantom with cytoplasm, nucleus, and 2 nucleoli

        Configuration:
        - cytoplasm_index sphere (no fl) containing
          - nucleus sphere (shell fluorescence) containing
            - 2 small nucleoli (full fluorescence)
        """
        nleoi1 = Sphere(radius=1.5e-6,
                        center=(-.25e-6, 2e-6, 2e-6),
                        fl_brightness=nucleoli_fl-nucleus_fl,
                        object_index=medium_index +
                        (nucleoli_index-nucleus_index),
                        medium_index=medium_index,
                        )

        nleoi2 = Sphere(radius=1.5e-6,
                        center=(+.25e-6, -1e-6, 2e-6),
                        fl_brightness=nucleoli_fl-nucleus_fl,
                        object_index=medium_index +
                        (nucleoli_index-nucleus_index),
                        medium_index=medium_index,
                        )

        nuclus = Sphere(radius=4e-6,
                        center=(0e-6, 1e-6, 1e-6),
                        fl_brightness=nucleus_shell_fl,
                        object_index=medium_index +
                        (nucleus_index-cytoplasm_index),
                        medium_index=medium_index,
                        )

        nuclus_shell = Sphere(radius=3.8e-6,
                              center=(0e-6, 1e-6, 1e-6),
                              fl_brightness=nucleus_fl-nucleus_shell_fl,
                              object_index=medium_index,
                              medium_index=medium_index,
                              )

        cyto = Sphere(radius=5.5e-6,
                      center=(0, 0, 0),
                      fl_brightness=cytoplasm_fl,
                      object_index=cytoplasm_index,
                      medium_index=medium_index,
                      )
        self.elements = [nleoi1, nleoi2, nuclus, nuclus_shell, cyto]
        self.medium_index = medium_index
