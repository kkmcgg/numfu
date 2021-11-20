# a function that computes a kd-tree
def kdtree(points, depth=0):
    n = len(points)
    if n <= 0:
        return None
    axis = depth % k
    sorted_points = sorted(points, key=lambda point: point[axis])
    return {
        'point': sorted_points[n // 2],
        'left': kdtree(sorted_points[:n // 2], depth + 1),
        'right': kdtree(sorted_points[n // 2 + 1:], depth + 1)
    }


# a function that computes the distance between 2 points
def distance(a, b):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(a, b)))


# a function that computes the distance between a point and a segment
def distance_point_segment(point, segment):
    a, b = segment
    if all(a == point) or all(b == point):
        return 0
    if all(a == b):
        return distance(point, a)
    if a[0] == b[0]:
        return abs(point[0] - a[0])
    m = (b[1] - a[1]) / (b[0] - a[0])
    c = a[1] - m * a[0]
    x = (m * point[0] - point[1] + c) / (m * m + 1)
    y = m * x
    if x < min(a[0], b[0]) or x > max(a[0], b[0]):
        return min(distance(point, a), distance(point, b))
    return distance(point, (x, y))


# a function that computes the distance between a point and a kd-tree
def distance_point_kdtree(point, kdtree):
    if kdtree is None:
        return float('inf')
    k, axis = len(point), depth % k
    next_branch = kdtree['point'][axis] <= point[axis]
    return min(distance_point_kdtree(point, kdtree[next_branch]), distance_point_segment(point, (kdtree['point'], kdtree[next_branch ^ True]['point'])))


# a function that computes the distance between 2 segments
def distance_segment_segment(segment1, segment2):
    a, b = segment1
    c, d = segment2
    if all(a == c) or all(a == d) or all(b == c) or all(b == d):
        return 0
    if all(a == b):
        return min(distance_point_segment(c, segment1), distance_point_segment(d, segment1))
    if a[0] == b[0]:
        return min(distance_point_segment(c, segment1), distance_point_segment(d, segment1), distance_point_segment(a, segment2), distance_point_segment(b, segment2))
    m1 = (b[1] - a[1]) / (b[0] - a[0])
    m2 = (d[1] - c[1]) / (d[0] - c[0])
    if m1 == m2:
        return min(distance_point_segment(c, segment1), distance_point_segment(d, segment1), distance_point_segment(a, segment2), distance_point_segment(b, segment2))
    x = (m1 * a[0] - m2 * c[0] - a[1] + c[1]) / (m1 - m2)
    y = m1 * x
    return min(distance_point_segment(c, segment1), distance_point_segment(d, segment1), distance_point_segment(a, segment2), distance_point_segment(b, segment2), distance_point_segment((x, y), segment1), distance_point_segment((x, y), segment2))


# a function that computes the distance between 2 kd-trees
def distance_kdtree_kdtree(kdtree1, kdtree2):
    if kdtree1 is None or kdtree2 is None:
        return float('inf')
    k, axis = len(kdtree1['point']), depth % k
    next_branch = kdtree1['point'][axis] <= kdtree2['point'][axis]
    return min(distance_kdtree_kdtree(kdtree1[next_branch], kdtree2[next_branch]), distance_kdtree_kdtree(kdtree1[next_branch ^ True], kdtree2[next_branch]), distance_segment_segment((kdtree1['point'], kdtree1[next_branch ^ True]['point']), (kdtree2['point'], kdtree2[next_branch]['point'])))
