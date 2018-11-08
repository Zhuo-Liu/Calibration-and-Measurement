import numpy as np
import cv2
import glob
import os

'''
This is a calibration function using OpenCV Chessboard calibration plate.
--------------------------------------------------------------------
Input Parameters:
 1. length: length of the square (a single chess lattice) in mm
 2. rows: the number of lattices in a column (number of rows)
 3. cols: the number of lattices in a row (number of columns)
 4. image_path: path of images of calibration plate images, i.e. "./images/"
Return Parameters:
 1. Bool Value
 2. Camera Intrinsic Matrix
 3. Distortion Matrix
Other Output:
 Generate a directory "./calibration_results" containing numpy array of all the calibration
 result matrixes. The number of rotation_matrix_*.txt and translation_matrix_*.txt represents
 the corresponding number of input images.
---------------------------------------------------------------------
Please note that:
 1. Some parameters may need modifications for real condition.
 2. Calibration is a ONE-TIME process. Manually check of calibration images is NECESSARY.
'''

def perform_calibration(length,rows,cols,image_path):
    # setting termination condition
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)

    m = rows - 1
    n = cols - 1
    assert m >= 1, 'invalid number of rows'
    assert n >= 1, 'invalid number of columns'

    # setting world coordinates of the calibration plate
    world_points = np.zeros((m*n,3),np.float32)
    world_points[:,:2]= np.mgrid[0:m,0:n].T.reshape(-1,2)
    world_points = world_points * length

    obj_points = []
    img_points = []

    #reading calibration images, finding corners
    path = os.path.join(image_path,"*.tif")
    images = glob.glob(path)

    for image in images:
        img = cv2.imread(image)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        ret, corners = cv2.findChessboardCorners(gray,(m,n),None)

        if ret == True:
            obj_points.append(world_points)

            # find subpixel corners, the size of the searching window may need modifications!!!
            corners2 = cv2.cornerSubPix(gray, corners, (15,15),(-1,-1),criteria)
            img_points.append(corners2)

            img = cv2.drawChessboardCorners(img, (m,n), corners2,ret)
            img_resized = cv2.resize(img,(1184, 854))

            cv2.putText(img_resized, 'Please check if all corners are correctly found.',
            (50, 30), cv2.FONT_HERSHEY_SIMPLEX,
            0.6, (0, 0, 255), 2)
            cv2.putText(img_resized, 'If not, press esc to exit (you may need to change an image).',
            (50, 60), cv2.FONT_HERSHEY_SIMPLEX,
            0.6, (0, 0, 255), 2)
            cv2.putText(img_resized, 'Press any other keys to continue.',
            (50, 90), cv2.FONT_HERSHEY_SIMPLEX,
            0.6, (0, 255, 0), 2)
            cv2.imshow('Calibration',img_resized)

            cv2.imshow('img',img_resized)
            # key=cv2.waitKey()
            # if(key == 27):
            #     print("Program exits manually.")
            #     exit(0)
            cv2.destroyAllWindows()
    

    # calibration
    # rvecs, tvecs are the rotation vector and moving vector
    # mtx is the camera matrix
    # dist is the distortion coefficients
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)
    
    #write part
    dir = './calibration_result'
    if not os.path.exists(dir):
        os.makedirs(dir)

    np.savetxt("./calibration_result/camera_intrinsic_matrix.txt",mtx)

    np.savetxt("./calibration_result/distortion_matrix.txt",dist)

    i=1
    for mat in rvecs:
        np.savetxt("./calibration_result/rotation_matrix_{}.txt".format(i),mat)
        i=i+1
    j=1 
    for mat in tvecs:
        np.savetxt("./calibration_result/translation_matrix_{}.txt".format(j),mat)
        j=j+1
    
    return ret, mtx, dist