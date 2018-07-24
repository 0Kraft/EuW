from __future__ import division
import cv2
import numpy as np
import imutils
from time import sleep
import matplotlib.pyplot as plt
from numpy import array



img = cv2.imread('c1.jpg')
img2 = cv2.imread('c1.jpg')
img_rgb = cv2.imread('c1.jpg')
img_gray = cv2.imread('c1.jpg')
img_bw = np.zeros((600,800,3), np.uint8)
img_lines_raw = np.zeros((600,800,3), np.uint8)
img_lines = cv2.cvtColor(img_lines_raw,cv2.COLOR_BGR2GRAY)


p_blur_last = 0
lowt_last=0
hight_last=0
p_threshold_last=0
p_threshold=50
p_threshold_img=127
p_threshold_img_last=255

def getGradientMagnitude(im):
    "Get magnitude of gradient for given image"
    ddepth = cv2.CV_32F
    dx = cv2.Sobel(im, ddepth, 1, 0)
    dy = cv2.Sobel(im, ddepth, 0, 1)
    dxabs = cv2.convertScaleAbs(dx)
    dyabs = cv2.convertScaleAbs(dy)
    mag = cv2.addWeighted(dxabs, 0.5, dyabs, 0.5, 0)
    return mag



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
    
img = cv2.imread('c1.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    

# Create a black image, a windowimg = cv2.imread('net.jpg')
def match():
    global img_rgb
    global p_threshold
    global img_bw
    img_rgb = cv2.imread('c1.jpg')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    img_rgb2 = cv2.imread('feature.jpg')
    template_g = cv2.cvtColor(img_rgb2, cv2.COLOR_BGR2GRAY)
    img_bw = np.zeros((600,800,3), np.uint8)

    plot_x = []
    plot_y = []
    
    for i in range(0,360,15):
       
        template_r = imutils.rotate(template_g, i)
        template = template_r[15:40,15:40]
        
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        threshold = p_threshold/100
        loc = np.where( res >= p_threshold/100)
        
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
            cv2.circle(img_bw, pt, 20, (255,255,255), -1)
            plot_x.append(pt[0])
            plot_y.append(pt[1])
            
        print str(i)
        #img_big = cv2.resize(template, (0, 0), None, 10, 10)
        #cv2.imshow('image2', img_big)

    m, b = np.polyfit(plot_x, plot_y, 1)

    n_x = array( plot_x )
    n_y = array( plot_y )


    plt.plot(n_x,n_y , '.')
    plt.plot(n_x, m*n_x + b, '-')
    plt.show()
        
        
       
    
    


    
img = cv2.imread('c1.jpg')
gray = cv2.cvtColor(img_bw,cv2.COLOR_BGR2GRAY)
blur = cv2.bilateralFilter(gray,5,10,5)

clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
equ = clahe.apply(gray)


#diff = cv2.absdiff(gray,gray2)
#blur2 = cv2.GaussianBlur(diff,(15,15),0)
ret,thresh = cv2.threshold(blur, 6,255,cv2.THRESH_BINARY_INV)
edges = cv2.Canny(thresh,50,150,3)



cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('Blur','image',1,200,nothing)
cv2.createTrackbar('Edges_LOW','image',51,200,nothing)
cv2.createTrackbar('Edges_HIGH','image',107,200,nothing)
cv2.createTrackbar('Threshold','image',126,255,nothing)
cv2.createTrackbar('Threshold_Template','image',55,100,nothing)

# create switch for ON/OFF functionality
switch = '0'

#cv2.createTrackbar(switch, 'image',0,3,nothing)

while(1):
    s = cv2.getTrackbarPos(switch,'image')

##    if s == 0:
##        cv2.imshow('image',img)
##    elif s == 1:
##        cv2.imshow('image',edges)
##    elif s == 2:
##        cv2.imshow('image',blur)
##    elif s == 3:
##        cv2.imshow('image',thresh2)

    img_small = cv2.resize(gray, (0, 0), None, .25, .25)
    blur_small = cv2.resize(blur, (0, 0), None, .25, .25)
    edges_small = cv2.resize(edges, (0, 0), None, .25, .25)
 
    lines_small = cv2.resize(img_lines, (0, 0), None, .25, .25)
    thresh_small = cv2.resize(thresh, (0, 0), None, .25, .25)

    mag = getGradientMagnitude(gray)
    mag_small = cv2.resize(mag, (0, 0), None, .25, .25)


    
   
  

    numpy_horizontal = np.hstack((img_small,mag_small,thresh_small,edges_small,lines_small))

   
   # numpy_horizontal_concat = np.concatenate((img_small,blur_small,thresh_small,edges_small), axis=1)

   
    cv2.imshow('image', numpy_horizontal)
    #cv2.imshow('image2', img_bw)
   
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    # get current positions of four trackbars
    p_blur = cv2.getTrackbarPos('Blur','image')
    lowt = cv2.getTrackbarPos('Edges_LOW','image')
    hight = cv2.getTrackbarPos('Edges_HIGH','image')
    p_threshold = cv2.getTrackbarPos('Threshold_Template','image')
    p_threshold_img = cv2.getTrackbarPos('Threshold','image')

    #if p_blur % 2 == 0:
     #   p_blur=p_blur+1
    
    img = cv2.imread('c1.jpg')
    gray = cv2.cvtColor(img_bw,cv2.COLOR_BGR2GRAY)
    if p_blur!=p_blur_last:
        #blur = cv2.bilateralFilter(gray,p_blur,p_blur,p_blur/2)
        if p_blur % 2 == 0:
            p_blur=p_blur+1
        blur = cv2.GaussianBlur(gray,(p_blur,p_blur),0)
        equ = clahe.apply(blur)
        p_blur_last=p_blur
    if p_threshold!=p_threshold_last:
        #ret,thresh = cv2.threshold(blur, p_threshold,20,cv2.THRESH_BINARY_INV)
        match()
        p_threshold_last=p_threshold
    
        
    if lowt!=lowt_last or hight!=hight_last:
        edges = cv2.Canny(thresh,lowt,hight,3)
        lowt_last=lowt
        hight_last=hight
    

    

   
    if p_threshold_img!=p_threshold_img_last:
        ret,thresh = cv2.threshold(blur, p_threshold_img,255,cv2.THRESH_BINARY)
        p_threshold_img_last=p_threshold_img
        edges = cv2.Canny(thresh,75,180,3)
        lowt_last=lowt
        hight_last=hight
        lines = cv2.HoughLines(edges,lowt,np.pi/180,hight)
        img_lines_raw = np.zeros((600,800,3), np.uint8)
        img_lines = cv2.cvtColor(img_lines_raw,cv2.COLOR_BGR2GRAY)
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
                    cv2.line(img_lines,(x1,y1),(x2,y2),(255,255,255),2)
                       
    

    
       

cv2.waitKey(0)
cv2.destroyAllWindows()
