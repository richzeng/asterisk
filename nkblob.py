import cv2
from cv2 import cv

class BlobTracker:
    def __init__(self):
        cv.NamedWindow("Hue",1)
        cv.NamedWindow("Saturation",1)
        cv.NamedWindow("Filtered",1)
        cv.NamedWindow("Image",1)
        self.capture = cv.CaptureFromCAM(0)

    def run(self):
        while cv.WaitKey(10) != 27:
            img = cv.QueryFrame(self.capture)
            cv.Flip(img,img,1)
            cv.CvtColor(img, img, cv.CV_BGR2HSV)
            #cv.Dilate(img, img, None, 3)
            #cv.Erode(img, img, None, 1)
            #cv.Smooth(img, img, cv.CV_BLUR, 3)
            h = cv.CreateImage(cv.GetSize(img), 8, 1)
            s = cv.CreateImage(cv.GetSize(img), 8, 1)
            v = cv.CreateImage(cv.GetSize(img), 8, 1)
            cv.Split(img, h, s, v, None)
            threshold_h = cv.CreateImage(cv.GetSize(img), 8, 1)
            cv.Threshold(h, threshold_h, 15, 255, cv.CV_THRESH_BINARY)
            cv.Merge(threshold_h, s, v, None, img)
            cv.CvtColor(img, img, cv.CV_HSV2BGR)
            cv.ShowImage("Hue", threshold_h)
            cv.ShowImage("Image", img)

    def run2(self):
        while cv.WaitKey(10) != 27:
            img = cv.QueryFrame(self.capture)
            cv.Flip(img,img,1)
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
            #cv.Merge(threshold_h, s, v, None, img)
            #cv.CvtColor(img, img, cv.CV_HSV2BGR)
            #cv.ShowImage(window_hue, threshold_h)

            #EDITS BY RICHIE
            mem = cv.CreateMemStorage()
            contours = cv.FindContours(threshold_total,mem)
            moments = cv.Moments(contours, 0)
            area = cv.GetCentralMoment(moments, 0, 0)
            if area > 10:
                x = cv.GetSpatialMoment(moments, 1, 0)/area
                y = cv.GetSpatialMoment(moments, 0, 1)/area
                print('x:{0} y{1} area:{2}'.format(x,y,area))
            #END OF EDITS BY RICHIE

            cv.ShowImage("Hue", threshold_h)
            cv.ShowImage("Saturation", threshold_s)
            cv.ShowImage("Filtered", threshold_total)
            cv.ShowImage("Image", img)
            #cv.ShowImage(window_rgb, img)

if __name__=="__main__":
    color_tracker = BlobTracker()
    color_tracker.run2()
