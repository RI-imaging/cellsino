"""Reconstruction of a simple cell phantom

This example uses :ref:`ODTbrain<odtbrain:index>` and
:ref:`radontea<radontea:index>` for the reconstruction of the refractive
index and the fluorescence sinogram of the simple cell phantom.
The reconstruction is compared to the ground truth of the cell phantom.
"""
import cellsino
import matplotlib.pylab as plt
import numpy as np
import odtbrain as odt
import radontea as rt


# number of sinogram angles
num_ang = 160
# sinogram acquisition angles
angles = np.linspace(0, 2*np.pi, num_ang, endpoint=False)
# detector grid size
grid_size = (250, 250)
# vacuum wavelength [m]
wavelength = 550e-9
# pixel size [m]
pixel_size = 0.08e-6
# refractive index of the surrounding medium
medium_index = 1.335

# initialize cell phantom
phantom = cellsino.phantoms.SimpleCell()

# initialize sinogram with geometric parameters
sino = cellsino.Sinogram(phantom=phantom,
                         wavelength=wavelength,
                         pixel_size=pixel_size,
                         grid_size=grid_size)

# compute sinogram (field according to Rytov approximation and fluorescence)
sino_field, sino_fluor = sino.compute(angles=angles, propagator="rytov")

# reconstruction of refractive index
sino_rytov = odt.sinogram_as_rytov(sino_field)
potential = odt.backpropagate_3d(uSin=sino_rytov,
                                 angles=angles,
                                 res=wavelength/pixel_size,
                                 nm=medium_index)
ri = odt.odt_to_ri(f=potential,
                   res=wavelength/pixel_size,
                   nm=medium_index)

# reconstruction of fluorescence
fl = rt.backproject_3d(sinogram=sino_fluor,
                       angles=angles)

# reference for comparison
rimod, flmod = phantom.draw(grid_size=ri.shape,
                            pixel_size=pixel_size)

# plotting
idx = 150

plt.figure(figsize=(7, 5.5))

plotkwri = {"vmax": ri.real.max(),
            "vmin": ri.real.min(),
            "interpolation": "none",
            "cmap": "viridis",
            }

plotkwfl = {"vmax": fl.max(),
            "vmin": 0,
            "interpolation": "none",
            "cmap": "Greens_r",
            }

ax1 = plt.subplot(221, title="refractive index (ground truth)")
mapper = ax1.imshow(rimod[idx].real, **plotkwri)
plt.colorbar(mappable=mapper, ax=ax1)

ax2 = plt.subplot(222, title="refractive index (reconstruction)")
mapper = ax2.imshow(ri[idx].real, **plotkwri)
plt.colorbar(mappable=mapper, ax=ax2)

ax3 = plt.subplot(223, title="fluorescence (ground truth)")
mapper = ax3.imshow(flmod[idx], **plotkwfl)
plt.colorbar(mappable=mapper, ax=ax3)

ax4 = plt.subplot(224, title="fluorescence (reconstruction)")
mapper = ax4.imshow(fl[idx], **plotkwfl)
plt.colorbar(mappable=mapper, ax=ax4)

for ax in [ax1, ax2, ax3, ax4]:
    ax.grid(color="w", alpha=.5)
    ax.set_xticks(np.arange(0, grid_size[0], 50))
    ax.set_yticks(np.arange(0, grid_size[0], 50))
    ax.set_xticklabels([])
    ax.set_yticklabels([])

plt.tight_layout()

plt.show()
