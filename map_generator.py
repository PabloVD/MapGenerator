#---------------------------
# Map Generator
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

# TO DO
# try with different noises: opensimplex, fractional brownian noise...
# plot planet with spherical projection

from source.visualization_tools import *

#--- Parameters ---#

# Number of bins per dimension
boxsize = 500
# Number of bins per dimension in the smoothed high resolution box
highboxsize = boxsize
# Threshold for the sea level
threshold = 0.6
# Sigma for the gaussian smoothing
sigma = 5.
# Initial random seed
llavor = 0
# Amplitude of power spectrum
amp = 1.
# Spectral index for the power spectrum (only for Gauss noise)
indexlaw = -3.
# Hurst index for Fractional Brownian Field
hurst = 0.5
# Choose kind of noise. See the source/field.py module for the options
kind_noise = "gauss"
# Ensure that the boundaries are sea if 1
make_island = 0

#--- Perlin parameters ---#
# Scale sets the size of the objects
# Set to e.g. 500 to bigger portions of land
scale = 500
# Octaves is the number of levels, and increases the granularity with higher values
# Lower values give less defined boundaries
octaves = 6
# Persistence determines how much each octave contributes to the overall shape (adjusts amplitude)
# Lower than 1 means that sucessive octaves contribute less
# Set to close to 1 to have more islands and less big structures
persistence = 0.5
# Lacunarity determines how much detail is added or removed at each octave (adjusts frequency)
# More than 1 means that each octave will increase it’s level of fine grained detail (increased frequency)
# For the octave i, the frecuency is lacunarity**i, and the amplitude is persistence**i
lacunarity = 2.0

if kind_noise == "gauss":
    params = [amp, indexlaw]
elif kind_noise == "fbm":
    params = hurst
else:
    params = [scale,octaves,persistence,lacunarity,boxsize]
    # params = {"scale":scale, "octaves":octaves, "persistence":persistence, "lacunarity":lacunarity}


for llavor in range(10):
    fig = single_map(kind_noise,boxsize,llavor,params,sigma,threshold)
    fig.savefig("images/map_noise_{:}_seed_{:}_threshold_{:.1f}_sigma_{:.1f}.png".format(kind_noise,llavor,threshold,sigma))
    plt.close(fig)

plot_grid(kind_noise,boxsize,params,sigma,threshold,num_plots=3,make_island=0,cmap=modified_gist_earth())