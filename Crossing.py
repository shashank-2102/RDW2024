import numpy as np
import cv2


def Crosswalk(image): 
    width = image.shape[1]
    centre = width/2
    mask = np.zeros(image.shape[:2], np.uint8)
  
    # specify the background and foreground model
    # using numpy the array is constructed of 1 row
    # and 65 columns, and all array elements are 0
    # Data type for the array is np.float64 (default)
    backgroundModel = np.zeros((1, 65), np.float64)
    foregroundModel = np.zeros((1, 65), np.float64)
  

    #rectangle = (0, 200, 1190, 616)

 
    # Convert to graycsale
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Blur the image for better edge detection
    img_blur = cv2.GaussianBlur(img_gray, (3,3), 0) 
    
    # Sobel Edge Detection
    sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5) # Sobel Edge Detection on the X axis
    sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5) # Sobel Edge Detection on the Y axis
    sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5) # Combined X and Y Sobel Edge Detection
    # Display Sobel Edge Detection Images
 
    # Canny Edge Detection
    edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200) # Canny Edge Detection
    # Display Canny Edge Detection Image
    #cv2.imshow('Canny Edge Detection', edges)
    #cv2.waitKey(0)
    

    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=150)
    final = []
    min_space = 5
    zebra_final = []
    
    # Check if lines are detected
    if lines is not None:
        # Draw lines on the original image
        for line in lines:
            rho, theta = line[0]
            a = np.cos(theta)
            b = np.sin(theta)
        
            x0 = a*rho
        
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            final.append([x1,x2, y1,y2])
     
        xpol = 10000
        for line in final:
            x1,x2,y1,y2 = line
            ang = abs(np.arctan2(y2-y1, x2-x1))* 180 / np.pi
            if ang < 15 and not any(abs(y1-zebra_final[i][1]) < min_space for i in range(len(zebra_final))):
                zebra_final.append([x1,x2,y1,y2])
                
        # Display the results
        h1 = []
        if zebra_final != []:
            for crossing in zebra_final:
                h1.append(crossing[3])
            h1 = max(h1)
            sx1 = int(centre - 100)
            sy1 = int(h1)
            sx2 = int(centre + 100)
            sy2 = int(h1 - 20)
            return [sx1, sy1, sx2, sy2]
    
    # Return an empty list if no lines are detected
    return []