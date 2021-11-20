# a function simulates fluidflow on a mesh
#
# input:
#   mesh: the mesh
#   u0: the initial velocity
#   p0: the initial pressure
#   t: the current time
#   dt: the time step
#   mu: the dynamic viscosity
#   rho: the density
#   return_vars: a list of strings that specifies the variables to be returned
#
# output:
#   u: the velocity at time t+dt
#   p: the pressure at time t+dt
#   div: the divergence at time t+dt
#   if return_vars is not empty, the function will in addition return these variables
def simulate_fluid(mesh, u0, p0, t, dt, mu, rho, return_vars=[]):
    # compute the divergence on the mesh
    div = compute_divergence(mesh, u0)

    # compute the right hand side for the momentum equation
    f_mom = compute_momentum(mesh, u0, p0, div, mu, rho)

    # compute the right hand side for the continuity equation
    f_cont = compute_continuity(mesh, div, p0)

    # assemble the right hand side
    f = f_mom + f_cont

    # solve the linear system
    u, p = solve_system(mesh, f, div, mu, rho)

    # return the variables that were asked for
    return [u, p] + [div] if "div" in return_vars else [u, p]

# a function computes the divergence on a given mesh
#
# input:
#   mesh: the mesh
#   u: the velocity
#
# output:
#   div: the divergence
def compute_divergence(mesh, u):
    # allocate an array for the divergence
    div = np.zeros(mesh.n_eq)

    # compute the divergence at all cell centers
    for c in mesh:
        div[:2] += c.J.dot(u[c.dofs])

    # return the divergence
    return div

# a function computes the right hand side of the momentum equation
#
# input:
#   mesh: the mesh
#   u: the velocity
#   p: the pressure
#   div: the divergence
#   mu: the dynamic viscosity
#   rho: the density
#
# output:
#   f_mom: the right hand side of the momentum equation
def compute_momentum(mesh, u, p, div, mu, rho):
    # allocate an array for the right hand side of the momentum equation
    f_mom = np.zeros(mesh.n_eq)

    # compute the right hand side at all cell centers
    for c in mesh:
        f_mom[:2] += c.J.dot(mu * c.K.dot(u[c.dofs]) + rho * c.F.dot(u[c.dofs]))

    # return the right hand side
    return f_mom

# a function computes the right hand side of the continuity equation
#
# input:
#   mesh: the mesh
#   div: the divergence
#   p: the pressure
#
# output:
#   f_cont: the right hand side of the continuity equation
def compute_continuity(mesh, div, p):
    # allocate an array for the right hand side of the continuity equation
    f_cont = np.zeros(mesh.n_eq)

    # compute the right hand side at all cell centers
    for c in mesh:
        f_cont[2] += c.J.dot(p[c.dofs])

    # return the right hand side
    return f_cont

# a function solves the linear system
#
# input:
#   mesh: the mesh
#   f: the right hand side of the linear system
#   div: the divergence
#   mu: the dynamic viscosity
#   rho: the density
#
# output:
#   u: the velocity
#   p: the pressure
def solve_system(mesh, f, div, mu, rho):
    # allocate an array for the velocity
    u = np.zeros(mesh.n_eq)

    # allocate an array for the pressure
    p = np.zeros(mesh.n_eq)

    # allocate an array for the right hand side of the linear system
    b = np.zeros(mesh.n_eq)

    # compute the right hand side at all cell centers
    for c in mesh:
        b[:2] += c.J.dot(mu * c.K.dot(u[c.dofs]) + rho * c.F.dot(u[c.dofs]))
        b[2] += c.J.dot(p[c.dofs])

    # add the right hand side for the continuity equation
    b[2] += div[2]

    # assemble the linear system
    A = assemble_linear_system(mesh, mu, rho)

    # solve the linear system
    u, p = solve_linear_system(A, b)

    # return the velocity and the pressure
    return u, p

# a function assembles the linear system
#
# input:
#   mesh: the mesh
#   mu: the dynamic viscosity
#   rho: the density
#
# output:
#   A: the matrix of the linear system
def assemble_linear_system(mesh, mu, rho):
    # allocate an array for the matrix of the linear system
    A = np.zeros((mesh.n_eq, mesh.n_eq))

    # allocate an array for the right hand side of the linear system
    b = np.zeros(mesh.n_eq)

    # assemble the linear system
    for c in mesh:
        # compute the contributions to the matrix
        A[:2, :2] += c.J.T.dot(mu * c.K.dot(c.J))
        A[:2, 2] += c.J.T.dot(rho * c.F.dot(c.J))
        A[2, :2] += c.J.T.dot(p[c.dofs])
        A[2, 2] += c.J.T.dot(c.J)

        # compute the contributions to the right hand side
        b[:2] += c.J.T.dot(mu * c.K.dot(u[c.dofs]) + rho * c.F.dot(u[c.dofs]))
        b[2] += c.J.T.dot(p[c.dofs])

    # return the matrix of the linear system
    return A

# a function solves the linear system
#
# input:
#   A: the matrix of the linear system
#   b: the right hand side of the linear system
#
# output:
#   u: the velocity
#   p: the pressure
def solve_linear_system(A, b):
    # solve the linear system
    u = np.linalg.solve(A, b)

    # return the velocity and the pressure
    return u[:2], u[2]

# a function plots the solution
#
# input:
#   mesh: the mesh
#   u: the velocity
#   p: the pressure
#   t: the current time
#   dt: the time step
#   mu: the dynamic viscosity
#   rho: the density
#   out_dir: the output directory
def plot_solution(mesh, u, p, t, dt, mu, rho, out_dir):
    # create the output directory if it does not exist
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    # plot the velocity
    plot_field(mesh, u, "velocity", out_dir, t, dt, "u")

    # plot the pressure
    plot_field(mesh, p, "pressure", out_dir, t, dt, "p")

# a function plots a field
#
# input:
#   mesh: the mesh
#   field: the field
#   field_name: the name of the field
#   out_dir: the output directory
#   t: the current time
#   dt: the time step
#   suffix: the suffix of the output file
def plot_field(mesh, field, field_name, out_dir, t, dt, suffix):
    # create the output directory if it does not exist
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    # create a figure
    fig = plt.figure()

    # add plot with correct aspect ratio
    ax = fig.add_subplot(111, aspect='equal')

    # plot the mesh
    plot_mesh(ax, mesh)

    # plot the field
    plot_scalar_field(ax, mesh, field, field_name)

    # save the figure
    fig.savefig(os.path.join(out_dir, "%s_%04d_%04d.png" % (suffix, t // dt, t)))

    # close the figure
    plt.close(fig)

# a function plots a mesh
#
# input:
#   ax: the axes of the plot
#   mesh: the mesh
def plot_mesh(ax, mesh):
    # plot the cells
    for c in mesh:
        ax.add_patch(mpl.patches.Polygon(c.get_vertices()[:, :2], fill=False))

    # plot the vertices
    ax.plot(mesh.vertices[:, 0], mesh.vertices[:, 1], 'ko')

    # set the aspect ratio of the data
    ax.set_aspect('equal')
