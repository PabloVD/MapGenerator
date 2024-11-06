#---------------------------
# Field generator module
# PabloVD
# Started: 11/5/20
#---------------------------

"""
Collection of noise fields for generating maps.
Noises included are:
"gauss": Random gaussian field, with a given power spectrum, computed using the package powerbox
"perlin": Perlin noise, computed using the package noise
"warped_perlin": Perlin noise with domain warping, computed using the package noise
"cos": Sinusoidal noise (to be improved)
"fbm": Fractional Brownian Field
"""

import numpy as np
import powerbox as pbox
import noise

# Define power spectrum as a power law with an spectral index indexlaw
# With lower the spectral indexes (redder noise), small structures are removed
def powerspec(k,indexlaw=-3.):
    return k**indexlaw

# Generate a Gaussian field with a power law power spectrum
def gaussian_field(boxsize,seed,indexlaw=-3.):
    field = pbox.PowerBox(boxsize, lambda k: powerspec(k,indexlaw), dim=2, boxlength=1.,seed=seed).delta_x()
    return field

# Generate a Perlin field
def perlin_field(boxsizex,seed,scale,octaves,persistence,lacunarity,boxsizey=None):

    if boxsizey==None: boxsizey=boxsizex
    shape = (boxsizex,boxsizey)

    field = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            field[i,j] = noise.pnoise2(i/scale,
                                        j/scale,
                                        octaves=octaves,
                                        persistence=persistence,
                                        lacunarity=lacunarity,
                                        #repeatx=1024,
                                        #repeaty=1024,
                                        base=seed)
    return field

# 2D cosinus (see Hill noise for something similar but better https://blog.bruce-hill.com/hill-noise)
def cos_noise(X,Y,Amp,frecx,frecy,phase):
    return Amp*np.cos( frecx*X +frecy*Y + phase)
    #return Amp*(np.cos( frecx*X) +np.cos(frecy*Y + phase))

# Generate a noise using superposition of cosinus
def cos_field(boxsizex,seed,scale,octaves,persistence,lacunarity,boxsizey=None):

    if boxsizey==None: boxsizey=boxsizex
    np.random.seed(seed=seed)

    frec0 = 5.

    x, y = np.linspace(0,boxsizex,num=boxsizex), np.linspace(0,boxsizey,num=boxsizey)
    X, Y = np.meshgrid(x,y)

    noise_tot = np.zeros((boxsizex,boxsizey))

    for oct in range(octaves):
        Amp, frecx, frecy, phase = np.random.random(), 2.*np.pi*frec0*random.uniform(-1.,1.), 2.*np.pi*frec0*random.uniform(-1.,1.), 2.*np.pi*np.random.random()
        noise_tot += persistence**oct*cos_noise(X/scale,Y/scale,Amp,frecx*lacunarity**oct,frecy*lacunarity**oct,phase)

    return noise_tot

# Generate a Perlin field with warping domain (see e.g. https://iquilezles.org/www/articles/warp/warp.htm)
def warped_perlin_field(boxsizex,seed,scale,octaves,persistence,lacunarity,amplitude=None,boxsizey=None):

    if boxsizey==None: boxsizey=boxsizex
    shape = (boxsizex,boxsizey)

    if amplitude==None: amplitude = np.random.uniform(0.,30.)

    field = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            vec = np.random.rand(2)
            ii = noise.pnoise2(i/scale,j/scale,octaves=octaves,persistence=persistence,lacunarity=lacunarity,base=seed)
            jj = noise.pnoise2(i/scale,j/scale,octaves=octaves,persistence=persistence,lacunarity=lacunarity,base=seed)
            field[i,j] = noise.pnoise2(i/scale + amplitude*ii,j/scale + amplitude*jj,octaves=octaves,persistence=persistence,lacunarity=lacunarity,base=seed)
    return field

# Embedding of covariance function on a [0,R]^2 grid for fractional Brownian field
# From https://gist.github.com/radarsat1/6f8b9b50d1ecd2546d8a765e8a144631
def rho(x,y,R,alpha):

    if alpha <= 1.5:
        # alpha=2*H, where H is the Hurst parameter
        beta = 0
        c2 = alpha/2
        c0 = 1-alpha/2
    else:
        # parameters ensure piecewise function twice differentiable
        beta = alpha*(2-alpha)/(3*R*(R**2-1))
        c2 = (alpha-beta*(R-1)**2*(R+2))/2
        c0 = beta*(R-1)**3+1-c2

    # create continuous isotropic function
    r = np.sqrt((x[0]-y[0])**2+(x[1]-y[1])**2)
    if r<=1:
        out=c0-r**alpha+c2*r**2
    elif r<=R:
        out=beta*(R-r)**3/r
    else:
        out=0

    return out, c0, c2

# Fractional Brownian surface
# The main control is the Hurst parameter: H should be between 0 and 1, where 0 is very noisy, and 1 is smoother.
# From https://gist.github.com/radarsat1/6f8b9b50d1ecd2546d8a765e8a144631
def brownian_surface(boxsizex, H=0.8):
    N = 2*boxsizex
    R = 2  # [0,R]^2 grid, may have to extract only [0,R/2]^2

    # size of grid is m*n; covariance matrix is m^2*n^2
    M = N

    # create grid for field
    tx = np.linspace(0, R, M)
    ty = np.linspace(0, R, N)
    rows = np.zeros((M,N))


    for i in range(N):
        for j in range(M):
            # rows of blocks of cov matrix
            rows[j,i] = rho([tx[i],ty[j]],
                            [tx[0],ty[0]],
                            R, 2*H)[0]

    BlkCirc_row = np.vstack(
        [np.hstack([rows, rows[:,-1:1:-1]]),
         np.hstack([rows[-1:1:-1,:], rows[-1:1:-1, -1:1:-1]])])

    # compute eigen-values
    lam = np.real(np.fft.fft2(BlkCirc_row))/(4*(M-1)*(N-1))
    lam = np.sqrt(lam)

    # generate field with covariance given by block circular matrix
    Z = np.vectorize(complex)(np.random.randn(2*(M-1), 2*(M-1)),
                              np.random.randn(2*(M-1), 2*(M-1)))
    F = np.fft.fft2(lam*Z)
    F = F[:M, :N] # extract sub-block with desired covariance

    out,c0,c2 = rho([0,0],[0,0],R,2*H)

    field1 = np.real(F) # two independent fields
    #field2 = np.imag(F)
    #field1 = field1 - field1[0,0] # set field zero at origin
    #field2 = field2 - field2[0,0] # set field zero at origin

    # make correction for embedding with a term c2*r^2
    field1 = field1 + np.kron(np.array([ty]).T * np.random.randn(), np.array([tx]) * np.random.randn())*np.sqrt(2*c2)
    #field2 = field2 + np.kron(np.array([ty]).T * np.random.randn(), np.array([tx])   * np.random.randn())*np.sqrt(2*c2)
    #X,Y = np.meshgrid(tx,ty)

    field1 = field1[:N//2, :M//2]
    #field2 = field2[:N//2, :M//2]
    return field1
