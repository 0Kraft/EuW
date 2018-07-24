import cv2
import numpy as np
from subprocess import call
import time


def nothing(x):
    pass

class Point:
    """ Point class represents and manipulates x,y coords. """

    def __init__(self):
        """ Create a new point at the origin """
        self.x = 0
        self.y = 0

class C_Lines:
    """A simple example class"""
    degree=0
    L_Num=0
    L1 = Point()
    L2 = Point()
    LM = Point()
    

# Create a black image, a windowimg = cv2.imread('net.jpg')
def get_orientation():

    call(["raspistill", "-w", "480", "-h", "320", "-o", "cam.jpg"])

    time.sleep(3)


    img = cv2.imread('cam.jpg')
    
    crop_img = img[55:265, 1:479].copy() # Crop from x, y, w, h -> 100, 200, 300, 400
    gray = cv2.cvtColor(crop_img,cv2.COLOR_BGR2GRAY)
    cv2.imwrite( "Gray_Image.jpg", gray )
    blur = cv2.GaussianBlur(gray,(11,11),0)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(blur)
    high_thresh, thresh_im = cv2.threshold(blur, min_val+15,255,cv2.THRESH_BINARY_INV)
    cv2.imwrite( "thresh.jpg", thresh_im )
    #lowThresh = 0.8*high_thresh
   

    
    edges = cv2.Canny(gray,10,40,3)   #working
    #edges = cv2.Canny(thresh_im,10,40,3)   #working
    
   

    cv2.imwrite( "edges.jpg", edges )
  

    lines = cv2.HoughLines(edges,1,np.pi/180,50)
    

    counter = 0
    rho_all = 0
    course = 0
    
   
    if lines is not None:
        for rho,theta in lines[0]:
                        a = np.cos(theta)
                        b = np.sin(theta)
                        x0 = a*rho
                        y0 = b*rho
                        x1 = int(x0 + 1000*(-b))
                        y1 = int(y0 + 1000*(a))
                        x2 = int(x0 - 1000*(-b))
                        y2 = int(y0 - 1000*(a))

                        cv2.line(blur,(x1,y1),(x2,y2),(255,255,255),2)
                        if theta>((np.pi/4)*3) or theta<(np.pi/4):
                            counter=counter+1
                            rho_all=rho_all+theta
                            #cv2.putText(blur, str(theta) ,(10,30+counter*30), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2)
                            #cv2.putText(blur, str(rho) ,(400,30+counter*30), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2)            
                                           
                       

        rho_all=rho_all/counter          

        course=rho_all*(180/np.pi)
        
        if course>90:
            course=course-180

        cv2.putText(blur, str(course) ,(10,140), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2)

        cv2.imwrite( "final.jpg", blur )
    
    return course
    