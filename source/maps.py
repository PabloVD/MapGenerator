#---------------------------
# Field generator module
# PabloVD
# Started: 11/5/20
#---------------------------

from scipy import interpolate, ndimage
from source.fields import *

# Filter the field with a gaussian window
def smooth_field(field,sigmagauss,gridsize=None):

    if gridsize==None: gridsize=field.shape[0]

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

# A gaussian function
def central_gaussian(x,y,x_c,y_c,sig):
    return np.exp(-((x-x_c)**2.+(y-y_c)**2.)/2./sig**2.)

# Multiply the field by a gaussian mask to ensure an island in the center of the image
def masked_field(field,sig=None):
    a, b = field.shape[0], field.shape[1]
    if sig==None: sig = a/2.
    x, y = np.linspace(0,a-1,num=a), np.linspace(0,b-1,num=b)
    X, Y = np.meshgrid(x,y)
    mask = central_gaussian(X,Y,a/2,b/2,sig)
    field = field*mask
    return field

# Generate a map of islands applying different processes:
# 1. Generate a random field, either gaussian or perlin
# 2. Normalize the field between 0 and 1
# 3. Smooth the field with a gaussian filter
# 4. Retain only the mainland above a certain threshold
def generate_map(kind_noise,boxsize,llavor,params,sigma,threshold,boxsizey=None,make_island=0):

    if boxsizey==None: boxsizey=boxsize
    np.random.seed(seed=llavor)

    if kind_noise=="gauss":
        amp, indexlaw = params
        field = gaussian_field(boxsize,llavor,indexlaw,amp)
    elif kind_noise=="perlin":
        scale,octaves,persistence,lacunarity,boxsizey = params
        field = perlin_field(boxsize,llavor,scale,octaves,persistence,lacunarity,boxsizey=boxsizey)
        #field = perlin_field(boxsize,llavor,*params)
    elif kind_noise=="warped_perlin":
        scale,octaves,persistence,lacunarity,boxsizey = params
        field = warped_perlin_field(boxsize,llavor,scale,octaves,persistence,lacunarity,boxsizey=boxsizey)
    elif kind_noise=="fbm":
        hurst = params
        field = brownian_surface(boxsize, H=hurst)
    elif kind_noise=="cos":
        scale,octaves,persistence,lacunarity,boxsizey = params
        field = cos_field(boxsize,llavor,scale,octaves,persistence,lacunarity,boxsizey=boxsizey)
    else:
        print("Kind of noise not valid.")
        return np.zeros((boxsize,boxsizey))

    field = normalize_field(field)
    if make_island:
        field = masked_field(field)
    field = smooth_field(field,sigma,gridsize=2*boxsize)
    field = mainland(field,threshold)
    
    return field
