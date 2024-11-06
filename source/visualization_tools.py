#---------------------------
# Tools for visualization
# PabloVD
# Started: 11/5/20
#---------------------------

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image
#from mayavi import mlab
import os
from source.cities import *
from source.maps import *
import matplotlib as mpl
import matplotlib.cm as cm

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

cmap_default = modified_gist_earth()

# Convert an array to a RGBA array with a given cmap
def array2cmap(x,cmap_name=None):
    norm = mpl.colors.Normalize(vmin=0., vmax=1.)
    if cmap_name==None:
        cmap = modified_gist_earth()
    else:
        cmap = cm.get_cmap(cmap_name)
    m = cm.ScalarMappable(norm=norm, cmap=cmap)
    return m.to_rgba(x)

# Creates a random map
def single_map(kind_noise,boxsize,llavor,params,sigma,threshold,cities=1,make_island=0,cmap=cmap_default):

    figsize = (6.,6.)
    fig, ax = plt.subplots(figsize=figsize)
    margins = {  #     vvv margin in inches
    "left"   :     0.,
    "bottom" :     0.,
    "right"  :  1.,
    "top"    :  1.}
    fig.subplots_adjust(**margins)

    field = generate_map(kind_noise,boxsize,llavor,params,sigma,threshold,make_island=make_island)
    ax.imshow(field,vmin=0.,vmax=1.,cmap=cmap)

    if cities:
        cap_x, cap_y, city_x, city_y = generate_cities(field)
        ax.scatter(city_x, city_y, edgecolor=col_city, facecolor=col_city, alpha=1., s=5.)
        ax.scatter(cap_x, cap_y, edgecolor=col_cap, facecolor=col_cap, alpha=1., s=15.)

    ax.set_axis_off()
    fig.savefig("images/archipielago_noise_{:}_seed_{:}_threshold_{:.1f}_sigma_{:.1f}.png".format(kind_noise,llavor,threshold,sigma))
    plt.close(fig)

# Create (num_plots)x(num_plots) different maps of random islands, with different random seeds
def plot_grid(kind_noise,boxsize,params,sigma,threshold,num_plots=3,cities=1,make_island=0,cmap=cmap_default):

    fig, axes = plt.subplots(num_plots,num_plots, figsize=(9.,9.))
    fig.subplots_adjust(wspace = 0.1, hspace = 0.1)

    llavor = 0

    for axx in axes:
        for ax in axx:

            field = generate_map(kind_noise,boxsize,llavor,params,sigma,threshold,make_island=make_island)
            ax.imshow(field,vmin=0.,vmax=1.,cmap=cmap)

            if cities:
                cap_x, cap_y, city_x, city_y = generate_cities(field)
                ax.scatter(city_x, city_y, edgecolor=col_city, facecolor=col_city, alpha=1., s=5.)
                ax.scatter(cap_x, cap_y, edgecolor=col_cap, facecolor=col_cap, alpha=1., s=15.)

            ax.set_xlim([0,field.shape[0]])
            ax.set_ylim([field.shape[0],0])
            ax.set_axis_off()
            llavor+=1

    plt.axis('off')
    fig.savefig("images/archipielago_grid_noise_{:}_threshold_{:.1f}_sigma_{:.1f}.png".format(kind_noise,threshold,sigma), bbox_inches='tight')
    #plt.close(fig)

# Prints an b/w ascii art version of the map, with a width of specified in chars. Useful for debugging
# Author: Troy Unrau, u/troyunrau reddit user
def plot_ascii(map, term_width=None):

    map = map*255

    if not term_width:
        term_width = (os.get_terminal_size()[0] // 10) * 10 # round to nearest 10
    #ascii_art_chars = [' ', '░', '▒', '▓', '█']
    ascii_art_chars = [' ', '.', '-', 'x', '#']
    len_a = len(ascii_art_chars) - 1
    # see if we were a 1/0 mask
    map_max = np.max(map)
    width, height = map.shape
    map = np.swapaxes(map,0,1) # I don't even know what's x or y anymore

    new_width = term_width // 2
    scale = new_width / width
    new_height = int(height * scale + 0.5) # round to nearest 0.5
    #small_map = scipy.misc.imresize(map, (new_height, new_width*2))    # original line, deprecated
    small_map =np.array(Image.fromarray(map).resize((new_height, new_width*2)))

    if map_max == 1:
        small_map = (small_map>127).astype(int)*len_a # go back to being black or white
    else:
        rescaler = 255 * (len_a / len(ascii_art_chars))
        small_map = (small_map.astype(float)/rescaler*len_a).astype(int)
    chars = np.array(ascii_art_chars, dtype="U1")[small_map]
    strings = chars.view('U' + str(chars.shape[1]))
    strings = strings.flatten()
    print( "\n".join(strings))

# Plot a 3D surface (NEED TO BE IMPROVED)
def plot_surface():
    #field = perlin_field(llavor)#gaussian_field(llavor,indexlaw)#generate_map(llavor,indexlaw,sigma,threshold)
    #field = normalize_field(field)
    #field = smooth_field(field,10.)
    #field = generate_map(llavor,indexlaw,sigma,threshold)
    field = gaussian_field(llavor,indexlaw)
    field = smooth_field(field,10.,gridsize=field.shape[0])
    """for i, row in enumerate(field):
        for j, el in enumerate(row):
            if el<threshold:   field[i,j]=threshold
    lenx, leny = field.shape[0], field.shape[1]
    x, y = np.linspace(0,lenx,num=lenx), np.linspace(0,leny,num=leny)
    X, Y = np.meshgrid(x,y)
    f = interpolate.interp2d(x,y,field,kind="linear")
    sea = np.zeros_like(field)
    sea.fill(threshold)

    fig = plt.figure(figsize=(9,6))
    ax = fig.gca(projection='3d')
    ax.plot_surface(X, Y, sea, cmap=cmap_default,zorder=0.5)
    ax.plot_surface(X, Y, field, cmap=cmap_default, linewidth=0, antialiased=False,zorder=0.8)

    # TRY WITH MAYAVI

    #ax.grid(False)
    #ax.set_xticks([])
    #ax.set_yticks([])
    #ax.set_zticks([])
    plt.axis('off')
    ax.set_zlim(threshold, 1.01)
    #plt.zlim(threshold, 1.01)
    plt.show()"""
    #sea = np.zeros_like(field)
    #sea.fill(threshold)
    #mlab.surf(field,warp_scale="auto")
    #mlab.surf(sea,warp_scale="auto")
    #mlab.show()

# Produce the image of a planet masking the field
def planet(field,seed):

    a,b = field.shape[0]/2, field.shape[1]/2
    n = field.shape[0]*2
    r = field.shape[0]/3
    y,x = np.ogrid[-a:n-a, -b:n-b]
    # creates a mask with True False values
    # at indices
    mask = x**2+y**2 <= r**2

    black = [0, 0, 0]
    island_world = np.zeros_like(field)

    for i in range(field.shape[0]):
        for j in range(field.shape[1]):
            if mask[i][j]:
                island_world[i][j] = field[i][j]
            else:
                island_world[i][j] = -1.

    fig, ax = plt.subplots(1)
    ax.imshow(island_world)
    ax.set_axis_off()
    fig.savefig("images/planet_seed_{}.png".format(seed), bbox_inches='tight')

# Create a planet from a map with matplotlib (not very good)
def mpl_sphere(field):
    img = field

    # define a grid matching the map size, subsample along with pixels
    theta = np.linspace(0, np.pi, img.shape[0])
    phi = np.linspace(0, 2*np.pi, img.shape[1])

    count = 180 # keep 180 points along theta and phi
    theta_inds = np.linspace(0, img.shape[0] - 1, count).round().astype(int)
    phi_inds = np.linspace(0, img.shape[1] - 1, count).round().astype(int)
    theta = theta[theta_inds]
    phi = phi[phi_inds]
    img = img[np.ix_(theta_inds, phi_inds)]

    theta,phi = np.meshgrid(theta, phi)
    R = 1

    # sphere
    x = R * np.sin(theta) * np.cos(phi)
    y = R * np.sin(theta) * np.sin(phi)
    z = R * np.cos(theta)

    colorarray = np.zeros((img.shape[0],img.shape[1],3))
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            colorarray[i,j] = np.array([0,1,1])*img[i,j]


    # create 3d Axes
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x.T, y.T, z.T, facecolors=colorarray, cstride=1, rstride=1) # we've already pruned ourselves

    # make the plot more spherical
    ax.axis('scaled')
    ax.set_axis_off()
    plt.show()

# Planet generation from the spherical projection of a map onto a sphere
# It employs equirectangular_projection https://en.wikipedia.org/wiki/Equirectangular_projection
# Based on http://code.activestate.com/recipes/580695-image-projection-onto-sphere/
def spherical_projection(field,count,cmap=None,xy=None,xz=None,yz=None):
    import math, random
    imgxOutput = 768; imgyOutput = 768
    pi2 = math.pi * 2
    # 3D Sphere Rotation Angles (arbitrary) if not provided
    if xy==None: xy = -pi2 * random.random()
    if xz==None: xz = -pi2 * random.random()
    if yz==None: yz = -pi2 * random.random()
    sxy = math.sin(xy); cxy = math.cos(xy)
    sxz = math.sin(xz); cxz = math.cos(xz)
    syz = math.sin(yz); cyz = math.cos(yz)

    rgbfield = array2cmap(field,cmap_name=cmap)
    imageInput = Image.fromarray((rgbfield*255).astype('uint8'),mode="RGBA")
    #imageInput = Image.open(image_name) if it is from external file
    (imgxInput, imgyInput) = imageInput.size
    pixelsInput = imageInput.load()
    imageOutput = Image.new("RGB", (imgxOutput, imgyOutput))
    pixelsOutput = imageOutput.load()
    # define a sphere behind the screen
    xc = (imgxOutput - 1.0) / 2
    yc = (imgyOutput - 1.0) / 2
    zc = min((imgxOutput - 1.0), (imgyOutput - 1.0)) / 2
    r = min((imgxOutput - 1.0), (imgyOutput - 1.0)) / 2
    # define eye point
    xo = (imgxOutput - 1.0) / 2
    yo = (imgyOutput - 1.0) / 2
    zo = -min((imgxOutput - 1.0), (imgyOutput - 1.0))
    xoc = xo - xc
    yoc = yo - yc
    zoc = zo - zc
    doc2 = xoc * xoc + yoc * yoc + zoc * zoc
    for yi in range(imgyOutput):
        for xi in range(imgxOutput):
            xio = xi - xo
            yio = yi - yo
            zio = 0.0 - zo
            dio = math.sqrt(xio * xio + yio * yio + zio * zio)
            xl = xio / dio
            yl = yio / dio
            zl = zio / dio
            dot = xl * xoc + yl * yoc + zl * zoc
            val = dot * dot - doc2 + r * r
            if val >= 0: # if there is line-sphere intersection
                if val == 0: # 1 intersection point
                    d = -dot
                else: # 2 intersection points => choose the closest
                    d = min(-dot + math.sqrt(val), -dot - math.sqrt(val))
                    xd = xo + xl * d
                    yd = yo + yl * d
                    zd = zo + zl * d
                    x = (xd - xc) / r
                    y = (yd - yc) / r
                    z = (zd - zc) / r
                    x0=x*cxy-y*sxy;y=x*sxy+y*cxy;x=x0 # xy-plane rotation
                    x0=x*cxz-z*sxz;z=x*sxz+z*cxz;x=x0 # xz-plane rotation
                    y0=y*cyz-z*syz;z=y*syz+z*cyz;y=y0 # yz-plane rotation
                    lng = (math.atan2(y, x) + pi2) % pi2
                    lat = math.acos(z)
                    ix = int((imgxInput - 1) * lng / pi2 + 0.5)
                    iy = int((imgyInput - 1) * lat / math.pi + 0.5)
                    try:
                        pixelsOutput[xi, yi] = pixelsInput[ix, iy]
                    except:
                        pass
    img = np.array(imageOutput)
    #plt.imshow(img)
    #plt.show()
    imageOutput.save("images/World_%d.png"%count, "PNG")

# Choose the color map
#cmap_default = modified_gist_earth()
# List of color maps suitable for planets
cmaps_planets = ["viridis", "cividis", "inferno", "twilight", "ocean", "bone", "afmhot", "pink"]
# Color for the capitals
col_cap = "darkred"
# Color for the cities
col_city = "crimson"
