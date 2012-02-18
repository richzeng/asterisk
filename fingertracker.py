import cv2
from cv2 import cv
import numpy
from tracking import TrackerIn, util

class FingerTracker(object):
    """Finger tracking class
    """

    def __init__(self):
        """Initialize the finger tracker

        :param TrackerIn ti: Tracker input
        """
        cv.NamedWindow("Image",1)
        cv.NamedWindow("Output",1)
        self.capture = cv.CaptureFromCAM(0)

    def filter1(self, img):
        """Run filter method 1 on an image, returning a black-and-white version of it

        :param img: Input image (RGB)
        :return: Output image (Grayscale, white=finger, black=background)
        """
        cv.CvtColor(img, img, cv.CV_BGR2HSV)
        h = cv.CreateImage(cv.GetSize(img), 8, 1)
        s = cv.CreateImage(cv.GetSize(img), 8, 1)
        v = cv.CreateImage(cv.GetSize(img), 8, 1)
        cv.Split(img, h, s, v, None)

        threshold_h = cv.CreateImage(cv.GetSize(img), 8, 1)
        threshold_s = cv.CreateImage(cv.GetSize(img), 8, 1)
        threshold_total = cv.CreateImage(cv.GetSize(img), 8, 1)

        cv.Threshold(h, threshold_h, 65, 255, cv.CV_THRESH_BINARY)
        cv.Threshold(s, threshold_s, 125, 255, cv.CV_THRESH_BINARY)
        cv.And(threshold_h, threshold_s, threshold_total)

        return threshold_total

    def filter2(self, img, g_low=75, g_hi=150, h_low=55, h_hi=95, s_low=35, s_hi=255):
        """Run filter method 2 on an image, returing a black-and-white version of it

        :param img: Input image (RGB)
        :return: Output image (Grayscale, white=finger, black=background)
        """
        r = cv.CreateImage(cv.GetSize(img), 8, 1)
        g = cv.CreateImage(cv.GetSize(img), 8, 1)
        b = cv.CreateImage(cv.GetSize(img), 8, 1)
        cv.Split(img, r, g, b, None)

        cv.Smooth(g, g, cv.CV_BLUR, 4)
        threshold_g = cv.CreateImage(cv.GetSize(img), 8, 1)
        cv.InRangeS(g, g_low, g_hi, threshold_g)

        cv.CvtColor(img, img, cv.CV_BGR2HSV)
        h = cv.CreateImage(cv.GetSize(img), 8, 1)
        s = cv.CreateImage(cv.GetSize(img), 8, 1)
        v = cv.CreateImage(cv.GetSize(img), 8, 1)
        cv.Split(img, h, s, v, None)

        cv.Erode(h, h, None, 1)

        threshold_h = cv.CreateImage(cv.GetSize(img), 8, 1)
        threshold_s = cv.CreateImage(cv.GetSize(img), 8, 1)
        threshold_total = cv.CreateImage(cv.GetSize(img), 8, 1)

        cv.InRangeS(h, h_low, h_hi, threshold_h)
        cv.InRangeS(s, s_low, s_hi, threshold_s)
        cv.And(threshold_h, threshold_s, threshold_total)
        cv.And(threshold_total, threshold_g, threshold_total)

        cv.Smooth(threshold_total, threshold_total, cv.CV_BLUR, 11)
        cv.Threshold(threshold_total, threshold_total, 100, 255, cv.CV_THRESH_BINARY)
        return threshold_total

    def connectedcomps(self, img):
        rows, columns = cv.GetSize(img)
        imgc = cv.CreateImage(cv.GetSize(img), 8, 1)
        cv.Copy(img, imgc)
        def getconnectedcomp(x, y):
            imgarr = numpy.asarray(cv.GetMat(imgc))
            if(imgarr[y][x] == 255):
                return cv.FloodFill(imgc, (x, y), 125, 0, 0)
            else:
                return (0, 0, 0)
        complist = list(getconnectedcomp(x, y) for x in range(0, rows-10, 20) for y in range(0,columns-10,20))
        complist = sorted(filter(lambda comp: comp[0] > 0, complist), key = lambda comp: comp[0])
        for comp in complist:
            area = comp[0]
            if area < 400 or area > 6000:
                continue
            x, y, width, height = comp[-1]
            if float(abs(width-height))/min(width,height) > 0.15:
                continue
            print comp
            x1, x2, y1, y2 = x, x + width, y, y + height
            cv.Rectangle(img, (x1, y1), (x2, y2), (255, 0, 0))


    def run(self, ti):
        """Run the algorithm

        :param TrackerIn ti: TrackerIn object to send events to
        """
        while cv.WaitKey(10) != 27:
            img = cv.QueryFrame(self.capture)
            cv.Flip(img,img,1)
            cv.ShowImage("Image", img)

            img = self.filter2(img)
            self.connectedcomps(img)
            cv.ShowImage("Output", img)
        self.destroy()

    def destroy(self):
        """Close all windows and clean up
        """
        cv.DestroyWindow("Image")
        cv.DestroyWindow("Output")
        del self.capture


if __name__=="__main__":
    color_tracker = FingerTracker()
    def run(ti):
        color_tracker.run(ti)
    util.run_async_consumer(run, util.print_consumer)
