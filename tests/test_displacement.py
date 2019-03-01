import numpy as np

from cellsino import sinogram


def test_displacement():
    kw = {"phantom": "simple cell",
          "wavelength": 550e-9,
          "pixel_size": 0.7e-6,
          "grid_size": (25, 25),
          }
    sino = sinogram.Sinogram(**kw)

    angles = np.array([0, .5, .6])
    field1, fluor1 = sino.compute(angles=angles,
                                  propagator="projection")
    field2, fluor2 = sino.compute(angles=angles,
                                  displacements=np.ones((3, 2)),
                                  propagator="projection")
    field3 = np.roll(field1, (1, 1), axis=(1, 2))
    fluor3 = np.roll(fluor1, (1, 1), axis=(1, 2))

    assert np.allclose(field2, field3, rtol=0, atol=1e-13)
    assert np.allclose(fluor2, fluor3, rtol=0, atol=1e-13)
    assert not np.allclose(field2, field1, rtol=0, atol=1e-13)
    assert not np.allclose(fluor2, fluor1, rtol=0, atol=1e-13)


if __name__ == "__main__":
    # Run all tests
    loc = locals()
    for key in list(loc.keys()):
        if key.startswith("test_") and hasattr(loc[key], "__call__"):
            loc[key]()
