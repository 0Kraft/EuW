from __future__ import division
import cv2
import numpy as np
from time import sleep
from numpy import array
from sklearn.cluster import KMeans
from picamera.array import PiRGBArray
from picamera import PiCamera
from fractions import Fraction
import jsonrpclib


server = jsonrpclib.Server('http://localhost:8080')


gui_mode=0

def nothing(x):
    pass

def init_gui():
    cv2.namedWindow('control')
    cv2.namedWindow('image')
    cv2.namedWindow('final')
    # create trackbars for color change
    cv2.createTrackbar('Blur','control',1,400,nothing)
    cv2.createTrackbar('Edges_LOW','control',1,200,nothing)
    cv2.createTrackbar('Edges_HIGH','control',160,300,nothing)
    cv2.createTrackbar('Threshold','control',90,255,nothing)

class Point:
    """ Point class represents and manipulates x,y coords. """

    def __init__(self,its_x,its_y):
        """ Create a new point at the origin """
        self.x = its_x
        self.y = its_y

class C_Line:
    """A simple example class"""
    def __init__(self,c_Num,c_theta,c_rho):
        self.its_rho=c_rho
        self.its_theta=c_theta
        self.degree=c_theta*(180/np.pi)
        if self.degree>90:
            self.degree=self.degree-180
            
        self.L_Num=c_Num
        self.a = np.cos(self.its_theta)
        self.b = np.sin(self.its_theta)
        self.x0 = self.a*c_rho
        self.y0 = self.b*c_rho
        self.x1 = int(self.x0 + 1000*(-self.b))
        self.y1 = int(self.y0 + 1000*(self.a))
        self.x2 = int(self.x0 - 1000*(-self.b))
        self.y2 = int(self.y0 - 1000*(self.a))
        self.L1 = Point(self.x1,self.y1)
        self.L2 = Point(self.x2,self.y2)

        div_x=self.x1-self.x2

        if(div_x)==0:
            div_x=div_x+.0001
            

        self.m = (self.y1-self.y2)/(div_x)
        self.mb = self.y1-(self.m*self.x1)

    def draw_line(self,i_mat,color):
        cv2.line(i_mat,(self.x1,self.y1),(self.x2,self.y2),color,2)

        x_circ = 200

        for i_x in range(0,800,5):
            y_circ = self.m * ((x_circ-400)+i_x) + self.mb
            cv2.circle(i_mat, (int((x_circ-400+i_x)),int(y_circ)), 10, color, thickness=2, lineType=8, shift=0) 


        print "Die Formel der Linie ist: y = " + str(self.m) + " X x + " + str(self.mb)

    def fusion(self, comp_line, i_mat):

        new_rho=(self.its_rho+comp_line.its_rho)/2
        new_theta=(self.its_theta+comp_line.its_theta)/2

        f_line = C_Line(0,new_theta,new_rho)
        return f_line

    def intersection(self, comp_line, i_mat):

        intersect_p=[]

        intersect_p.append((comp_line.mb-self.mb)/(self.m-comp_line.m))

        intersect_p.append(self.m * intersect_p[0] + self.mb)

        cv2.circle(i_mat, (int((intersect_p[0])),int(intersect_p[1])), 50, (255,255,255), thickness=2, lineType=8, shift=0) 

        return intersect_p
       
     


        

##        new_x1 = (self.x1+comp_line.x1)/2
##        new_x2 = (self.x2+comp_line.x2)/2
##        new_y1 = (self.y1+comp_line.y1)/2
##        new_y2 = (self.y2+comp_line.y2)/2
##
##        div_x=new_x1-new_x2
##
##        if(div_x)==0:
##            div_x=div_x+.0001
##            
##
##        new_m = (new_y1-new_y2)/(div_x)
##        new_mb = new_y1-(new_m*new_x1)
##        
##        x_circ = 200
##        for i_x in range(0,800,5):
##            y_circ = new_m * ((x_circ-400)+i_x) + new_mb
##            #cv2.circle(i_mat, (int((x_circ-400+i_x)),int(y_circ)), 20, (255,30,90), thickness=2, lineType=8, shift=0) 

        

       
        
       
def makephoto():
    server.send_cmd('switchir#1')
    camera = PiCamera()
    camera.close()
    camera = PiCamera()
    rawCapture = PiRGBArray(camera)
    camera.led = False
    w=800
    h=600
    camera.resolution = (w, h)
# Take a picture while the LED remains off
   
    sleep(.5)
       
    camera.iso = 200
   
    #camera.contrast=100
    
   # camera = PiCamera(resolution=(1280, 720), framerate=30)
    # Set ISO to the desired value
   
    # Wait for the automatic gain control to settle
    
    
    
    
    
    #sleep(4)
    # Now fix the values
    camera.shutter_speed = camera.exposure_speed
    s = camera.shutter_speed
    #if s<10000:
    #    camera.iso=600
    #ciso=camera.iso
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g
    
    
   
    camera.capture(rawCapture, format="bgr")
    
    res_img = rawCapture.array
    camera.close();
    cv2.imwrite("shot.jpg", res_img )
    server.send_cmd('switchir#0')
    return res_img;
        

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
                
                #if rho<0:
                #    rho=abs(rho)
                #    theta=theta-(np.pi) #normalize radians

                if np.pi-theta<0.3:
                    theta=theta-(np.pi) #normalize radians
                    rho = rho * (-1)

               
                
                dummy = C_Line(0,theta,rho)
                list_lines.append(dummy)
                data.insert(0,[theta,rho/300]) #normalize distances factor 300
 
    return cluster(data,lines,c_img)
  
def cluster(f_data, f_lines, c_img):
    
    global kmeans,img,list_lines, p_blur
    kmeans = KMeans(n_clusters=4,n_init=10, init="random", random_state=0, max_iter=300).fit(data)
    print kmeans.cluster_centers_

  

    resulting_line1 = C_Line(0,kmeans.cluster_centers_[0][0],kmeans.cluster_centers_[0][1]*300)
    resulting_line2 = C_Line(0,kmeans.cluster_centers_[1][0],kmeans.cluster_centers_[1][1]*300)
    resulting_line3 = C_Line(0,kmeans.cluster_centers_[2][0],kmeans.cluster_centers_[2][1]*300)
    resulting_line4 = C_Line(0,kmeans.cluster_centers_[3][0],kmeans.cluster_centers_[3][1]*300)

    
    

   
    
    img = c_img

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

     
       
       
    cv2.putText(img, str(kmeans.cluster_centers_[0]) ,(20,20), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),1)
    cv2.putText(img, str(kmeans.cluster_centers_[1]) ,(20,60), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,0),1)
    cv2.putText(img, str(kmeans.cluster_centers_[2]) ,(20,100), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),1)
    cv2.putText(img, str(kmeans.cluster_centers_[3]) ,(20,140), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),1)
    

    ## check for pairs
        
        
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

    print fin1
    print fin2
    print fin3
    print fin4

    winner=0
    winner2=0
    line_winner=[0,0]
    line_winner2=[0,0]

    if abs(abs(fin1)-abs(fin2))<20:
        global winner,winner2
        winner=(fin1+fin2)/2
        winner2=(fin3+fin4)/2
        line_winner=[(kmeans.cluster_centers_[0][0]+kmeans.cluster_centers_[1][0])/2,(kmeans.cluster_centers_[0][1]+kmeans.cluster_centers_[1][1])/2]
        line_winner2=[(kmeans.cluster_centers_[2][0]+kmeans.cluster_centers_[3][0])/2,(kmeans.cluster_centers_[2][1]+kmeans.cluster_centers_[3][1])/2]
        w_line1 = resulting_line1.fusion(resulting_line2,img)
        w_line2 = resulting_line3.fusion(resulting_line4,img)
 
    if abs(abs(fin1)-abs(fin3))<20:
        global winner,winner2
        winner=(fin1+fin3)/2
        winner2=(fin2+fin4)/2
        line_winner=[(kmeans.cluster_centers_[0][0]+kmeans.cluster_centers_[2][0])/2,(kmeans.cluster_centers_[0][1]+kmeans.cluster_centers_[2][1])/2]
        line_winner2=[(kmeans.cluster_centers_[1][0]+kmeans.cluster_centers_[3][0])/2,(kmeans.cluster_centers_[1][1]+kmeans.cluster_centers_[3][1])/2]
        w_line1 = resulting_line1.fusion(resulting_line3,img)
        w_line2 = resulting_line2.fusion(resulting_line4,img)
  
    if abs(abs(fin1)-abs(fin4))<20:
        global winner,winner2
        winner=(fin1+fin4)/2
        winner2=(fin3+fin2)/2
        line_winner=[(kmeans.cluster_centers_[0][0]+kmeans.cluster_centers_[3][0])/2,(kmeans.cluster_centers_[0][1]+kmeans.cluster_centers_[3][1])/2]
        line_winner2=[(kmeans.cluster_centers_[1][0]+kmeans.cluster_centers_[2][0])/2,(kmeans.cluster_centers_[1][1]+kmeans.cluster_centers_[2][1])/2]
        w_line1 = resulting_line1.fusion(resulting_line4,img)
        w_line2 = resulting_line3.fusion(resulting_line2,img)
  
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
    
    #w_line1.draw_line(img,(20,80,170))
    #w_line2.draw_line(img,(20,80,170))

    #distance = w_line1.intersection(w_line2,img)[1]

    distance = 0
    

    ## check for pairs

   

    result = []
    if(abs(winner)<abs(winner2)):
        result.append(winner)
        result.append(winner2)
    else:
        result.append(winner2)
        result.append(winner)
        
                      
   
    result.append(distance)
    cv2.imwrite("result.jpg", img )
    return result
    
     
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

# ## init ##
# img = cv2.imread('c1.jpg')
# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# mag = getGradientMagnitude(gray)
# ret,thresh = cv2.threshold(mag, 0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
# edges = cv2.Canny(thresh,75,180,3)
# lines = cv2.HoughLines(edges,3,np.pi/180,160)

# blur = cv2.bilateralFilter(gray,5,10,5)
# clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
# equ = clahe.apply(gray)
p_blur = 20

w, h = 800,600
img_lines_raw = np.zeros((w,h,3), np.uint8)
img_lines = cv2.cvtColor(img_lines_raw,cv2.COLOR_BGR2GRAY)
img_lines_fin = cv2.cvtColor(img_lines_raw,cv2.COLOR_BGR2GRAY)
img_bw = np.zeros((h,w,3), np.uint8)
hight=120
p_threshold=50
p_threshold_img=127

if gui_mode == 1:
    init_gui()

data=[]
list_lines=[]

##print "The course of EuW is: " + str(compute(img)[0])


    

if gui_mode == 1:
    cv2.imshow('image', render())
    cv2.imshow('final', img)
     
    
#img = cv2.imread('c1.jpg')
img_now= makephoto()
text = compute(img_now)
print "The course of EuW is: " + str(text[0]) + "     " + " with a crossing angle of: " + str(text[1])
print "Der Abstand betraegt: " + str(text[2])
print "-----------"
course=text[0]
while course>12.0 or course<-12.0:
                
                    if course>12.0:
                        server.send_cmd('turnadder+')
                    if course<12.0:
                        server.send_cmd('turnadder-')
                    
                    sleep(1)
                        
                    text = compute(img_now)
                    print "The course of EuW is: " + str(text[0]) + "     " + " with a crossing angle of: " + str(text[1])
                    print "Der Abstand betraegt: " + str(text[2])
                    print "-----------"
                    course=text[0]

