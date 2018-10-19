import numpy as np
import cv2
import transform

imgpath="images/"
i=1
rat = []
while(i<11):
    imgp = imgpath  +  "{}.tif".format(i)
    img = cv2.imread(imgp)
    
    ratio,dev = transform.transform(3.6,7,7,img)
    rat.append(ratio)
    i=i+1

pixel_per_mm = np.array(rat)
ave = np.average(pixel_per_mm)
deviation = np.std(pixel_per_mm)

print("The average pixel per mm is " + str(ave))