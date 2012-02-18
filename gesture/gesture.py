import mouse

class Gesture():
    def __init__(self, name, waypoints, min_sizes = None, command = None, delay = 0.25):
        self.name = name
        self.waypoints = waypoints
        self.finger_num = len(waypoints)
        if min_sizes != None:
            self.min_sizes = min_sizes
            if len(min_sizes) != self.finger_num:
                print "Warning: Invalid min_sizes. Continuing anyway."
        else:
            self.min_sizes = [(0, 0) for i in range(self.finger_num)]
        if command != None:
            self.command = command
        else:
            def print_name():
                print name
            self.command = print_name
        self.delay = delay
    def execute(self):
        self.command()

def is_between(x1, x2, x):
    if x1 <= x2:
        return x1 <= x and x2 >= x
    else:
        return x2 <= x and x1 >= x

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
    if is_between(x1, x2, x) and is_between(y1, y2, y):
        return (x3-x)**2 + (y3-y)**2
    return min((x3-x1)**2+(y3-y1)**2, (x3-x2)**2+(y3-y2)**2)

def error(gesture, points):
    """Returns the sum of the sqr_min_dist of each point in gesture to some line
    in points added to the sqr_min_dist of each point in points to some line in
    gestures

    :param list gesture: The gesture's waypoints
    :param list points: The points of the finger
    """
    np = len(points)
    ng = len(gesture)
    err = sum(min(sqr_min_dist(i, (points[x-1], points[x])) for x in range(1, np)) for i in gesture)
    err += sum(min(sqr_min_dist(i, (gesture[x-1], gesture[x])) for x in range(1, ng)) for i in points)
    return err

def resize(gesture, points, min_size):
    """Returns the ratio to multiply the points by, and the x, y shift to shift
    them by.
    
    :param list gesture: The waypoints of the gesture to resize the points to
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

THRESHOLD = 0.05

def compare(gesture, points):
    finger_count = len(points[0])
    if gesture.finger_num != finger_count:
        return None
    gesture_err = None
    for n in xrange(finger_count):
        waypoints = gesture.waypoints[n]
        min_size = gesture.min_sizes[n]
        sgn_g_x = cmp(waypoints[-1][0] - waypoints[0][0], 0)
        sgn_g_y = cmp(waypoints[-1][1] - waypoints[0][1], 0)
        min_err = None
        for s in range(len(points) - 2):
            t_points = [p[n] for p in points[s:]]
            ratio, x_shift, y_shift = resize(waypoints, t_points, min_size)
                
            sgn_p_x = cmp(t_points[-1][0] - t_points[0][0], 0)
            sgn_p_y = cmp(t_points[-1][1] - t_points[0][1], 0)
            if sgn_g_x != 0 and sgn_p_x != 0 and sgn_g_x != sgn_p_x: continue
            if sgn_g_y != 0 and sgn_p_y != 0 and sgn_g_y != sgn_p_y: continue
            if ratio == None: continue
            if ratio <= 0: continue
            r_points = [(ratio*i[0], ratio*i[1]) for i in t_points]
            r_points = [(i[0] - x_shift, i[1] - y_shift) for i in r_points]
            err = error(waypoints, r_points)
            if min_err == None:
                min_err = err
            else:
                min_err = min(err, min_err)
        if min_err == None:
            return None
        if gesture_err == None:
            gesture_err = min_err
        else:
            gesture_err += min_err
    if gesture_err != None:
        return gesture_err * 1.0 / finger_count
    else:
        return None

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
    gesture_errors = [compare(gesture, points) for gesture in gestures]
    if len(gesture_errors) == 0 or all(e == None for e in gesture_errors):
        return None
    min_err = min(e for e in gesture_errors if e != None)
    if min_err == None or min_err > THRESHOLD:
        return None
    index = gesture_errors.index(min_err)
    return gestures[index]

def make_default_gesture(name, count, end, default_size, command=None):
    return Gesture(name, [[(0, 0), end] for i in range(count)], [default_size for i in range(count)], command)

sample_points = [[(223, 189)], [(223, 187)], [(223, 184)], [(223, 182)], [(223, 179)], [(222, 176)], [(222, 173)], [(221, 170)], [(221, 167)], [(220, 164)], [(220, 161)], [(219, 158)], [(218, 155)], [(217, 151)], [(217, 148)], [(216, 145)], [(216, 142)], [(215, 138)], [(215, 135)], [(216, 132)], [(216, 129)], [(215, 125)], [(215, 122)], [(216, 120)], [(216, 117)], [(217, 113)], [(217, 110)], [(217, 107)], [(216, 103)], [(216, 99)], [(214, 95)], [(213, 92)], [(212, 89)], [(211, 87)], [(210, 87)], [(210, 89)]]
one_up = Gesture("One Up", [[(0, 0), (0, 1)]], [(0, 50)])
two_left = make_default_gesture("Two Left", 2, (-1, 0), (50, 0), mouse.move_left)
two_right = make_default_gesture("Two Right", 2, (1, 0), (50, 0), mouse.move_right)
two_up = make_default_gesture("Two Up", 2, (0, -1), (0, 50), mouse.move_up)
two_down = make_default_gesture("Two Down", 2, (0, 1), (0, 50), mouse.move_down)
two_together = Gesture("Two Together", [[(0, 0), (1, 0)], [(0, 0), (-1, 0)]], [(50, 0), (50, 0)])
two_away = Gesture("Two Away", [[(0, 0), (-1, 0)], [(0, 0), (1, 0)]], [(50, 0), (50, 0)])
gestures = [one_up, two_left, two_right, two_up, two_down, two_together, two_away]
