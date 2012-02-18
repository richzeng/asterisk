import gesture
if __name__ == '__main__':
    from cv2 import cv

camcapture = cv.CreateCameraCapture(0)

TPL_WIDTH= 15 # template width
TPL_HEIGHT= 15 # template height
WINDOW_WIDTH = 24 # search window width
WINDOW_HEIGHT = 24 # search window height
THRESHOLD = 0.2
MAX_POINTS = 50

frame = cv.QueryFrame(camcapture)

object_x0 = cv.GetSize(frame)[0] // 2
object_y0 = cv.GetSize(frame)[1] // 2
is_tracking = False

gray = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_8U, 1)
cv.CvtColor(frame, gray, cv.CV_RGB2GRAY)

tpl = cv.CreateImage((TPL_WIDTH,TPL_HEIGHT), cv.IPL_DEPTH_8U, 1)

# create image to store template matching result in
tm = cv.CreateImage((WINDOW_WIDTH-TPL_WIDTH+1, WINDOW_HEIGHT-TPL_HEIGHT+1),
                    cv.IPL_DEPTH_32F, 1)

def get_rect(img, rect):
    """Returns a rectangle based on the original, but within the bounds of
    the image, shifting it around the image's boundaries.

    Arguments:
    :param cvImage img: The img to load the boundaries from
    :param tuple rect: The initial rectangle to shift
    """
    w = img.width
    h = img.height
    if rect[0] + rect[2] > w:
        rect = (w - rect[2], rect[1], rect[2], rect[3])
    elif rect[0] < 0:
        rect = (0, rect[1], rect[2], rect[3])
    if rect[1] + rect[3] > h:
        rect = (rect[0], h - rect[3], rect[2], rect[3])
    elif rect[1] < 0:
        rect = (rect[0], 0, rect[2], rect[3])
    return rect

def trackobject(img, frame):
    """Tracks the object, updating it's position, is_tracking, and past_point,
    by finding the template, tpl in the image within an area

    Arguments:
    :param cvImage img: the image to search in. In grayscale
    :param cvImage frame: the image in color (to draw the rectangle in)
    """
    global object_x0, object_y0, is_tracking, past_points
    object_x0 -= (WINDOW_WIDTH - TPL_WIDTH) // 2
    object_y0 -= (WINDOW_HEIGHT - TPL_HEIGHT) // 2
    rect = get_rect(img, (object_x0, object_y0, WINDOW_WIDTH, WINDOW_HEIGHT))
    window = cv.GetSubRect(img, rect)
    cv.MatchTemplate(window, tpl, tm, cv.CV_TM_SQDIFF_NORMED)
    minval, maxval, minloc, maxloc = cv.MinMaxLoc(tm)
    if minval <= THRESHOLD:
        rect = get_rect(img, (minloc[0] + object_x0, minloc[1] + object_y0,
                              WINDOW_WIDTH, WINDOW_HEIGHT))
        object_x0 = rect[0]
        object_y0 = rect[1]
        
        past_points.append((object_x0, object_y0))
        if len(past_points) > MAX_POINTS:
            past_points = past_points[1:]
        
        cv.Rectangle(frame, (object_x0, object_y0),
                     (object_x0+TPL_WIDTH, object_y0+TPL_HEIGHT),
                     (0,0,1,0),3,8,0)
    else:
        #if not found
        print "Lost object"
        is_tracking = False


def mousecallback(event, x, y, flags, param):
    """Handles mouseclicks by tracking the object at the click location.
    Overrides the default cvImage mouse click.

    Arguments:
    :param thing event: The type of mouse click (left click, right click, etc.)
    :param int x: the x position of the mouse click
    :param int y: the y position of the mouse click
    :param thing flags: no idea what this is.
    :param thing param: no idea what this is.
    """
    global gray, is_tracking, object_x0, object_y0, tpl
    if event == cv.CV_EVENT_LBUTTONUP:
        rect = get_rect(gray, (x - TPL_WIDTH // 2, y - TPL_HEIGHT // 2,
                               WINDOW_WIDTH, WINDOW_HEIGHT))
        object_x0 = rect[0]
        object_y0 = rect[1]
        sub = cv.GetSubRect(gray, (rect[0], rect[1], TPL_WIDTH, TPL_HEIGHT))
        cv.Copy(sub, tpl)
        print "Template selected. Start tracking"
        is_tracking = True

cv.ShowImage("video", gray)
cv.SetMouseCallback("video", mousecallback)

past_points = []

while True:
    frame = cv.QueryFrame(camcapture)
    if frame is None:
        break
    cv.Flip(frame, frame, cv.CV_CVTIMG_FLIP)
    cv.CvtColor(frame, gray, cv.CV_RGB2GRAY)

    if is_tracking:
        trackobject(gray, frame)
        if len(past_points) == MAX_POINTS:
            g = gesture.match(gesture.gestures, past_points)
            if g != None:
                print "Gesture detected! Gesture index =", g
    cv.ShowImage("video", frame)
    k=cv.WaitKey(10)
    if k == 27:
        break

cv.DestroyWindow("video")
del camcapture
