# a function that efficiently draws a circle in an array
def draw_circle(array, cx, cy, cz, r):
    # get the dimensions of the array
    dims = array.shape
    # get the max radius
    max_r = min(cx, cy, (dims[0]-cx), (dims[1]-cy))
    # while the radius still exists
    while r <= max_r:
        # get the indices of the square
        x, y = np.indices((dims[0], dims[1]))
        # get the indices that are in the circle
        idx = np.where((x-cx)**2 + (y-cy)**2 <= r**2)
        # assign the circle values to those indices
        array[idx] = 1
        # decrease the radius
        r += 1

# a function that efficiently draws a sphere in an array
def draw_sphere(array, cx, cy, cz, r):
    # get the dimensions of the array
    dims = array.shape
    # get the max radius
    max_r = min(cx, cy, cz, (dims[0]-cx), (dims[1]-cy), (dims[2]-cz))
    # while the radius still exists
    while r <= max_r:
        # get the indices of the cube
        x, y, z = np.indices((dims[0], dims[1], dims[2]))
        # get the indices that are in the sphere
        idx = np.where((x-cx)**2 + (y-cy)**2 + (z-cz)**2 <= r**2)
        # assign the sphere values to those indices
        array[idx] = 1
        # decrease the radius
        r += 1

# a function that efficiently draws a cylinder in an array
def draw_cylinder(array, cx, cy, cz, r, h):
    # get the dimensions of the array
    dims = array.shape
    # get the max radius
    max_r = min(cx, cy, (dims[0]-cx), (dims[1]-cy))
    # while the radius still exists
    while r <= max_r:
        # get the indices of the square
        x, y = np.indices((dims[0], dims[1]))
        # get the indices that are in the cylinder
        idx = np.where((x-cx)**2 + (y-cy)**2 <= r**2)
        # assign the cylinder values to those indices
        array[idx] = 1
        # decrease the radius
        r += 1
    # get the indices of the square
    x, y = np.indices((dims[0], dims[1]))
    # get the indices that are in the cylinder
    idx = np.where((x-cx)**2 + (y-cy)**2 <= r**2)
    # assign the cylinder values to those indices
    array[idx] = 1
    # get the indices of the square
    x, z = np.indices((dims[0], dims[2]))
    # get the indices that are in the cylinder
    idx = np.where((x-cx)**2 + (z-cz)**2 <= r**2)
    # assign the cylinder values to those indices
    array[idx] = 1
    # get the indices of the square
    y, z = np.indices((dims[1], dims[2]))
    # get the indices that are in the cylinder
    idx = np.where((y-cy)**2 + (z-cz)**2 <= r**2)
    # assign the cylinder values to those indices
    array[idx] = 1

# a function that efficiently draws a cone in an array
def draw_cone(array, cx, cy, cz, r, h):
    # get the dimensions of the array
    dims = array.shape
    # get the max radius
    max_r = min(cx, cy, (dims[0]-cx), (dims[1]-cy))
    # while the radius still exists
    while r <= max_r:
        # get the indices of the square
        x, y = np.indices((dims[0], dims[1]))
        # get the indices that are in the cone
        idx = np.where((x-cx)**2 + (y-cy)**2 <= r**2)
        # assign the cone values to those indices
        array[idx] = 1
        # decrease the radius
        r += 1
    # get the indices of the square
    x, y = np.indices((dims[0], dims[1]))
    # get the indices that are in the cone
    idx = np.where((x-cx)**2 + (y-cy)**2 <= r**2)
    # assign the cone values to those indices
    array[idx] = 1
    # get the indices of the square
    x, z = np.indices((dims[0], dims[2]))
    # get the indices that are in the cone
    idx = np.where((x-cx)**2 + (z-cz)**2 <= r**2)
    # assign the cone values to those indices
    array[idx] = 1
    # get the indices of the square
    y, z = np.indices((dims[1], dims[2]))
    # get the indices that are in the cone
    idx = np.where((y-cy)**2 + (z-cz)**2 <= r**2)
    # assign the cone values to those indices
    array[idx] = 1