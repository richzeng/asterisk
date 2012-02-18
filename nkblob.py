import cv2
from cv2 import cv

class BlobTracker:
    def __init__(self):
        cv.NamedWindow("Image",1)
        cv.NamedWindow("Filtered",1)
        cv.NamedWindow("Threshold",1)
        cv.NamedWindow("Postprocessed",1)
        cv.NamedWindow("Test",1)
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
            cv.ShowImage("Image", img)

            r = cv.CreateImage(cv.GetSize(img), 8, 1)
            g = cv.CreateImage(cv.GetSize(img), 8, 1)
            b = cv.CreateImage(cv.GetSize(img), 8, 1)
            cv.Split(img, r, g, b, None)

            cv.Smooth(g, g, cv.CV_BLUR, 4)
            threshold_g = cv.CreateImage(cv.GetSize(img), 8, 1)
            cv.InRangeS(g, 75, 150, threshold_g)

            cv.CvtColor(img, img, cv.CV_BGR2HSV)
            h = cv.CreateImage(cv.GetSize(img), 8, 1)
            s = cv.CreateImage(cv.GetSize(img), 8, 1)
            v = cv.CreateImage(cv.GetSize(img), 8, 1)
            cv.Split(img, h, s, v, None)
            cv.Erode(h, h, None, 1)
            threshold_h = cv.CreateImage(cv.GetSize(img), 8, 1)
            threshold_s = cv.CreateImage(cv.GetSize(img), 8, 1)


            threshold_total = cv.CreateImage(cv.GetSize(img), 8, 1)
            cv.InRangeS(h, 55, 95, threshold_h)
            cv.InRangeS(s, 35, 255, threshold_s)
            cv.And(threshold_h, threshold_s, threshold_total)
            cv.And(threshold_total, threshold_g, threshold_total)
            cv.ShowImage("Filtered", threshold_total)

            cv.Smooth(threshold_total, threshold_total, cv.CV_BLUR, 11)
            cv.Threshold(threshold_total, threshold_total, 100, 255, cv.CV_THRESH_BINARY)
            cv.ShowImage("Threshold", threshold_total)


            r = cv.GetSubRect(threshold_total, (30, 30, img.width-30, img.height-30))
            do_edges = True
            if do_edges:
                try:
                    mem = cv.CreateMemStorage()
                    contours = cv.FindContours(r,mem,cv.CV_RETR_LIST)
                    if contours:
                        moments = cv.Moments(contours, 0)
                        area = cv.GetCentralMoment(moments, 0, 0)
                        if area > 10:
                            x = cv.GetSpatialMoment(moments, 1, 0)/area
                            y = cv.GetSpatialMoment(moments, 0, 1)/area
                            print('x:{0} y{1} area:{2}'.format(x,y,area))
                except:
                    raise

            do_box = False
            if do_box:
                cv.Canny(threshold_total, threshold_total, 25, 75)
                storage = cv.CreateMemStorage(0)
                obj = cv.FindContours(threshold_total, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
                aa = cv.ApproxPoly(obj, storage, cv.CV_POLY_APPROX_DP)
                print [a for a in aa]
                box = cv.BoundingRect(obj)
                #print((box[0]+(box[2]/2), box[1]+(box[3]/2)))
                cv.Rectangle(img, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]),(255,0,0),1,8,0)

            cv.ShowImage("Postprocessed", r)

            cv.ShowImage("Test", threshold_g)
        self.destroy()

    def destroy(self):
        cv.DestroyWindow("Image")
        cv.DestroyWindow("Filtered")
        cv.DestroyWindow("Threshold")
        cv.DestroyWindow("Postprocessed")
        cv.DestroyWindow("Test")
        del self.capture

if __name__=="__main__":
    color_tracker = BlobTracker()
    color_tracker.run2()
