import numpy as np
import cv2

'''
This function is for undistortion after calibration. Camera intrinsic matrix
and undistortion matrix are mandatory.
--------------------------------------------------------------------
Input Parameters:
 1. image: input image 
 2. camera_mat_path: the matrix intrinsic matrix txt file obtained from calibration 
    function. i.e. "./calibration_result/camera_intrinsic_matrix.txt"
 3. distrot_mat_path: the distortion matrix txt file obtained from calibration 
    function. i.e. "./calibration_result/camera_intrinsic_matrix.txt"
Output:
    undistorted image
-----------
'''

def perform_undistortion(image,camera_mat_path,distort_mat_path):
    mtx = np.loadtxt(camera_mat_path)
    dist = np.loadtxt(distort_mat_path)
    
    #optimzing camera matrix
    img = cv2.imread(image)
    h, w = img.shape[:2]
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

    #undistort
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
    #crop the image
    x,y,w,h = roi
    dst = dst[y:y+h, x:x+w]
    cv2.imwrite('undistort_image.png',dst)

    return dst