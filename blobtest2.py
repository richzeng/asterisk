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
            cv.CvtColor(img, img, cv.CV_BGR2HSV)
            cv.Dilate(img, img, None, 3)
            cv.Erode(img, img, None, 1)
            cv.Smooth(img, img, cv.CV_BLUR, 3)
            img_H = cv.CreateImage(cv.GetSize(img), 8, 1)
            img_S = cv.CreateImage(cv.GetSize(img), 8, 1)
            img_V = cv.CreateImage(cv.GetSize(img), 8, 1)
            cv.Split(img, img_H, img_S, img_V, None)
            threshold = cv.CreateImage(cv.GetSize(img), 8, 1)
            cv.Threshold(img_H, threshold, 10, 90, cv.CV_THRESH_BINARY)
            cv.ShowImage(window, img_H)

if __name__=="__main__":
    color_tracker = BlobTracker()
    color_tracker.run()
