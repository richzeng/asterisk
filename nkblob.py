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
        self.destroy()

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
            cv.ShowImage("Hue", threshold_h)
            cv.ShowImage("Saturation", threshold_s)
            cv.ShowImage("Filtered", threshold_total)
            cv.ShowImage("Image", img)
            #cv.ShowImage(window_rgb, img)
        self.destroy()
    
    def destroy(self):
        cv.DestroyWindow("Hue")
        cv.DestroyWindow("Saturation")
        cv.DestroyWindow("Filtered")
        cv.DestroyWindow("Image")
        del self.capture

if __name__=="__main__":
    color_tracker = BlobTracker()
    color_tracker.run2()
