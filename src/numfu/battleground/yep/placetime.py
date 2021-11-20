import datetime, math

# a function that converts GPS time to datetime
def gps_to_datetime(gps_time):
    gps_epoch = datetime.datetime(1980, 1, 6)
    return gps_epoch + datetime.timedelta(seconds=gps_time)

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

# a function that converts utm to lat long
def utmToLatLng(zone, easting, northing, northernHemisphere=True):
    if not northernHemisphere:
        northing = 10000000 - northing

    a = 6378137
    e = 0.081819191
    e1sq = 0.006739497
    k0 = 0.9996

    arc = northing / k0
    mu = arc / (a * (1 - math.pow(e, 2) / 4.0 - 3 * math.pow(e, 4) / 64.0 - 5 * math.pow(e, 6) / 256.0))

    ei = (1 - math.pow((1 - e * e), (1 / 2.0))) / (1 + math.pow((1 - e * e), (1 / 2.0)))

    ca = 3 * ei / 2 - 27 * math.pow(ei, 3) / 32.0

    cb = 21 * math.pow(ei, 2) / 16 - 55 * math.pow(ei, 4) / 32
    cc = 151 * math.pow(ei, 3) / 96
    cd = 1097 * math.pow(ei, 4) / 512
    phi1 = mu + ca * math.sin(2 * mu) + cb * math.sin(4 * mu) + cc * math.sin(6 * mu) + cd * math.sin(8 * mu)

    n0 = a / math.pow((1 - math.pow((e * math.sin(phi1)), 2)), (1 / 2.0))

    r0 = a * (1 - e * e) / math.pow((1 - math.pow((e * math.sin(phi1)), 2)), (3 / 2.0))
    fact1 = n0 * math.tan(phi1) / r0

    _a1 = 500000 - easting
    dd0 = _a1 / (n0 * k0)
    fact2 = dd0 * dd0 / 2

    t0 = math.pow(math.tan(phi1), 2)
    Q0 = e1sq * math.pow(math.cos(phi1), 2)
    fact3 = (5 + 3 * t0 + 10 * Q0 - 4 * Q0 * Q0 - 9 * e1sq) * math.pow(dd0, 4) / 24

    fact4 = (61 + 90 * t0 + 298 * Q0 + 45 * t0 * t0 - 252 * e1sq - 3 * Q0 * Q0) * math.pow(dd0, 6) / 720

    lof1 = _a1 / (n0 * k0)
    lof2 = (1 + 2 * t0 + Q0) * math.pow(dd0, 3) / 6.0
    lof3 = (5 - 2 * Q0 + 28 * t0 - 3 * math.pow(Q0, 2) + 8 * e1sq + 24 * math.pow(t0, 2)) * math.pow(dd0, 5) / 120
    _a2 = (lof1 - lof2 + lof3) / math.cos(phi1)
    _a3 = _a2 * 180 / math.pi

    latitude = 180 * (phi1 - fact1 * (fact2 + fact3 + fact4)) / math.pi

    if not northernHemisphere:
        latitude = -latitude

    longitude = ((zone > 0) and (6 * zone - 183.0) or 3.0) - _a3

    return (latitude, longitude)

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
