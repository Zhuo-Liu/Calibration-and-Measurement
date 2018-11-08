import cv2
import numpy as np

'''
This function is written to find out mm-pixel ratio using OpenCV Chessboard calibration plate.
Some parameters may need modifications for real condition.
For more accurate result, the camera plane should be as parallel to object plane as possible.
--------------------------------------------------------------------
Input Parameters:
 1. length: length of the square (a single chess lattice) in mm
 2. rows: the number of lattices in a column (number of rows)
 3. cols: the number of lattices in a row (number of columns)
 4. img: input image of the calibration plate
Output Parameters:
 1. averaging mm per pixel
 2. deviation of mm/pixel
---------------------------------------------------------------------
'''

def transform(length,rows,cols,img):
    dis=[]
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    
    m = rows - 1
    n = cols - 1
    if m < 1 or n < 1:
        print("Error: Invalid number of rows or columns!")
        exit(1)

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # find corners on chess calibration plate
    ret, corners = cv2.findChessboardCorners(gray,(m,n),None)
    if ret == True:
        # find subpixel corners, the size of the searching window may need modifications!!!
        corners2 = cv2.cornerSubPix(gray, corners, (15,15),(-1,-1),criteria)

        if len(corners2) != m*n:
            print("Error: corners are not all correctly found!")
            exit(1)
        
        # uncommet below part to enable manual check
        '''
        # draw the corners on the image
        image = cv2.drawChessboardCorners(img, (m,n), corners2,ret)
        image_resized = cv2.resize(image,(1184, 854))

        cv2.putText(image_resized, 'Please check if all corners are correctly found.',
        (50, 30), cv2.FONT_HERSHEY_SIMPLEX,
        0.6, (0, 0, 255), 2)
        cv2.putText(image_resized, 'If not, press esc to exit (you may need to change an image).',
        (50, 60), cv2.FONT_HERSHEY_SIMPLEX,
        0.6, (0, 0, 255), 2)
        cv2.putText(image_resized, 'Press any other keys to continue.',
        (50, 90), cv2.FONT_HERSHEY_SIMPLEX,
        0.6, (0, 255, 0), 2)
        cv2.imshow('Chess Board',image_resized)

        key=cv2.waitKey()
        if(key == 27):
            print("Program exits manually.")
            exit(0)
        cv2.destroyAllWindows()
        '''

        # find pixel distance between neighbour corners
        for i in range(m):
            for j in range(n-1):
                deltax = np.abs(corners2[i*n+j+1][0][0]-corners2[i*n+j][0][0])
                deltay = np.abs(corners2[i*n+j+1][0][1]-corners2[i*n+j][0][1])
                delta = np.sqrt(deltax*deltax + deltay*deltay)
                dis.append(delta)
        
        for l in range(m-1):
            for k in range(n):
                deltax = np.abs(corners2[(l+1)*n+k][0][0]-corners2[l*n+k][0][0])
                deltay = np.abs(corners2[(l+1)*n+k][0][1]-corners2[l*n+k][0][1])
                delta = np.sqrt(deltax*deltax + deltay*deltay)
                dis.append(delta)

        # find the ratio and deviation
        pixel = length / np.array(dis)
        average = np.average(pixel)
        deviation = np.std(pixel)

        return average,deviation

    else:
        print("Error: Chess board not found!")
        exit(1)