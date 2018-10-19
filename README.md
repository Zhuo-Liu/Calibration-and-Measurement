# Calibration-and-Measurement

Transform.py is written to find out mm-pixel ratio using **OpenCV Chessboard calibration plate**.

- Input Parameters:
  1. length: length of the square (a single chess lattice) in mm
  2. rows: the number of lattices in a column (number of rows)
  3. cols: the number of lattices in a row (number of columns)
  4. img: input image of the calibration plate
- Output Parameters:
  1. averaging mm per pixel
  2. deviation of mm/pixel

An example for using this is **test.py**, where 10 images of OpenCV Chessboard calibration plate are used to determine the pixel_per_mm.


Please note that :
- **No** camera calibration or undistortion have been added. 
- Some parameters may need modifications for real condition.
- For more accurate result, the camera plane should be as parallel to object plane as possible.
