import cv2
import numpy as np
img = cv2.imread('cam.png')

p_blur_last = 0


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


img = cv2.imread('cam.png')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
blur = cv2.bilateralFilter(gray,5,10,5)
edges = cv2.Canny(blur,50,150,3)






cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('Blur','image',1,30,nothing)
cv2.createTrackbar('Edges_LOW','image',1,200,nothing)
cv2.createTrackbar('Edges_HIGH','image',3,200,nothing)
cv2.createTrackbar('Threshold','image',30,500,nothing)

# create switch for ON/OFF functionality
switch = '0'
cv2.createTrackbar(switch, 'image',0,2,nothing)

while(1):
    s = cv2.getTrackbarPos(switch,'image')

    if s == 0:
        cv2.imshow('image',img)
    elif s == 1:
        cv2.imshow('image',edges)
    elif s == 2:
        cv2.imshow('image',blur)
  
  
        
   
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    # get current positions of four trackbars
    p_blur = cv2.getTrackbarPos('Blur','image')
    lowt = cv2.getTrackbarPos('Edges_LOW','image')
    hight = cv2.getTrackbarPos('Edges_HIGH','image')
    p_threshold = cv2.getTrackbarPos('Threshold','image')

    #if p_blur % 2 == 0:
     #   p_blur=p_blur+1
    
    img = cv2.imread('cam.png')
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    if p_blur!=p_blur_last:
        blur = cv2.bilateralFilter(gray,p_blur,p_blur,p_blur/2)
        p_blur_last=p_blur
    edges = cv2.Canny(blur,lowt,hight,3)

    
       

cv2.waitKey(0)
cv2.destroyAllWindows()
