from __future__ import division
import cv2
import numpy as np
import imutils
from time import sleep
from numpy import array
from sklearn.cluster import KMeans

data=[]
list_lines=[]
rotation=0
hight=120

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


## init ##
img = cv2.imread('c1.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
mag = getGradientMagnitude(gray)
ret,thresh = cv2.threshold(mag, 0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
edges = cv2.Canny(thresh,75,180,3)
lines = cv2.HoughLines(edges,3,np.pi/180,hight)
w, h = img.shape[:2]
img_lines_raw = np.zeros((w,h,3), np.uint8)
img_lines = cv2.cvtColor(img_lines_raw,cv2.COLOR_BGR2GRAY)
img_lines_fin = cv2.cvtColor(img_lines_raw,cv2.COLOR_BGR2GRAY)
img_bw = np.zeros((h,w,3), np.uint8)
hight=120
p_blur_last = 0
lowt_last=0
hight_last=0
p_threshold_last=0
p_threshold=50
p_threshold_img=127
p_threshold_img_last=255





def nothing(x):
    pass

    
def compute():

    global data,gray,ret,thresh,edges,lowt_last,hight_last,lines,img_lines,hight,lowt,p_threshold,img_lines_raw,dummy,list_lines,img
    
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
                
                if rho<0:
                    rho=abs(rho)
                    theta=theta-(np.pi) #normalize radians
                
                dummy = C_Line(0,rho,theta)
                list_lines.append(dummy)
                data.insert(0,[theta,rho/300])#normalize distances factor 300
         
                                
    cluster(data,lines)
  
def cluster(f_data, f_lines):
    global img_lines_fin,img_lines_raw,kmeans,img,list_lines
    img_lines_fin = cv2.cvtColor(img_lines_raw,cv2.COLOR_BGR2GRAY)
    kmeans = KMeans(n_clusters=4,n_init=10, init="random", random_state=0, max_iter=300).fit(data)
    print kmeans.cluster_centers_
    img = cv2.imread('c1.jpg')
    print len(list_lines)
    textcount=20
    
##    for l_i in range(0,len(list_lines)):
##        ta = np.cos(list_lines[l_i].its_theta)
##        tb = np.sin(list_lines[l_i].its_theta)
##        tx0 = ta*list_lines[l_i].its_rho
##        ty0 = tb*list_lines[l_i].its_rho
##        tx1 = int(tx0 + 1000*(-tb))
##        ty1 = int(ty0 + 1000*(ta))
##        tx2 = int(tx0 - 1000*(-tb))
##        ty2 = int(ty0 - 1000*(ta))
##
##        group= kmeans.predict([[list_lines[l_i].its_theta,list_lines[l_i].its_rho/300]])
##                  
##        color=(0,0,0)
##        if group == 0:
##            color = (255,0,0)
##        if group == 1:
##            color = (255,255,0)
##        if group == 2:
##            color = (0,255,0)
##        if group == 3:
##            color = (0,0,255)
##        
##        #if textcount<550:
##            #cv2.putText(img, str(list_lines[l_i].its_theta) + "  /  " + str(list_lines[l_i].its_rho) ,(20,textcount), cv2.FONT_HERSHEY_SIMPLEX, 1,color,2)
##
##        #cv2.line(img,(tx1,ty1),(tx2,ty2),color,2)

        
        
##    for c_i in range(0,4):
##        
##        ta = np.cos(kmeans.cluster_centers_[c_i][0])
##        tb = np.sin(kmeans.cluster_centers_[c_i][0])
##        tx0 = ta*(kmeans.cluster_centers_[c_i][1]*300)
##        ty0 = tb*(kmeans.cluster_centers_[c_i][1]*300)
##        tx1 = int(tx0 + 1000*(-tb))
##        ty1 = int(ty0 + 1000*(ta))
##        tx2 = int(tx0 - 1000*(-tb))
##        ty2 = int(ty0 - 1000*(ta))
##    
##        color=(0,0,0)
##        if c_i == 0:
##            color = (255,0,0)
##        if c_i == 1:
##            color = (255,255,0)
##        if c_i == 2:
##            color = (0,255,0)
##        if c_i == 3:
##            color = (0,0,255)
##        cv2.line(img,(tx1,ty1),(tx2,ty2),color,2)

    fin1 = kmeans.cluster_centers_[0][0]*(180/np.pi)
    fin2 = kmeans.cluster_centers_[1][0]*(180/np.pi)
    fin3 = kmeans.cluster_centers_[2][0]*(180/np.pi)
    fin4 = kmeans.cluster_centers_[3][0]*(180/np.pi)

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
       
    cv2.line(img,(tx1,ty1),(tx2,ty2),(0,255,0),2)

    ta = np.cos(winner2/((180/np.pi)))
    tb = np.sin(winner2/((180/np.pi)))
    tx0 = ta*(line_winner2[1]*300)
    ty0 = tb*(line_winner2[1]*300)
    tx1 = int(tx0 + 1000*(-tb))
    ty1 = int(ty0 + 1000*(ta))
    tx2 = int(tx0 - 1000*(-tb))
    ty2 = int(ty0 - 1000*(ta))
       
    cv2.line(img,(tx1,ty1),(tx2,ty2),(0,255,0),2)
 
            
    
    
##    ta = np.cos(kmeans.cluster_centers_[0][0])
##    tb = np.sin(kmeans.cluster_centers_[0][0])
##    tx0 = ta*kmeans.cluster_centers_[0][1]
##    ty0 = tb*kmeans.cluster_centers_[0][1]
##    tx1 = int(tx0 + 1000*(-tb))
##    ty1 = int(ty0 + 1000*(ta))
##    tx2 = int(tx0 - 1000*(-tb))
##    ty2 = int(ty0 - 1000*(ta))
##    cv2.putText(img_lines_fin, str(kmeans.cluster_centers_[0][0]*(180/np.pi)) ,(20,20), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)
##    cv2.line(img_lines_fin,(tx1,ty1),(tx2,ty2),(255,0,0),2)
##    ta = np.cos(kmeans.cluster_centers_[1][0])
##    tb = np.sin(kmeans.cluster_centers_[1][0])
##    tx0 = ta*kmeans.cluster_centers_[1][1]
##    ty0 = tb*kmeans.cluster_centers_[1][1]
##    tx1 = int(tx0 + 1000*(-tb))
##    ty1 = int(ty0 + 1000*(ta))
##    tx2 = int(tx0 - 1000*(-tb))
##    ty2 = int(ty0 - 1000*(ta))
##    cv2.line(img_lines_fin,(tx1,ty1),(tx2,ty2),(255,0,255),2)
##    cv2.putText(img_lines_fin, str(kmeans.cluster_centers_[1][0]*(180/np.pi)) ,(20,60), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)

    
    
##    for rho,theta in f_lines[0]:
##                        
##                        a = np.cos(theta)
##                        b = np.sin(theta)
##                        x0 = a*rho
##                        y0 = b*rho
##                        x1 = int(x0 + 1000*(-b))
##                        y1 = int(y0 + 1000*(a))
##                        x2 = int(x0 - 1000*(-b))
##                        y2 = int(y0 - 1000*(a))
##                                                
##                        
##                        if (kmeans.predict([[theta,rho]]))==0:
##                            cv2.line(img_lines_fin,(x1,y1),(x2,y2),(255,255,255),2)
##                        else:
##                            cv2.line(img_lines_fin,(x1,y1),(x2,y2),(0,0,50),2)
   
def render():
    global gray,thresh,mag,edges,img_lines,img_lines_fin
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


    #plt.plot(n_x,n_y , '.')
    #plt.plot(n_x, m*n_x + b, '-')
    #plt.show()
        
        
       
    
    


    


blur = cv2.bilateralFilter(gray,5,10,5)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
equ = clahe.apply(gray)
#diff = cv2.absdiff(gray,gray2)
#blur2 = cv2.GaussianBlur(diff,(15,15),0)
ret,thresh = cv2.threshold(blur, 6,255,cv2.THRESH_BINARY_INV)
edges = cv2.Canny(thresh,50,150,3)

cv2.namedWindow('control')
cv2.namedWindow('image')
cv2.namedWindow('final')

# create trackbars for color change
cv2.createTrackbar('Blur','control',1,200,nothing)
cv2.createTrackbar('Edges_LOW','control',1,200,nothing)
cv2.createTrackbar('Edges_HIGH','control',120,300,nothing)
cv2.createTrackbar('Threshold','control',90,255,nothing)
#cv2.createTrackbar('Threshold_Template','image',55,100,nothing)

# create switch for ON/OFF functionality
switch = '0'

#cv2.createTrackbar(switch, 'image',0,3,nothing)

while(1):
    global numpy_complete
#    s = cv2.getTrackbarPos(switch,'image')

##    if s == 0:
##        cv2.imshow('image',img)
##    elif s == 1:
##        cv2.imshow('image',edges)
##    elif s == 2:
##        cv2.imshow('image',blur)
##    elif s == 3:
##        cv2.imshow('image',thresh2)

   
    cv2.imshow('image', render())
    cv2.imshow('final', img)
     
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
    if k == 13:
        compute()
       
    
    

    # get current positions of four trackbars
    p_blur = cv2.getTrackbarPos('Blur','control')
    lowt = cv2.getTrackbarPos('Edges_LOW','control')
    hight = cv2.getTrackbarPos('Edges_HIGH','control')
    p_threshold = cv2.getTrackbarPos('Threshold_Template','control')
    p_threshold_img = cv2.getTrackbarPos('Threshold','control')
  
   
  
       

cv2.waitKey(0)
cv2.destroyAllWindows()
