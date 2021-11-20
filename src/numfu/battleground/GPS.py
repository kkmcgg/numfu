# a function that calculates position from ephemeris and pseudoranges
def calc_pos(ephemeris, pseudorange):
    # get the ephemeris data
    prn = ephemeris[0]
    toc = ephemeris[1]
    af0 = ephemeris[2]
    af1 = ephemeris[3]
    af2 = ephemeris[4]
    IODE = ephemeris[5]
    Crs = ephemeris[6]
    delta_n = ephemeris[7]
    M0 = ephemeris[8]

    # calculate time from ephemeris reference epoch
    tk = check_t(time - toc)

    # calculate corrected mean motion
    n_k = sqrt(GM / pow(a, 3)) + delta_n

    # calculate mean anomaly
    Mk = M0 + n_k * tk

    # solve Kepler's equation
    E_k = solve_kepler(Mk, e)

    # calculate the argument of latitude
    u_k = calc_u(a, e, E_k)

    # calculate the corrected argument of latitude
    omega_k = u_k + Crs

    # calculate corrected radius
    r_k = calc_r(a, e, E_k)

    # calculate inclination
    inc_k = inc

    # calculate the satellite position in orbital plane
    x_orb = r_k * cos(omega_k)
    y_orb = r_k * sin(omega_k)

    # calculate satellite position in ECEF
    x_ecef = x_orb * cos(inc_k) - y_orb * sin(inc_k) * cos(omega_k + omega_e)
    y_ecef = x_orb * sin(inc_k) + y_orb * cos(inc_k) * cos(omega_k + omega_e)
    z_ecef = y_orb * sin(omega_k + omega_e)

    # calculate satellite position vector in ECEF
    pos_ecef = array([x_ecef, y_ecef, z_ecef])

    # calculate pseudorange
    rho_meas = sqrt(pow(x_ecef, 2) + pow(y_ecef, 2) + pow(z_ecef, 2)) + Crs - \
               (sqrt(pow(x_orb, 2) + pow(y_orb, 2)) * cos(inc_k))

    return pos_ecef, rho_meas


# a function that calculates the satellite clock correction
def calc_sat_clock_correction(ephemeris, time):
    # get the ephemeris data
    prn = ephemeris[0]
    toc = ephemeris[1]
    af0 = ephemeris[2]
    af1 = ephemeris[3]
    af2 = ephemeris[4]

    # calculate time from ephemeris reference epoch
    tk = check_t(time - toc)

    # calculate satellite clock correction
    sat_clock_correction = af0 + af1 * tk + af2 * pow(tk, 2)

    return sat_clock_correction

# a function that solves keplers equations for a single time step
def kepler(M,e,E0,n):
    E = E0 - (M-E0+e*np.sin(E0))/(e*np.cos(E0)-1)
    for i in range(n):
        E = E - (M-E+e*np.sin(E))/(e*np.cos(E)-1)
    return E

# a function that calculates the true anomaly from the eccentric anomaly
def true_anomaly(E,e):
    return 2*np.arctan(np.sqrt((1+e)/(1-e))*np.tan(E/2))

# a function that calculates the distance to the central body in the
# heliocentric frame
def r_h(a,e,E):
    return a*(1-e*np.cos(E))

# a function that calculates the specific angular momentum
def h(a,e,r):
    return np.sqrt(a*(1-e**2)*mu)

# a function that calculates the specific energy
def specific_energy(a,e,r):
    return -mu/(2*a)
