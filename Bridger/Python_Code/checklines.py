import cv2
import numpy as np
img = cv2.imread('net.jpg')

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


img = cv2.imread('net.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(25,25),0)
edges = cv2.Canny(blur,50,150,apertureSize = 3)

lines = cv2.HoughLines(edges,1,np.pi/180,300)
for rho,theta in lines[0]:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))

                cv2.line(blur,(x1,y1),(x2,y2),(0,0,255),2)



cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('Blur','image',1,30,nothing)
cv2.createTrackbar('Edges','image',3,10,nothing)
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
    p_edges = cv2.getTrackbarPos('Edges','image')
    p_threshold = cv2.getTrackbarPos('Threshold','image')

    if p_blur % 2 == 0:
        p_blur=p_blur+1
    
    img = cv2.imread('net.jpg')
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(p_blur,p_blur),0)
    edges = cv2.Canny(blur,50,150,apertureSize = p_edges)

    lines = cv2.HoughLines(edges,1,np.pi/180,p_threshold)

    for rho,theta in lines[0]:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))

                cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)  
       
    for rho,theta in lines[0]:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))

                cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)  


       

cv2.waitKey(0)
cv2.destroyAllWindows()
