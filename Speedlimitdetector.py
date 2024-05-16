# input the models
import cv2
import math
import keyboard
import multiprocessing
import time
import numpy as np
from ultralytics import YOLO
from collections import deque
from collections import Counter
from central_Logic import receive_data
import torch
model = YOLO(r"/home/rdw_orin/Desktop/RDW2024-Software-Structure/Models/numberrec.pt")


def Euclidean_dist(v1=[0,0],v2=[0,0]):
    """Will calculate the Euclidean distance between two 2-dimensional vectors"""
    return ((v1[0]-v2[0])**2+(v1[1]-v2[1])**2)**(1/2)


def predict(chosen_model, img, classes=[], conf=0.5):
    if classes:
        results = chosen_model.predict(img, classes=classes, conf=conf)
    else:
        results = chosen_model.predict(img, conf=conf)

    return results


def predict(chosen_model, img, classes=[], conf=0.5):
    if classes:
        results = chosen_model.predict(img, classes=classes, conf=conf)
    else:
        results = chosen_model.predict(img, conf=conf)

    return results


def predict_and_detect(chosen_model, img, classes=[], conf=0.5):
    results = predict(chosen_model, img, classes, conf=conf)
    
    # for result in results:

#originally used a for loop, but there is only one result always, so I just made it take the first item of the list

    result = results[0]

    approved_dict = {}

    # Iterate over boxes in result.boxes
    for box in result.boxes:
        # Check conditions for approval
        if (box.cls == 0 and box.conf >= 0.3) or (box.cls == 1 and box.conf >= 0.1) or (box.cls == 2 and box.conf >= 0.3) or (box.cls == 3 and box.conf >= 0.3):
            # Calculate distance from center
            dist = Euclidean_dist([box.xywhn[0][0], box.xywhn[0][1]], [0.5, 0.5])
            # Add to approved dictionary
            if box.cls == 0:
                cls = 0
            elif box.cls == 1:
                cls = 1
            elif box.cls == 2:
                cls = 2
            elif box.cls == 3:
                cls = 5
            if cls not in approved_dict:
                approved_dict[cls] = [dist]
            else:
                approved_dict[cls].append(dist)

        lowest_values = []
        approvednums = []
        for key, values in approved_dict.items():
        # Find the minimum value in the list of values for the current key
            approvednums.append(key)
        # Add the minimum value to the list
            lowest_values.append(min(values))

        cv2.rectangle(img, (int(box.xyxy[0][0]), int(box.xyxy[0][1])),
                        (int(box.xyxy[0][2]), int(box.xyxy[0][3])), (255, 0, 0), 2)
        cv2.putText(img, f"{result.names[int(box.cls[0])]}",
                    (int(box.xyxy[0][0]), int(box.xyxy[0][1]) - 10),
                    cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
    # print(approved_dict)

    if len(approvednums)<2: #if there are no two numbers detected
        return img, results, None
    elif len(approvednums)>2: #logic to take the two numbers closest to the center
        combined_lists = zip(approvednums, lowest_values)

        # Sort the combined list based on the second element of each tuple (which is from list2)
        sorted_combined_lists = sorted(combined_lists, key=lambda x: x[1], reverse=False)

        # Unzip the sorted list to get back the sorted lists
        sorted_cls, sorted_dists = zip(*sorted_combined_lists)
        # print(sorted_cls,sorted_dists)
        approvednums = sorted_cls[:2]


    if len(approvednums)==2:
        if set(approvednums)==set([1,0]):
            return img, results, 10
        elif set(approvednums)==set([1,5]):
            return img, results, 15
        elif set(approvednums)==set([2,0]):
            return img, results, 20
        else:
            return img, results, None
    return img, results, None




# Read image. 
# image_path = r'E:\Honors\test29_04\orange\12_5m.png'
# img = cv2.imread(image_path, cv2.IMREAD_COLOR)
# imgcropping = cv2.imread(image_path,0) #image used for cropping later
# imgcolor = cv2.imread(image_path)



#without conversion to color_gbr2lab
#RGB Value at (1060,588): (130, 41, 33)     3m
#RGB Value at (1052,632): (135, 48, 39)     6m
#RGB Value at (946,650): (165, 59, 48)      9m
#RGB Value at (955,589): (174, 123, 123)    12m
#RGB Value at (968,614): (121, 84, 98)      18m



#BGR Value at (995,605): (124, 148, 127)    18m

#based on super scientific experiments
#brg = [29,29,105]


# Threshold the Lab image, keep only the red pixels
# Possible yellow threshold: [20, 110, 170][255, 140, 215]
# Possible blue threshold: [20, 115, 70][255, 145, 120]

def speedlimitfinder(imaage):
    """Detects speed limits in the image, 10,15,20"""


    #check if the images still work, as before it was a function it worked slighlty differently
    # Convert original image to BGR, since Lab is only available from BGR
    captured_frame_bgr = cv2.cvtColor(imaage, cv2.COLOR_BGRA2BGR)
    # First blur to reduce noise prior to color space conversion
    captured_frame_bgr = cv2.medianBlur(captured_frame_bgr, 3)
    # Convert to Lab color space, we only need to check one channel (a-channel) for red here
    captured_frame_lab = cv2.cvtColor(captured_frame_bgr, cv2.COLOR_BGR2Lab)

    # cv2.imshow("Thresholded Red Regions", captured_frame_lab)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # Threshold the Lab image, keep only the red pixels
    captured_frame_lab_red = cv2.inRange(captured_frame_lab, np.array([20, 140, 125]), np.array([190, 255, 255]))
    # cv2.imshow("Thresholded Red Regions", captured_frame_lab_red)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # Second blur to reduce more noise, easier circle detection
    captured_frame_lab_red = cv2.GaussianBlur(captured_frame_lab_red, (5, 5), 2, 2)
    # cv2.imshow("Gausian Blur Red Regions", captured_frame_lab_red)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


    # Use the Hough transform to detect circles in the image

    #changed min radius to 10 from 5
    detected_circles = cv2.HoughCircles(captured_frame_lab_red, cv2.HOUGH_GRADIENT, 1, captured_frame_lab_red.shape[0] / 8, param1=10, param2=50, minRadius=3, maxRadius=220)
    detectionlist = [[],[],[]]
    # Draw circles that are detected. 
    if detected_circles is not None: 
    
        # Convert the circle parameters a, b and r to integers. 
        detected_circles = np.uint16(np.around(detected_circles)) 
    
        for pt in detected_circles[0, :]: 
            a, b, r = pt[0], pt[1], pt[2] 
            a0 = round(a,3)
            b0= round(b,3)
            r0 = round(r,3)
            # print('x0',a,'y0',b,'rad',r)
            #crops the image to the fit only the traffic sign
            # Define bounding box coordinates for cropping
            x1 = max(0, a0 - r0)
            # print(b0)
            # print(r0)
            # print(b0-r0)
            if 0>= b0-r0 or imaage.shape[0]<=b0-r0:
                y1=0
            else:
                y1=b0-r0
            x2 = min(imaage.shape[1], a0 + r0) 
            y2 = min(imaage.shape[0], b0 + r0)
            
            # print('x1:',x1,'x2:',x2)
            # print('y1:',y1,'y2:',y2)

            # Crop the image
            enlarged_image = imaage[y1:y2, x1:x2]
            # cv2.imshow("Cropped Circle", enlarged_image)
            # cv2.imwrite('croppedim.jpg', enlarged_image)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            result_img, results, detectedspeedlimit = predict_and_detect(model, enlarged_image, classes=[], conf=0.05)
            if detectedspeedlimit == 10:
                detectionlist[0] = [x1,y1,x2,y2]
            elif detectedspeedlimit == 15:
                detectionlist[1] = [x1,y1,x2,y2]
            elif detectedspeedlimit == 20:
                detectionlist[2] = [x1,y1,x2,y2]
            # cv2.imshow("Image", result_img)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            
            # if not None:
            #     print("There is a speed limit in the image:",detectedspeedlimit)
            # print('shape of croped image:',enlarged_image.shape)

            #rescales the image
            # y_scale_factor = img1.shape[0]/enlarged_image.shape[0]
            # x_scale_factor = img1.shape[1]/enlarged_image.shape[1]
            # enlarged_image = cv2.resize(enlarged_image, None, fx=x_scale_factor, fy=y_scale_factor, interpolation=cv2.INTER_LINEAR)


        
            # Show the cropped image

            # Draw the circumference of the circle. 
            # cv2.circle(img, (a, b), r, (0, 255, 0), 2) 
    
            # Draw a small circle (of radius 1) to show the center. 
        #     cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
        # cv2.imwrite('detected.jpg', img)
        # cv2.imshow("Detected Circle", img) 
        # cv2.waitKey(0)
        return detectionlist
    else:
        return detectionlist
        #found no circles so returns empty list
        # print('no circles found')