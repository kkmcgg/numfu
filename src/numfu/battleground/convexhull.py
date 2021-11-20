# a function that calculates convex hull of a set of points
def convex_hull(points):
    # find the leftmost point
    start = points[0]
    min_x = start[0]
    for p in points[1:]:
        if p[0] < min_x:
            min_x = p[0]
            start = p
    # sort the points by polar angle with the start
    points.sort(key=lambda p: math.atan2(p[1] - start[1], p[0] - start[0]))
    # find the hull points
    hull = [start, points[1]]
    for p in points[2:]:
        hull.append(p)
        while len(hull) > 2 and not is_left(hull[-3], hull[-2], hull[-1]):
            del hull[-2]
    return hull