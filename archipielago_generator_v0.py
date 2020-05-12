#---------------------------
# Archipielago Generator
# PabloVD
# Started: 11/5/20
#---------------------------

"""
---------------------------------------------------------------------------------
Generate maps of random islands from a gaussian field.
After being normalized and smoothed,
only the mainland above a certain threshold is retained,
being the rest considered as sea.
The gaussian field is generated employing a cosmological package, powerbox,
from a power spectrum as input.
---------------------------------------------------------------------------------
"""

import matplotlib.pyplot as plt
import numpy as np
import powerbox as pbox
from scipy import interpolate, ndimage

#--- Parameters ---#

# Number of bins per dimension
boxsize = 500
# Number of bins per dimension in the high resolution  box
highboxsize = 2*boxsize
# Threshold for the sea level
threshold = 0.6
# Sigma for the gaussian smoothing
sigma = 5.
# Initial random seed
llavor = 0
# Spectral index for the power spectrum
indexlaw = -3.

# Define power spectrum as a power law with an spectral index indexlaw
# With lower the spectral indexes, small structures are removed
def powerspec(k,indexlaw):
    return k**indexlaw

# Filter the field with a gaussian window
def smooth_field(field,sigmagauss,gridsize=boxsize):

    x, y = np.linspace(0,field.shape[0],num=field.shape[0]), np.linspace(0,field.shape[1],num=field.shape[1])

    # Interpolation
    f = interpolate.interp2d(x,y,field,kind="linear")

    qx = np.linspace(x[0],x[-1], num = gridsize)
    qy = np.linspace(y[0],y[-1], num = gridsize)

    # Filtering
    smooth = ndimage.filters.gaussian_filter(f(qx,qy),sigmagauss)
    return smooth

# Remove regions below sea level
def mainland(field,threshold):
    for i, row in enumerate(field):
        for j, el in enumerate(row):
            if el<threshold:   field[i,j]=0.
    return field

# Normalize the values of the field between 0 and 1
def normalize_field(field):
    min, max = np.amin(field), np.amax(field)
    newfield = (field-min)/(max-min)
    return newfield

# Generate a map of islands applying different processes:
# 1. Generate a random gaussian field given a power spectrum
# 2. Normalize the field between 0 and 1
# 3. Smooth the field with a gaussian filter
# 4. Retain only the mainland above a certain threshold
def generate_map(llavor,indexlaw,sigma,threshold):
    np.random.seed(seed=llavor)
    field = pbox.powerbox.PowerBox(boxsize, lambda k: powerspec(k,indexlaw), dim=2, boxlength=100.).delta_x()
    field = normalize_field(field)
    field = smooth_field(field,sigma,gridsize=highboxsize)
    field = mainland(field,threshold)
    return field

#--- MAIN ---#

# Create 9 different maps of random islands, with different random seeds
fig, axes = plt.subplots(3,3, figsize=(9.,9.))
fig.subplots_adjust(wspace = 0.1, hspace = 0.1)

for axx in axes:
    for ax in axx:
        field = generate_map(llavor,indexlaw,sigma,threshold)
        city_x, city_y = generate_cities(field)

        ax.imshow(field,vmin=0.,vmax=1.)
        ax.scatter(city_x, city_y, edgecolor=colcity, facecolor=colcity, alpha=1., s=5.)
        ax.set_xlim([0,highboxsize])
        ax.set_ylim([highboxsize,0])
        ax.set_axis_off()
        llavor+=1

plt.axis('off')
plt.savefig("images/archipielago_9seeds_indexlaw_{:+.1f}_threshold_{:.1f}_sigma_{:.1f}.png".format(indexlaw,threshold,sigma), bbox_inches='tight')
plt.show()
