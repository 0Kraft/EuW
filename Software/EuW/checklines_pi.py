import cv2
import numpy as np
from cluster import HierarchicalClustering
from cluster import KMeansClustering
from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.datasets.samples_generator import make_blobs
from subprocess import call
import time
import RPi.GPIO as GPIO
from numpy  import array
from sklearn.preprocessing import StandardScaler
from picamera.array import PiRGBArray
from picamera import PiCamera
from fractions import Fraction
from sklearn.cluster import KMeans


import HTML
import datetime






# Schreiben

 
# initialize the camera and grab a reference to the raw camera capture



GPIO.setmode(GPIO.BCM)

CAMLED = 40 
 
# Set GPIO to output
GPIO.setup(CAMLED, GPIO.OUT, initial=False) 


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
    
def get_cv():

    global w
    global h

    # for i in range(5):
        # GPIO.output(CAMLED,True) # On
        # time.sleep(0.5)
        # GPIO.output(CAMLED,False) # Off
        # time.sleep(0.5)
        
    camera = PiCamera()
    camera.close()
    camera = PiCamera()
    rawCapture = PiRGBArray(camera)
    rawCapture2 = PiRGBArray(camera)

# Turn the camera's LED off
    camera.led = False
    w=800
    h=600
    camera.resolution = (w, h)
# Take a picture while the LED remains off
   
    time.sleep(.2)
   
    
    camera.iso = 200
   
    #camera.contrast=100
    
   # camera = PiCamera(resolution=(1280, 720), framerate=30)
    # Set ISO to the desired value
   
    # Wait for the automatic gain control to settle
    time.sleep(4)
    # Now fix the values
    camera.shutter_speed = camera.exposure_speed
    s = camera.shutter_speed
    if s<10000:
        camera.iso=600
    ciso=camera.iso
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g
    # Finally, take several photos with the fixed settings
    #camera.capture_sequence(['image%02d.jpg' % i for i in range(10)])
    camera.capture(rawCapture, format="bgr")
    
   # picam_01 = rawCapture.array
    picam_01 = cv2.imread('shot1.jpg',0)
    
    time.sleep(1)
    
       
    GPIO.output(CAMLED,True) # On
    time.sleep(1)
    
    camera.capture(rawCapture2, format="bgr")
    
    picam_02 = cv2.imread('shot2.jpg',0)
   # picam_02 = rawCapture2.array
    
    
    
    #camera.capture(rawCapture, format="bgr")
    #picam_01 = rawCapture.array
    #time.sleep(.1)
    #GPIO.output(CAMLED,True) # On
    #time.sleep(10)
    #GPIO.output(CAMLED,True) # On
    #camera.capture(rawCapture2, format="bgr")
    #picam_02 = rawCapture2.array
    time.sleep(2)
    GPIO.output(CAMLED,False) # Off
      
    
        
    crop_img = picam_02[(h/5.33):(h/1.23), (w/24):(w/1.04)].copy() # Crop from x, y, w, h -> 100, 200, 300, 400
    
    crop_img2 = picam_01[(h/5.33):(h/1.23), (w/24):(w/1.04)].copy() # Crop from x, y, w, h -> 100, 200, 300, 400
    
   
    #gray = cv2.cvtColor(crop_img,cv2.COLOR_BGR2GRAY)
    #gray2 = cv2.cvtColor(crop_img2,cv2.COLOR_BGR2GRAY)
  
    cv2.imwrite( "g1.jpg", crop_img )
    cv2.imwrite( "g2.jpg", crop_img2 )
    
    diff = cv2.absdiff(crop_img,crop_img2)
    
    
    camera.close();
    
    # CLAHE (Contrast Limited Adaptive Histogram Equalization)
    
    clahe = cv2.createCLAHE(clipLimit=3., tileGridSize=(8,8))
    lab = cv2.cvtColor(diff, cv2.COLOR_BGR2LAB)  # convert from BGR to LAB color space
    l, a, b = cv2.split(lab)  # split on 3 different channels
    l2 = clahe.apply(l)  # apply CLAHE to the L-channel
    lab = cv2.merge((l2,a,b))  # merge channels
    img2 = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)  # convert from LAB to BGR
    cv2.imwrite('sunset_modified.jpg', img2)
    
    gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    
    #blur2 = cv2.GaussianBlur(diff,(15,15),0)
    
    #ret,thresh2 = cv2.threshold(blur2, 6,255,cv2.THRESH_BINARY_INV)
    
    #cv2.imwrite( "gray.jpg", gray )
    
    #blur = cv2.bilateralFilter(gray,6,12,3)
    img_hsv=cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0,20,20])
    upper_red = np.array([20,255,255])
    mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

# upper mask (170-180)
    lower_red = np.array([160,20,20])
    upper_red = np.array([180,255,255])
    mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

# join my masks
    mask = mask0+mask1
    
    cv2.imwrite( "mask.jpg", mask)

    
    blur = cv2.GaussianBlur(mask,(15,15),4)
    
    ret3,th3 = cv2.threshold(blur,20,255,cv2.THRESH_BINARY_INV)
    cv2.imwrite( "blur.jpg", blur )
        
    edges = cv2.Canny(blur,8,24,3)   #working
    cv2.imwrite( "edges.jpg", edges )

    cv2.imwrite( "diff.jpg", diff )
    
     
    lines = cv2.HoughLines(edges,1,np.pi/180,50)
    
    data=[]
    

    counter = 0
    rho_all = 0
    course = 200
    overlay = crop_img.copy()
    overlay2 = crop_img.copy()
   
    if lines is not None:
        for rho,theta in lines[0]:
                        course=0
                        a = np.cos(theta)
                        b = np.sin(theta)
                        x0 = a*rho
                        y0 = b*rho
                        x1 = int(x0 + 1000*(-b))
                        y1 = int(y0 + 1000*(a))
                        x2 = int(x0 - 1000*(-b))
                        y2 = int(y0 - 1000*(a))
                        #data.insert(0,[rho,theta])
                        data.insert(0,[theta,rho])
                        if theta>((np.pi/4)*3) or theta<(np.pi/4):
                            counter=counter+1
                            #cv2.line(crop_img,(x1,y1),(x2,y2),(0,255,10),2)
                            temp=theta*(180/np.pi)
                            if temp>90:
                                temp=temp-180
                            #data.insert(0,[theta,rho])
                             
                            rho_all=rho_all+temp
                            
                            # if counter < 10:
                                # cv2.putText(crop_img, str(theta) ,(10,73+counter*30), cv2.FONT_HERSHEY_SIMPLEX, .4,(0,0,255),2)
                            # if counter>9 and counter < 20:
                                # cv2.putText(crop_img, str(theta) ,(100,73+(counter-10)*30), cv2.FONT_HERSHEY_SIMPLEX, .4,(0,0,255),2)#
                            # if counter>19 and counter < 30:
                                # cv2.putText(crop_img, str(theta) ,(200,73+(counter-20)*30), cv2.FONT_HERSHEY_SIMPLEX, .4,(0,0,255),2)
                            # if counter>29 and counter < 40:
                                # cv2.putText(crop_img, str(theta) ,(300,73+(counter-20)*30), cv2.FONT_HERSHEY_SIMPLEX, .4,(0,0,255),2)
                            # if counter>39 and counter < 50:
                                # cv2.putText(crop_img, str(theta) ,(400,73+(counter-20)*30), cv2.FONT_HERSHEY_SIMPLEX, .4,(0,0,255),2)
                        else:
                            #cv2.line(overlay,(x1,y1),(x2,y2),(255,10,10),2)
                            a="oli"

        
        
        
        
        # data1=(set(data))
        # print data1
        # cl = HierarchicalClustering(data1, lambda x,y: abs(x-y))
        # data2 = cl.getlevel(8)     
        # print data2
        
        
        # flattened_list = []
        # for x in data2:
            # check=0
            # for y in x:
                # check=check+y
            # checksum=check/len(x)
            # flattened_list.append(checksum)
            
        
        
        # print flattened_list
        print data
        kmeans = KMeans(n_clusters=2, random_state=0, max_iter=3000).fit(data)
        print kmeans.cluster_centers_
        
             
        for rho,theta in lines[0]:
                        
                        a = np.cos(theta)
                        b = np.sin(theta)
                        x0 = a*rho
                        y0 = b*rho
                        x1 = int(x0 + 1000*(-b))
                        y1 = int(y0 + 1000*(a))
                        x2 = int(x0 - 1000*(-b))
                        y2 = int(y0 - 1000*(a))
                                                
                        
                        if (kmeans.predict([theta,rho]))==0:
                            cv2.line(overlay,(x1,y1),(x2,y2),(255,10,255),2)
                        else:
                            cv2.line(overlay,(x1,y1),(x2,y2),(255,50,10),2)
        
        opacity = .3
        cv2.addWeighted(overlay, opacity, crop_img, 1 - opacity, 0, crop_img)
        
        
        ta = np.cos(kmeans.cluster_centers_[0][0])
        tb = np.sin(kmeans.cluster_centers_[0][0])
        tx0 = ta*kmeans.cluster_centers_[0][1]
        ty0 = tb*kmeans.cluster_centers_[0][1]
        tx1 = int(tx0 + 1000*(-tb))
        ty1 = int(ty0 + 1000*(ta))
        tx2 = int(tx0 - 1000*(-tb))
        ty2 = int(ty0 - 1000*(ta))
        cv2.putText(crop_img, str(kmeans.cluster_centers_[0][0]*(180/np.pi)) ,(30,190), cv2.FONT_HERSHEY_SIMPLEX, .4,(0,0,255),2)
        cv2.line(crop_img,(tx1,ty1),(tx2,ty2),(255,0,0),2)
        ta = np.cos(kmeans.cluster_centers_[1][0])
        tb = np.sin(kmeans.cluster_centers_[1][0])
        tx0 = ta*kmeans.cluster_centers_[1][1]
        ty0 = tb*kmeans.cluster_centers_[1][1]
        tx1 = int(tx0 + 1000*(-tb))
        ty1 = int(ty0 + 1000*(ta))
        tx2 = int(tx0 - 1000*(-tb))
        ty2 = int(ty0 - 1000*(ta))
        cv2.line(crop_img,(tx1,ty1),(tx2,ty2),(255,0,255),2)
        cv2.putText(crop_img, str(kmeans.cluster_centers_[1][0]*(180/np.pi)) ,(300,190), cv2.FONT_HERSHEY_SIMPLEX, .4,(0,0,255),2)
        #opacity = 1
        #cv2.addWeighted(overlay2, opacity, crop_img, 1 - opacity, 0, crop_img)
        
        #bandwidth = estimate_bandwidth(lines, quantile=0.2, n_samples=500)
        #print lines
        #X = StandardScaler().fit_transform(lines)
        #print X
        #bandwidth = estimate_bandwidth(data2, quantile=0.2, n_samples=len(data2))
        #print bandwith
        # ms = MeanShift()

       
        # ms.fit(data2)
        # labels = ms.labels_
        # cluster_centers = ms.cluster_centers_

        # labels_unique = np.unique(labels)
        # n_clusters_ = len(labels_unique)

        # print("number of estimated clusters : %d" % n_clusters_)
        
        
        
        
        
        
        
        
        
                            
                       
        if counter>0:
            rho_all=rho_all/counter          

            course=rho_all
        
            #if course>90:
                #course=course-180
        else:
            course=200
        cv2.putText(crop_img, str(rho_all) ,(200,13), cv2.FONT_HERSHEY_SIMPLEX, .5,(0,0,255),2)
        #cv2.putText(crop_img, str(course) ,(10,13), cv2.FONT_HERSHEY_SIMPLEX, .5,(0,0,255),2)
        cv2.putText(crop_img, str(g) ,(10,33), cv2.FONT_HERSHEY_SIMPLEX, .5,(0,0,255),2)
        cv2.putText(crop_img, str(s) ,(10,53), cv2.FONT_HERSHEY_SIMPLEX, .5,(0,0,255),2)

        
    
    now = datetime.datetime.now()
    filename = "pictures/" 
    filename += str(now.microsecond)
    filename+= ".jpg"
        
    filename2 = "<img src=\""
    filename2 += filename
    filename2 += "\" alt=\"Fehler beim anzeigen\" />,"
        
    cv2.imwrite(filename, crop_img )
    
    test_results = {
        'shutter_speed': str(s),
        'awb_gain': str(g),
        'course': str(course),
        'img': filename2,
        'iso': str(ciso),
    }
    # dict of colors for each result:
    result_colors = {
            'success':      'lime',
            'failure':      'red',
            'error':        'yellow',
        }
    t = HTML.Table(header_row=['Test', 'Result'])
    for test_id in sorted(test_results):
        # create the colored cell:
        #color = result_colors[test_results[test_id]]
        colored_result = HTML.TableCell(test_results[test_id], 'white')
        # append the row with two cells:
        t.rows.append([test_id, colored_result])
    htmlcode = str(t)

    f = open('report2.html', 'a+')
    f.write(htmlcode)
    f.close()
           
    return course
    
    
def shot(name):

    global w
    global h

    # for i in range(5):
        # GPIO.output(CAMLED,True) # On
        # time.sleep(0.5)
        # GPIO.output(CAMLED,False) # Off
        # time.sleep(0.5)
        
    camera = PiCamera()
    camera.close()
    camera = PiCamera()
    rawCapture = PiRGBArray(camera)
   
# Turn the camera's LED off
    camera.led = False
    w=800
    h=600
    camera.resolution = (w, h)
# Take a picture while the LED remains off
   
    time.sleep(.2)
   
    
    camera.iso = 100 #200
   
    #camera.contrast=100
    
   # camera = PiCamera(resolution=(1280, 720), framerate=30)
    # Set ISO to the desired value
   
    # Wait for the automatic gain control to settle
    time.sleep(4)
    # Now fix the values
    camera.shutter_speed = camera.exposure_speed
    s = camera.shutter_speed
    if s<10000:
        camera.iso=100 #600
    ciso=camera.iso
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g
    # Finally, take several photos with the fixed settings
    #camera.capture_sequence(['image%02d.jpg' % i for i in range(10)])
    camera.capture(rawCapture, format="bgr")
    picam_01 = rawCapture.array
             
    #crop_img2 = picam_01[(h/5.33):(h/1.23), (w/24):(w/1.04)].copy() # Crop from x, y, w, h -> 100, 200, 300, 400
    
    filename=name
    filename += ".jpg"
    
    filenamewww = "/var/www/html/"
    filenamewww += name
    filenamewww += ".jpg"
       
    cv2.imwrite( filename, picam_01 )
    cv2.imwrite( filenamewww, picam_01 )
   
    camera.close();
                   
    return 0
    

# Create a black image, a windowimg = cv2.imread('net.jpg')
def get_orientation():

    call(["raspistill", "-w", "480", "-h", "320", "-o", "cam.jpg"])

    time.sleep(3)


    img = cv2.imread('cam.jpg')
    
    crop_img = img[60:260, 20:459].copy() # Crop from x, y, w, h -> 100, 200, 300, 400
    
    gray = cv2.cvtColor(crop_img,cv2.COLOR_BGR2GRAY)
    cv2.imwrite( "Gray_Image.jpg", gray )
    
    blur = cv2.GaussianBlur(gray,(15,15),0)
    cv2.imwrite( "Gray_Image.jpg", blur )
    #min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(blur)
    #high_thresh, thresh_im = cv2.threshold(blur, min_val+15,255,cv2.THRESH_BINARY_INV)
    #cv2.imwrite( "thresh.jpg", thresh_im )
    #lowThresh = 0.8*high_thresh
   

    
    edges = cv2.Canny(blur,20,60,3)   #working
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
                                           
                       
        if counter>0:
            rho_all=rho_all/counter          

            course=rho_all*(180/np.pi)
        
            if course>90:
                course=course-180
        else:
            course=0
        
        cv2.putText(blur, str(course) ,(10,140), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2)

        cv2.imwrite( "final.jpg", blur )
    
    return course
    
def get_cv2():

    global w
    global h

    # for i in range(5):
        # GPIO.output(CAMLED,True) # On
        # time.sleep(0.5)
        # GPIO.output(CAMLED,False) # Off
        # time.sleep(0.5)
        
   
    w=800
    h=600
 
    picam_01 = cv2.imread('shot1.jpg',0)
  
     
    picam_02 = cv2.imread('shot2.jpg',0)
      
           
    crop_img = picam_02[(h/5.33):(h/1.23), (w/24):(w/1.04)].copy() # Crop from x, y, w, h -> 100, 200, 300, 400
    
    crop_img2 = picam_01[(h/5.33):(h/1.23), (w/24):(w/1.04)].copy() # Crop from x, y, w, h -> 100, 200, 300, 400
    
      
    diff = cv2.absdiff(crop_img,crop_img2)
    
    
     
       
    #gray = cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
    
    #blur2 = cv2.GaussianBlur(diff,(15,15),0)
    
    #ret,thresh2 = cv2.threshold(blur2, 6,255,cv2.THRESH_BINARY_INV)
    
    #cv2.imwrite( "gray.jpg", gray )
    
   
    
    blur = cv2.GaussianBlur(diff,(15,15),4)
    
    ret3,th3 = cv2.threshold(diff,20,255,cv2.THRESH_BINARY_INV)
    cv2.imwrite( "blur.jpg", ret3 )
        
    edges = cv2.Canny(diff,8,24,3)   #working
    cv2.imwrite( "edges.jpg", edges )

    cv2.imwrite( "diff.jpg", diff )
    
     
    lines = cv2.HoughLines(edges,1,np.pi/180,50)
    
    data=[]
    

    counter = 0
    rho_all = 0
    course = 200
    overlay = crop_img.copy()
    overlay2 = crop_img.copy()
   
    if lines is not None:
        for rho,theta in lines[0]:
                        course=0
                        a = np.cos(theta)
                        b = np.sin(theta)
                        x0 = a*rho
                        y0 = b*rho
                        x1 = int(x0 + 1000*(-b))
                        y1 = int(y0 + 1000*(a))
                        x2 = int(x0 - 1000*(-b))
                        y2 = int(y0 - 1000*(a))
                        #data.insert(0,[rho,theta])
                        data.insert(0,[theta,rho])
                        if theta>((np.pi/4)*3) or theta<(np.pi/4):
                            counter=counter+1
                            #cv2.line(crop_img,(x1,y1),(x2,y2),(0,255,10),2)
                            temp=theta*(180/np.pi)
                            if temp>90:
                                temp=temp-180
                            #data.insert(0,[theta,rho])
                             
                            rho_all=rho_all+temp
                            
                            # if counter < 10:
                                # cv2.putText(crop_img, str(theta) ,(10,73+counter*30), cv2.FONT_HERSHEY_SIMPLEX, .4,(0,0,255),2)
                            # if counter>9 and counter < 20:
                                # cv2.putText(crop_img, str(theta) ,(100,73+(counter-10)*30), cv2.FONT_HERSHEY_SIMPLEX, .4,(0,0,255),2)#
                            # if counter>19 and counter < 30:
                                # cv2.putText(crop_img, str(theta) ,(200,73+(counter-20)*30), cv2.FONT_HERSHEY_SIMPLEX, .4,(0,0,255),2)
                            # if counter>29 and counter < 40:
                                # cv2.putText(crop_img, str(theta) ,(300,73+(counter-20)*30), cv2.FONT_HERSHEY_SIMPLEX, .4,(0,0,255),2)
                            # if counter>39 and counter < 50:
                                # cv2.putText(crop_img, str(theta) ,(400,73+(counter-20)*30), cv2.FONT_HERSHEY_SIMPLEX, .4,(0,0,255),2)
                        else:
                            #cv2.line(overlay,(x1,y1),(x2,y2),(255,10,10),2)
                            a="oli"

        
        
        
        
        # data1=(set(data))
        # print data1
        # cl = HierarchicalClustering(data1, lambda x,y: abs(x-y))
        # data2 = cl.getlevel(8)     
        # print data2
        
        
        # flattened_list = []
        # for x in data2:
            # check=0
            # for y in x:
                # check=check+y
            # checksum=check/len(x)
            # flattened_list.append(checksum)
            
        
        
        # print flattened_list
        print data
        kmeans = KMeans(n_clusters=2, random_state=0, max_iter=3000).fit(data)
        print kmeans.cluster_centers_
        
             
        for rho,theta in lines[0]:
                        
                        a = np.cos(theta)
                        b = np.sin(theta)
                        x0 = a*rho
                        y0 = b*rho
                        x1 = int(x0 + 1000*(-b))
                        y1 = int(y0 + 1000*(a))
                        x2 = int(x0 - 1000*(-b))
                        y2 = int(y0 - 1000*(a))
                                                
                        
                        if (kmeans.predict([theta,rho]))==0:
                            cv2.line(overlay,(x1,y1),(x2,y2),(255,10,255),2)
                        else:
                            cv2.line(overlay,(x1,y1),(x2,y2),(255,50,10),2)
        
        opacity = .3
        cv2.addWeighted(overlay, opacity, crop_img, 1 - opacity, 0, crop_img)
        
        
        ta = np.cos(kmeans.cluster_centers_[0][0])
        tb = np.sin(kmeans.cluster_centers_[0][0])
        tx0 = ta*kmeans.cluster_centers_[0][1]
        ty0 = tb*kmeans.cluster_centers_[0][1]
        tx1 = int(tx0 + 1000*(-tb))
        ty1 = int(ty0 + 1000*(ta))
        tx2 = int(tx0 - 1000*(-tb))
        ty2 = int(ty0 - 1000*(ta))
        cv2.putText(crop_img, str(kmeans.cluster_centers_[0][0]*(180/np.pi)) ,(30,190), cv2.FONT_HERSHEY_SIMPLEX, .4,(0,0,255),2)
        cv2.line(crop_img,(tx1,ty1),(tx2,ty2),(255,0,0),2)
        ta = np.cos(kmeans.cluster_centers_[1][0])
        tb = np.sin(kmeans.cluster_centers_[1][0])
        tx0 = ta*kmeans.cluster_centers_[1][1]
        ty0 = tb*kmeans.cluster_centers_[1][1]
        tx1 = int(tx0 + 1000*(-tb))
        ty1 = int(ty0 + 1000*(ta))
        tx2 = int(tx0 - 1000*(-tb))
        ty2 = int(ty0 - 1000*(ta))
        cv2.line(crop_img,(tx1,ty1),(tx2,ty2),(255,0,255),2)
        cv2.putText(crop_img, str(kmeans.cluster_centers_[1][0]*(180/np.pi)) ,(300,190), cv2.FONT_HERSHEY_SIMPLEX, .4,(0,0,255),2)
        #opacity = 1
        #cv2.addWeighted(overlay2, opacity, crop_img, 1 - opacity, 0, crop_img)
        
        #bandwidth = estimate_bandwidth(lines, quantile=0.2, n_samples=500)
        #print lines
        #X = StandardScaler().fit_transform(lines)
        #print X
        #bandwidth = estimate_bandwidth(data2, quantile=0.2, n_samples=len(data2))
        #print bandwith
        # ms = MeanShift()

       
        # ms.fit(data2)
        # labels = ms.labels_
        # cluster_centers = ms.cluster_centers_

        # labels_unique = np.unique(labels)
        # n_clusters_ = len(labels_unique)

        # print("number of estimated clusters : %d" % n_clusters_)
        
        
        
        
        
        
        
        
        
                            
                       
        if counter>0:
            rho_all=rho_all/counter          

            course=rho_all
        
            #if course>90:
                #course=course-180
        else:
            course=200
        cv2.putText(crop_img, str(rho_all) ,(200,13), cv2.FONT_HERSHEY_SIMPLEX, .5,(0,0,255),2)
        #cv2.putText(crop_img, str(course) ,(10,13), cv2.FONT_HERSHEY_SIMPLEX, .5,(0,0,255),2)
        #cv2.putText(crop_img, str(g) ,(10,33), cv2.FONT_HERSHEY_SIMPLEX, .5,(0,0,255),2)
        #cv2.putText(crop_img, str(s) ,(10,53), cv2.FONT_HERSHEY_SIMPLEX, .5,(0,0,255),2)

        
    
    now = datetime.datetime.now()
    filename = "pictures/" 
    filename += str(now.microsecond)
    filename+= ".jpg"
        
    filename2 = "<img src=\""
    filename2 += filename
    filename2 += "\" alt=\"Fehler beim anzeigen\" />,"
        
    cv2.imwrite(filename, crop_img )
    
    foo = "0"
    
    test_results = {
        'shutter_speed': str(foo),
        'awb_gain': str(foo),
        'course': str(course),
        'img': filename2,
        'iso': str(foo),
    }
    # dict of colors for each result:
    result_colors = {
            'success':      'lime',
            'failure':      'red',
            'error':        'yellow',
        }
    t = HTML.Table(header_row=['Test', 'Result'])
    for test_id in sorted(test_results):
        # create the colored cell:
        #color = result_colors[test_results[test_id]]
        colored_result = HTML.TableCell(test_results[test_id], 'white')
        # append the row with two cells:
        t.rows.append([test_id, colored_result])
    htmlcode = str(t)

    f = open('report2.html', 'a+')
    f.write(htmlcode)
    f.close()
           
    print course
    return course
    