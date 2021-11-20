import numpy as np
from matplotlib import pyplot as plt
import matplotlib.cm as cm

# a function that renders the ellipsoid
def ellipsoid(a, b, c):
    # create the x, y, and z arrays
    x = np.linspace(-a, a, 50)
    y = np.linspace(-b, b, 50)
    z = np.linspace(-c, c, 50)
    # create the mesh grid
    xx, yy, zz = np.meshgrid(x, y, z)
    # calculate the radius squared
    r2 = xx**2 + yy**2 + zz**2
    # calculate the surface area
    area = (2 * np.pi * a * b * c) * (1 - (r2 / (a**2))**0.5 * (1 + (r2 / (b**2))**0.5 * (1 + (r2 / (c**2))**0.5)))
    # plot the surface area
    print(xx)
    print(yy)
    ax.plot_trisurf(xx.flatten(), yy.flatten(), zz.flatten())

# create the figure
fig = plt.figure()
# create the axes
ax = fig.add_subplot(111, projection='3d')
# plot the ellipsoid
ellipsoid(1, 2, 3)
# show the plot
plt.show()