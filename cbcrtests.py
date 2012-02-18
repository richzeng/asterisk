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
            
            #cv.Dilate(img, img, None, 1)
            #cv.Erode(img, img, None, 3)
            #cv.Smooth(img, img, cv.CV_BLUR, 10)
            
            img_Cb = cv.CreateImage(cv.GetSize(img), 8, 1)
            img_Cr = cv.CreateImage(cv.GetSize(img), 8, 1)
            img_Y = cv.CreateImage(cv.GetSize(img), 8 ,1)
            cv.Split(img, img_Y, img_Cr, img_Cb, None)
            cv.Threshold(img_Y, img_Y, 200, 255, cv.CV_THRESH_BINARY_INV)
            #threshold1 = cv.CreateImage(cv.GetSize(img), 8, 1)
            cv.Threshold(img_Cb, img_Cb, 77, 255, cv.CV_THRESH_TOZERO)
            cv.Threshold(img_Cb, img_Cb, 127, 255, cv.CV_THRESH_BINARY_INV)
            #threshold2 = cv.CreateImage(cv.GetSize(img), 8, 1)
            cv.Threshold(img_Cr, img_Cr, 133, 255, cv.CV_THRESH_TOZERO)
            cv.Threshold(img_Cr, img_Cr, 173, 255, cv.CV_THRESH_BINARY_INV)
            threshold = cv.CreateImage(cv.GetSize(img), 8, 1)
            cv.And(img_Cb, img_Cr, threshold)
            cv.And(threshold, img_Y, threshold)

            cv.Erode(threshold, threshold, None, 3)
            cv.Smooth(threshold, threshold, cv.CV_BLUR, 10)
            
            cv.ShowImage(window,threshold)
        cv.DestroyWindow(window)
        del self.capture

if __name__=="__main__":
    color_tracker = BlobTracker()
    color_tracker.run()
