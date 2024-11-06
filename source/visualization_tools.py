#---------------------------
# Tools for visualization
# PabloVD
# Started: 11/5/20
#---------------------------

import matplotlib.pyplot as plt
from source.maps import *

# Modify gist_earth color map to have a dark blue as the minimum value, instead of black
def modified_gist_earth():

    cmap = plt.get_cmap("gist_earth")
    # Color maps defined for 256 values
    num = 256
    # Location of the color I want to be the lowest value
    ind_blue = 5   #

    blue_list = []
    for i in range(ind_blue):
        blue_list.append(cmap(ind_blue))

    newcmap = cmap.from_list('modified_gist_earth',blue_list+list(map(cmap,range(ind_blue,num))), N=num)
    return newcmap

# Creates a random map
def single_map(kind_noise,boxsize,llavor,params,sigma,threshold,make_island=0,cmap=modified_gist_earth(),axissize=6):

    figsize = (axissize,axissize)
    fig, ax = plt.subplots(figsize=figsize)
    margins = {  #     vvv margin in inches
    "left"   :     0.,
    "bottom" :     0.,
    "right"  :  1.,
    "top"    :  1.}
    fig.subplots_adjust(**margins)

    field = generate_map(kind_noise,boxsize,llavor,params,sigma,threshold,make_island=make_island)
    ax.imshow(field,vmin=0.,vmax=1.,cmap=cmap)

    ax.set_axis_off()

    return fig
    

# Create (num_plots)x(num_plots) different maps of random islands, with different random seeds
def plot_grid(kind_noise,boxsize,params,sigma,threshold,num_plots=3,make_island=0,cmap=modified_gist_earth()):

    fig, axes = plt.subplots(num_plots,num_plots, figsize=(9.,9.))
    fig.subplots_adjust(wspace = 0.1, hspace = 0.1)

    llavor = 0

    for axx in axes:
        for ax in axx:

            field = generate_map(kind_noise,boxsize,llavor,params,sigma,threshold,make_island=make_island)
            ax.imshow(field,vmin=0.,vmax=1.,cmap=cmap)

            ax.set_xlim([0,field.shape[0]])
            ax.set_ylim([field.shape[0],0])
            ax.set_axis_off()
            llavor+=1

    plt.axis('off')
    fig.savefig("images/gridmap_noise_{:}_threshold_{:.1f}_sigma_{:.1f}.png".format(kind_noise,threshold,sigma), bbox_inches='tight')
    #plt.close(fig)

