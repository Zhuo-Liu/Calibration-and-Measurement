import numpy as np
import cv2
import transform
import calibration
import undistort

# # measure
# imgpath="images/"
# i=1
# rat = []
# while(i<11):
#     imgp = imgpath  +  "{}.tif".format(i)
#     img = cv2.imread(imgp)
    
#     ratio,dev = transform.transform(3.6,7,7,img)
#     rat.append(ratio)
#     i=i+1

# pixel_per_mm = np.array(rat)
# ave = np.average(pixel_per_mm)
# deviation = np.std(pixel_per_mm)

# print("The average pixel per mm is " + str(ave))

#calibration
calibration.perform_calibration(3.6, 7, 7, "images/")

#undistort
undistort.perform_undistortion("./images/1.tif","./calibration_result/camera_intrinsic_matrix.txt",
 "./calibration_result/distortion_matrix.txt")