from __future__ import division
import cv2
import numpy as np
import imutils
from time import sleep
from numpy import array
from sklearn.cluster import KMeans

gui_mode=0

def nothing(x):
    pass



def init_gui():
    cv2.namedWindow('control')
    cv2.namedWindow('image')
    cv2.namedWindow('final')
    # create trackbars for color change
    cv2.createTrackbar('Blur','control',1,200,nothing)
    cv2.createTrackbar('Edges_LOW','control',1,200,nothing)
    cv2.createTrackbar('Edges_HIGH','control',120,300,nothing)
    cv2.createTrackbar('Threshold','control',90,255,nothing)

class Point:
    """ Point class represents and manipulates x,y coords. """

    def __init__(self,its_x,its_y):
        """ Create a new point at the origin """
        self.x = its_x
        self.y = its_y

class C_Line:
    """A simple example class"""
    def __init__(self,c_Num,c_rho,c_theta):
        self.its_rho=c_rho
        self.its_theta=c_theta
        self.degree=c_theta*(180/np.pi)
        if self.degree>90:
            self.degree=self.degree-180
            
        self.L_Num=c_Num
        a = np.cos(self.its_theta)
        b = np.sin(self.its_theta)
        x0 = a*c_rho
        y0 = b*c_rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
        self.L1 = Point(x1,y1)
        self.L2 = Point(x2,y2)
        

def getGradientMagnitude(im):
    "Get magnitude of gradient for given image"
    ddepth = cv2.CV_32F
    dx = cv2.Sobel(im, ddepth, 1, 0)
    dy = cv2.Sobel(im, ddepth, 0, 1)
    dxabs = cv2.convertScaleAbs(dx)
    dyabs = cv2.convertScaleAbs(dy)
    mag = cv2.addWeighted(dxabs, 0.5, dyabs, 0.5, 0)
    return mag
    
def compute(c_img):

    global data,ret,thresh,edges,lowt_last,hight_last,lines,img_lines,hight,lowt,p_threshold,img_lines_raw,dummy,list_lines,img

    
  
     # get current positions of four trackbars
    if gui_mode:
        p_blur = cv2.getTrackbarPos('Blur','control')
        lowt = cv2.getTrackbarPos('Edges_LOW','control')
        hight = cv2.getTrackbarPos('Edges_HIGH','control')
        p_threshold = cv2.getTrackbarPos('Threshold_Template','control')
        p_threshold_img = cv2.getTrackbarPos('Threshold','control')

    gray = cv2.cvtColor(c_img,cv2.COLOR_BGR2GRAY)
    mag = getGradientMagnitude(gray)
    ret,thresh = cv2.threshold(mag, 0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    edges = cv2.Canny(thresh,75,180,3)
    lines = cv2.HoughLines(edges,3,np.pi/180,hight)
    data = []
    list_lines = []
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
                
                if theta<0:
                    rho=abs(rho)
                    theta=theta+(np.pi) #normalize radians

                if theta>np.pi:
                    rho=abs(rho)
                    theta=theta-(np.pi) #normalize radians

               
                
                dummy = C_Line(0,rho,theta)
                list_lines.append(dummy)
                data.insert(0,[theta,rho/300]) #normalize distances factor 300
 
    return cluster(data,lines)
    
def render_line(c_img,c_rho,c_theta,c_color):
    a = np.cos(c_theta)
    b = np.sin(c_theta)
    x0 = a*c_rho
    y0 = b*c_rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    cv2.line(c_img,(x1,y1),(x2,y2),c_color,2)
    return c_img
    
  
def cluster(f_data, f_lines):
    
    global kmeans,img,list_lines
    kmeans = KMeans(n_clusters=4,n_init=10, init="random", random_state=0, max_iter=300).fit(data)
    print kmeans.cluster_centers_
    img = cv2.imread('c1.jpg')

    for l_i in range(0,len(list_lines)):
        ta = np.cos(list_lines[l_i].its_theta)
        tb = np.sin(list_lines[l_i].its_theta)
        tx0 = ta*list_lines[l_i].its_rho
        ty0 = tb*list_lines[l_i].its_rho
        tx1 = int(tx0 + 1000*(-tb))
        ty1 = int(ty0 + 1000*(ta))
        tx2 = int(tx0 - 1000*(-tb))
        ty2 = int(ty0 - 1000*(ta))

        #print str(list_lines[l_i].its_rho) + " " + str(list_lines[l_i].its_theta)

        group= kmeans.predict([[list_lines[l_i].its_theta,list_lines[l_i].its_rho/300]])
                  
        color=(0,0,0)
        if group == 0:
            color = (255,0,0)
            
        if group == 1:
            color = (255,255,0)
        if group == 2:
            color = (0,255,0)
        if group == 3:
            color = (0,0,255)
        
        #if textcount<550:
            #cv2.putText(img, str(list_lines[l_i].its_theta) + "  /  " + str(list_lines[l_i].its_rho) ,(20,textcount), cv2.FONT_HERSHEY_SIMPLEX, 1,color,2)

        cv2.line(img,(tx1,ty1),(tx2,ty2),color,2)
        
    fin1 = kmeans.cluster_centers_[0][0]*(180/np.pi)
    fin2 = kmeans.cluster_centers_[1][0]*(180/np.pi)
    fin3 = kmeans.cluster_centers_[2][0]*(180/np.pi)
    fin4 = kmeans.cluster_centers_[3][0]*(180/np.pi)

    print fin1
    print fin2
    print fin3
    print fin4

    if fin1>90:
        fin1=fin1-180
    if fin2>90:
        fin2=fin2-180
    if fin3>90:
        fin3=fin3-180
    if fin4>90:
        fin4=fin4-180

    winner=0
    winner2=0
    line_winner=[0,0]
    line_winner2=[0,0]

    if abs(fin1-fin2)<20:
        global winner,winner2
        winner=(fin1+fin2)/2
        winner2=(fin3+fin4)/2
        line_winner=[(kmeans.cluster_centers_[0][0]+kmeans.cluster_centers_[1][0])/2,(kmeans.cluster_centers_[0][1]+kmeans.cluster_centers_[1][1])/2]
        line_winner2=[(kmeans.cluster_centers_[2][0]+kmeans.cluster_centers_[3][0])/2,(kmeans.cluster_centers_[2][1]+kmeans.cluster_centers_[3][1])/2]
 
    if abs(fin1-fin3)<20:
        global winner,winner2
        winner=(fin1+fin3)/2
        winner2=(fin2+fin4)/2
        line_winner=[(kmeans.cluster_centers_[0][0]+kmeans.cluster_centers_[2][0])/2,(kmeans.cluster_centers_[0][1]+kmeans.cluster_centers_[2][1])/2]
        line_winner2=[(kmeans.cluster_centers_[1][0]+kmeans.cluster_centers_[3][0])/2,(kmeans.cluster_centers_[1][1]+kmeans.cluster_centers_[3][1])/2]
  
    if abs(fin1-fin4)<20:
        global winner,winner2
        winner=(fin1+fin4)/2
        winner2=(fin3+fin2)/2
        line_winner=[(kmeans.cluster_centers_[0][0]+kmeans.cluster_centers_[3][0])/2,(kmeans.cluster_centers_[0][1]+kmeans.cluster_centers_[3][1])/2]
        line_winner2=[(kmeans.cluster_centers_[1][0]+kmeans.cluster_centers_[2][0])/2,(kmeans.cluster_centers_[1][1]+kmeans.cluster_centers_[2][1])/2]
  
    cv2.putText(img_lines_fin, str(winner),(20,20), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)
    cv2.putText(img_lines_fin, str(winner2),(20,60), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)

    ta = np.cos(line_winner[0])
    tb = np.sin(line_winner[0])
    tx0 = ta*(line_winner[1]*300)
    ty0 = tb*(line_winner[1]*300)
    tx1 = int(tx0 + 1000*(-tb))
    ty1 = int(ty0 + 1000*(ta))
    tx2 = int(tx0 - 1000*(-tb))
    ty2 = int(ty0 - 1000*(ta))
       
    cv2.line(img,(tx1,ty1),(tx2,ty2),(0,255,255),2)

    ta = np.cos(winner2/((180/np.pi)))
    tb = np.sin(winner2/((180/np.pi)))
    tx0 = ta*(line_winner2[1]*300)
    ty0 = tb*(line_winner2[1]*300)
    tx1 = int(tx0 + 1000*(-tb))
    ty1 = int(ty0 + 1000*(ta))
    tx2 = int(tx0 - 1000*(-tb))
    ty2 = int(ty0 - 1000*(ta))
       
    cv2.line(img,(tx1,ty1),(tx2,ty2),(0,255,255),2)

    distance = 20; # look for seg_intersect!!

    result = []
    result.append(winner2)
    result.append(winner)
    result.sort()
    result.append(distance)
    return result
    
     
def render():
    global gray,thresh,mag,edges,img_lines,img_lines_fin,blur


    img_lines_fin = render_line(img_lines_fin,30,2.14,(120,120,120))
    img_lines_fin = render_line(img_lines_fin,-40,2.14+(3.14),(80,80,80))
    img_lines_fin = render_line(img_lines_fin,-20,2.14-(3.14),(255,255,255))
    
        
    img_lines_fin = render_line(img_lines_fin,140,0.1,(255,255,255))
      



    img_small = cv2.resize(gray, (0, 0), None, .25, .25)
    blur_small = cv2.resize(blur, (0, 0), None, .25, .25)
    edges_small = cv2.resize(edges, (0, 0), None, .25, .25)
    lines_small = cv2.resize(img_lines, (0, 0), None, .25, .25)
    thresh_small = cv2.resize(thresh, (0, 0), None, .25, .25)
    mag_small = cv2.resize(mag, (0, 0), None, .25, .25)
    img_lines_fin_small = cv2.resize(img_lines_fin, (0, 0), None, .25, .25)
    numpy_horizontal = np.hstack((img_small,mag_small,thresh_small))
    numpy_horizontal2 = np.hstack((thresh_small,img_lines_fin_small,lines_small))
    numpy_complete = np.vstack([numpy_horizontal,numpy_horizontal2])
    return numpy_complete

## init ##
img = cv2.imread('c1.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
mag = getGradientMagnitude(gray)
ret,thresh = cv2.threshold(mag, 0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
edges = cv2.Canny(thresh,75,180,3)
lines = cv2.HoughLines(edges,3,np.pi/180,160)

blur = cv2.bilateralFilter(gray,5,10,5)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
equ = clahe.apply(gray)

w, h = img.shape[:2]
img_lines_raw = np.zeros((w,h,3), np.uint8)
img_lines = cv2.cvtColor(img_lines_raw,cv2.COLOR_BGR2GRAY)
img_lines_fin = cv2.cvtColor(img_lines_raw,cv2.COLOR_BGR2GRAY)
img_bw = np.zeros((h,w,3), np.uint8)
hight=120
p_threshold=50
p_threshold_img=127

def get_course():
    img = cv2.imread('c1.jpg')
    return compute(img)[0]
    

if gui_mode == 1:
    init_gui()

data=[]
list_lines=[]

##print "The course of EuW is: " + str(compute(img)[0])
##
##while(1):
##    global numpy_complete
##
##    if gui_mode == 1:
##        cv2.imshow('image', render())
##        cv2.imshow('final', img)
##     
##    k = cv2.waitKey(1) & 0xFF
##    if k == 27:
##        break
##    if k == 13:
##        img = cv2.imread('c1.jpg')
##        text = str(compute(img)[0])
##        print "The course of EuW is: " + text
  

cv2.waitKey(0)
cv2.destroyAllWindows()
