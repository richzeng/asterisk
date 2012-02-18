def make_gesture(min_size, way_points):
    """Returns a gesture with minimum allowed size min_size and way points
    way_points

    :param tuple min_size: (min_size_x, min_size_y), if the points are smaller
    than this it breaks
    :param list way_points: a list of way points for the gesture
    """
    return (min_size, way_points)

def sqr_min_dist(point, line):
    """Returns the square of the minimum of the distance from point, 'point,'
    to the line segment, 'line'

    :param tuple point: The point in the form (x, y)
    :param tuple line: The line in the form ((x1, y1), (x2, y2)
    """
    x1, x2, x3 = line[0][0], line[1][0], point[0]
    y1, y2, y3 = line[0][1], line[1][1], point[1]
    if x2 == x1 and y2 == y1:
        return (x3-x1)**2 + (y3-y1)**2
    u = ((x3-x1)*(x2-x1) + (y3-y1)*(y2-y1)) / ((x2-x1)**2 + (y2-y1)**2)
    x = x1 + u * (x2 - x1)
    y = y1 + u * (y2 - y1)
    if x1 <= x and x2 >= x and y1 <= y and y2 >= y:
        return (x3-x)**2 + (y3-y)**2
    return min((x3-x1)**2+(y3-y1)**2, (x3-x2)**2+(y3-y2)**2)

def error(gesture, points):
    n = len(points)
    return sum(min(sqr_min_dist(i, (points[x-1], points[x])) for x in range(1, n)) for i in gesture)

def resize(gesture, points, min_size):
    """Returns the ratio to multiply the points by, and the x, y shift to shift
    them by.

    :param list gesture: The gesture to resize the points to
    :param list points: The points (of the fingers) to resize
    :param tuple min_size: The minimum size for the points. Anything smaller
    will cause the function to return (None, None, None)
    """
    g_max_x, g_min_x = max(i[0] for i in gesture), min(i[0] for i in gesture)
    g_size_x = g_max_x - g_min_x
    g_max_y, g_min_y = max(i[1] for i in gesture), min(i[1] for i in gesture)
    g_size_y = g_max_y - g_min_y
        
    p_max_x, p_min_x = max(i[0] for i in points), min(i[0] for i in points)
    p_size_x = p_max_x - p_min_x
    p_max_y, p_min_y = max(i[1] for i in points), min(i[1] for i in points)
    p_size_y = p_max_y - p_min_y
    if p_size_x <= min_size[0] or p_size_y <= min_size[1]:
        return (None, None, None)
        
    if p_size_x == 0:
        if p_size_y == 0:
            ratio = 1 # ?
        else:
            ratio = g_size_y * 1.0 / p_size_y
    elif p_size_y == 0:
        ratio = g_size_x * 1.0 / p_size_x
    else:
        ratio = (g_size_x * p_size_x + g_size_y * p_size_y)
        ratio = ratio * 1.0 / (p_size_x**2 + p_size_y**2)

    x_shift, y_shift = ratio*p_min_x - g_min_x, ratio*p_min_y - g_min_y

    return (ratio, x_shift, y_shift)

THRESHOLD = 0.01

def match(gestures, points):
    """Finds matches to gestures in points. Algorithm -
    1. For every subset of points from points[:] to points[-2:]
    2. for every gesture
    3. If the points are smaller that the min_size for that gesture, skip it
    4. If the points are in the wrong direction, skip them.
    5. Resize and shift the image to fit the gesture.
    6. Check the error from the gesture to the points.
    7. If this error is under the threshold, return this gesture's index

    :param list gestures: a list of gesturesto compare to the points
    :param list points: The list of positions of the hand
    """
    for n in range(len(points) - 2):
        t_points = points[n:]
        for index in range(len(gestures)):
            min_size, gesture = gestures[index]
            ratio, x_shift, y_shift = resize(gesture, t_points, min_size)
            sgn_g_x = cmp(gesture[-1][0] - gesture[0][0], 0)
            sgn_g_y = cmp(gesture[-1][1] - gesture[0][1], 0)
            sgn_p_x = cmp(points[-1][0] - points[0][0], 0)
            sgn_p_y = cmp(points[-1][1] - points[0][1], 0)
            if sgn_g_x != 0 and sgn_p_x != 0 and sgn_g_x != sgn_p_x: continue
            if sgn_g_y != 0 and sgn_p_y != 0 and sgn_g_y != sgn_p_y: continue
            if ratio == None: continue
            if ratio <= 0: continue
            r_points = [(ratio*i[0], ratio*i[1]) for i in t_points]
            r_points = [(i[0] - x_shift, i[1] - y_shift) for i in r_points]
            err = error(gesture, r_points)
            if err <= THRESHOLD:
                print "Error for gesture", index, "=", err
                return index
    return None

sample_points = ((223, 189), (223, 187), (223, 184), (223, 182), (223, 179), (222, 176), (222, 173), (221, 170), (221, 167), (220, 164), (220, 161), (219, 158), (218, 155), (217, 151), (217, 148), (216, 145), (216, 142), (215, 138), (215, 135), (216, 132), (216, 129), (215, 125), (215, 122), (216, 120), (216, 117), (217, 113), (217, 110), (217, 107), (216, 103), (216, 99), (214, 95), (213, 92), (212, 89), (211, 87), (210, 87), (210, 89))
gestures = (make_gesture((0, 50), ((0, 0), (0, 1))),)
