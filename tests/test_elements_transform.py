import numpy as np

from cellsino.elements.base_element import BaseElement


def test_translation():
    points = np.array([[0, 0, 0]])
    el = BaseElement(object_index=1.36,
                     medium_index=1.335,
                     fl_brightness=0,
                     points=points)

    el2 = el.transform(x=1, y=2, z=-3)
    assert np.all(el2.points[0] == [1, 2, -3])


if __name__ == "__main__":
    # Run all tests
    loc = locals()
    for key in list(loc.keys()):
        if key.startswith("test_") and hasattr(loc[key], "__call__"):
            loc[key]()
