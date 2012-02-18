import cv2
from cv2 import cv

window = "Blob Tracker"

class BlobTracker:
    def __init__(self):
        cv.NamedWindow(window,1)
        self.capture = cv.CaptureFromCAM(0)

    def run(self):
        while cv.WaitKey(10) != 27:
            img = cv.QueryFrame(self.capture)
            cv.Flip(img,img,1)
            cv.CvtColor(img, img, cv.CV_BGR2YCrCb)
            #cv.Dilate(img, img, None, 3)
            #cv.Erode(img, img, None, 1)
            #cv.Smooth(img, img, cv.CV_BLUR, 3)
            img_Cb = cv.CreateImage(cv.GetSize(img), 8, 1)
            img_Cr = cv.CreateImage(cv.GetSize(img), 8, 1)
            cv.Split(img, None, img_Cr, img_Cb, None)
            threshold1 = cv.CreateImage(cv.GetSize(img), 8, 1)
            cv.Threshold(img_Cb, threshold1, 77, 255, cv.CV_THRESH_BINARY)
            cv.Threshold(img_Cb, threshold1, 120, 255, cv.CV_THRESH_BINARY_INV)
            threshold2 = cv.CreateImage(cv.GetSize(img), 8, 1)
            cv.Threshold(img_Cr, threshold2, 133, 255, cv.CV_THRESH_BINARY)
            cv.Threshold(img_Cr, threshold2, 173, 255, cv.CV_THRESH_BINARY_INV)
            threshold = cv.CreateImage(cv.GetSize(img), 8, 1)
            cv.And(threshold1, threshold2, threshold)
            cv.ShowImage(window, threshold)
        cv.DestroyWindow("video")

if __name__=="__main__":
    color_tracker = BlobTracker()
    color_tracker.run()
