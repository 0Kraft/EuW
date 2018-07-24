from __future__ import division
import cv2
import numpy as np
import imutils
from time import sleep


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

def drawMatches(img1, kp1, img2, kp2, matches):
    """
    My own implementation of cv2.drawMatches as OpenCV 2.4.9
    does not have this function available but it's supported in
    OpenCV 3.0.0

    This function takes in two images with their associated 
    keypoints, as well as a list of DMatch data structure (matches) 
    that contains which keypoints matched in which images.

    An image will be produced where a montage is shown with
    the first image followed by the second image beside it.

    Keypoints are delineated with circles, while lines are connected
    between matching keypoints.

    img1,img2 - Grayscale images
    kp1,kp2 - Detected list of keypoints through any of the OpenCV keypoint 
              detection algorithms
    matches - A list of matches of corresponding keypoints through any
              OpenCV keypoint matching algorithm
    """

    # Create a new output image that concatenates the two images together
    # (a.k.a) a montage
    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1]

    # Create the output image
    # The rows of the output are the largest between the two images
    # and the columns are simply the sum of the two together
    # The intent is to make this a colour image, so make this 3 channels
    out = np.zeros((max([rows1,rows2]),cols1+cols2,3), dtype='uint8')

    # Place the first image to the left
    out[:rows1,:cols1] = np.dstack([img1, img1, img1])

    # Place the next image to the right of it
    out[:rows2,cols1:] = np.dstack([img2, img2, img2])

    # For each pair of points we have between both images
    # draw circles, then connect a line between them
    for mat in matches:

        # Get the matching keypoints for each of the images
        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx

        # x - columns
        # y - rows
        (x1,y1) = kp1[img1_idx].pt
        (x2,y2) = kp2[img2_idx].pt

        # Draw a small circle at both co-ordinates
        # radius 4
        # colour blue
        # thickness = 1
        cv2.circle(out, (int(x1),int(y1)), 4, (255, 0, 0), 1)   
        cv2.circle(out, (int(x2)+cols1,int(y2)), 4, (255, 0, 0), 1)

        # Draw a line in between the two points
        # thickness = 1
        # colour blue
        cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), (255,0,0), 1)


    # Show the image
    cv2.imshow('Matched Features', out)
    cv2.waitKey(0)
    cv2.destroyWindow('Matched Features')

    # Also return the image if you'd like a copy
    return out



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
        print str(i)
        #img_big = cv2.resize(template, (0, 0), None, 10, 10)
        #cv2.imshow('image2', img_big)
        
        
       
    
    


    
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
   
  

    numpy_horizontal = np.hstack((img_small,blur_small,thresh_small,edges_small,lines_small))

   
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
