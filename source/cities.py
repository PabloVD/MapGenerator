#---------------------------
# Cities module
# PabloVD
# Started: 11/5/20
#---------------------------

import numpy as np
from scipy import interpolate

# Generate a Poisson point process
def poisson_process(dim):

    # Simulation window parameters
    xMin, xMax = 0., dim
    yMin, yMax = 0., dim

    # Average number of points in the window for the Poisson point process
    lamb = 30

    # Get number of points
    n_points = np.random.poisson( lamb )

    # x and y coordinates of Poisson points
    xx = xMin + (xMax-xMin) * np.random.uniform(0, 1, n_points)
    yy = yMin + (yMax-yMin) * np.random.uniform(0, 1, n_points)

    return xx, yy

# Generate a Thomas point process
# Based on https://hpaulkeeler.com/simulating-a-thomas-cluster-point-process/
def thomas_process(dim, xxParent, yyParent):

    # Simulation window parameters
    xMin, xMax = 0., dim
    yMin, yMax = 0., dim

    # Number of Poisson parents
    numbPointsParent = len(xxParent)
    # Mean number of points in each cluster
    lambdaDaughter = 10
    # Sigma for normal variables (ie random locations) of daughters
    sigma_thomas = 50.#0.05

    # Simulate Poisson point process for the daughters (ie final point process)
    numbPointsDaughter = np.random.poisson(lambdaDaughter, numbPointsParent)
    numbPoints = sum(numbPointsDaughter) # total number of points

    # Generate the (relative) locations in Cartesian coordinates by
    # simulating independent normal variables
    xx0 = np.random.normal(0, sigma_thomas, numbPoints) # (relative) x coordinaets
    yy0 = np.random.normal(0, sigma_thomas, numbPoints) # (relative) y coordinates

    # replicate parent points (ie centres of disks/clusters)
    xx = np.repeat(xxParent, numbPointsDaughter)
    yy = np.repeat(yyParent, numbPointsDaughter)

    # translate points (ie parents points are the centres of cluster disks)
    xx = xx + xx0
    yy = yy + yy0

    # thin points if outside the simulation window
    booleInside=((xx>=xMin)&(xx<=xMax)&(yy>=yMin)&(yy<=yMax))
    # retain points inside simulation window
    xx = xx[booleInside]
    yy = yy[booleInside]

    return xx, yy

# Thinning a point process with a probability given by the field
def thinning(field, xx, yy):

    # Get the probability to thin a point from the interpolated field
    x, y = np.linspace(0,field.shape[0],num=field.shape[0]), np.linspace(0,field.shape[1],num=field.shape[1])
    f = interpolate.interp2d(x,y,field,kind="linear")
    p = []
    for xxx, yyy in zip(xx,yy):
        p.append(f(xxx, yyy))
    p = np.array(p)

    #Generate Bernoulli variables (ie coin flips) for thinning
    booleThinned = np.random.uniform(0,1,(len(xx),1))>p #points to be thinned
    booleRetained =~ booleThinned #points to be retained

    #x/y locations of retained points
    xx, yy = xx.reshape(-1,1), yy.reshape(-1,1)
    xxRetained, yyRetained = xx[booleRetained], yy[booleRetained]

    return xxRetained, yyRetained

# Generate city locations
# 1. Randomly place capital cities following Poisson processes
# 2. Thin the point process to remove capitals under the sea level
# 3. Place cities around capitals following the Thomas process
# 4. Thin the point process to remove cities under the sea level
# 5. TO DO Remove capitals to close each other
def generate_cities(field):
    xx_p, yy_p = poisson_process(field.shape[0])
    xx_p, yy_p = thinning(field, xx_p, yy_p)
    xx, yy = thomas_process(field.shape[0], xx_p, yy_p)
    xx, yy = thinning(field, xx, yy)
    return xx_p, yy_p, xx, yy
