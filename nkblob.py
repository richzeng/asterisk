import cv2
from cv2 import cv

class BlobTracker:
    def __init__(self):
        cv.NamedWindow("Hue",1)
        cv.NamedWindow("Saturation",1)
        cv.NamedWindow("Filtered",1)
        cv.NamedWindow("Eroded",1)
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
            r = cv.CreateImage(cv.GetSize(img), 8, 1)
            g = cv.CreateImage(cv.GetSize(img), 8, 1)
            b = cv.CreateImage(cv.GetSize(img), 8, 1)
            cv.Split(img, b, g, r, None)

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

            do_blur = True
            if do_blur:
                cv.Smooth(threshold_total, threshold_total, cv.CV_BLUR, 10)
                cv.Erode(threshold_total, threshold_total, None, 3)
                #cv.Dilate(threshold_total, threshold_total, None, 4)
                #cv.Smooth(threshold_total, threshold_total, cv.CV_BLUR, 5)

                blurred = cv.CreateImage(cv.GetSize(img), 8, 1)
                cv.Smooth(threshold_total, blurred, cv.CV_BLUR, 2)
                cv.AddWeighted(threshold_total, 1.8, blurred, -0.8, 0, threshold_total)
                cv.Dilate(threshold_total, threshold_total, None, 1)
                #cv.Erode(threshold_total, threshold_total, None, 6)

            do_edges = False
            if do_edges:
                mem = cv.CreateMemStorage()
                contours = cv.FindContours(threshold_total,mem,cv.CV_RETR_LIST)
                moments = cv.Moments(contours, 0)
                area = cv.GetCentralMoment(moments, 0, 0)
                if area > 10:
                    x = cv.GetSpatialMoment(moments, 1, 0)/area
                    y = cv.GetSpatialMoment(moments, 0, 1)/area
                    print('x:{0} y{1} area:{2}'.format(x,y,area))

            do_box = True
            if do_box:
                cv.Canny(threshold_total, threshold_total, 25, 75)
                storage = cv.CreateMemStorage(0)
                obj = cv.FindContours(threshold_total, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
                box = cv.BoundingRect(obj)
                print((box[0]+(box[2]/2), box[1]+(box[3]/2)))
                cv.Rectangle(img, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]),(255,0,0),1,8,0)

            cv.ShowImage("Eroded", threshold_total)
            cv.ShowImage("Image", img)
        self.destroy()

    def destroy(self):
        cv.DestroyWindow("Hue")
        cv.DestroyWindow("Saturation")
        cv.DestroyWindow("Filtered")
        cv.DestroyWindow("Eroded")
        cv.DestroyWindow("Image")
        del self.capture

if __name__=="__main__":
    color_tracker = BlobTracker()
    color_tracker.run2()
