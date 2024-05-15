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
model = YOLO("C:\\Users\\Jandl\\Downloads\\numberrec.pt")

# capture front and back camera
cam_front_index = 0   # set index of rear camera
cam_rear_index = 1
cap_front = cv2.VideoCapture(cam_front_index)  # capture front camera
cap_rear = cv2.VideoCapture(cam_rear_index)  # capture rear camera

# setting width and height of camera (pixels)
cap_front.set(3, 640)
cap_front.set(4, 480)
cap_rear.set(3, 640)
cap_rear.set(4, 480)

class ObjectData:
    def __init__(self):
        self.classes = {
            'person': [],
            'crossing': [],
            '10': [],
            '15': [],
            '20': [],
            'red': [],
            'green': [],
            'car': [],
            'rear_car': []
        }

    def add_data(self, class_name, coords):
        if class_name in self.classes:
            # add new coordinates
            self.classes[class_name] = coords

# filter
def combine_filter(buffer):
    output = {}
    counter = Counter()
    last_coord = {}
    obj_data = ObjectData()
    for item in buffer:
        for class_name, coords_list in item.items():
            counter[class_name] += len(coords_list)
            last_coord[class_name] = coords_list[-1] if coords_list else None
    for class_name in counter:
        if counter[class_name] > 4:
            obj_data.add_data(class_name, last_coord[class_name])
    return obj_data.classes  

# returns the classname for a specific index of the class
def get_class_name(index, model_index):
    classes = classes_list[model_index]
    class_names = class_names_list[model_index]
    if index < len(classes):
        return class_names[index]
    else:
        return 0

# input the models


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
        #width = image.shape[1]
        #midpoint = width/2
        #print(ang)
        #if ang > 30 and not any(abs(ang-angs[i]) < min_diff for i in range(len(angs))):
        #    filtered_final.append([x1,x2,y1,y2])
        #    angs.append(ang)
        #    cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
        if ang < 15 and not any(abs(y1-zebra_final[i][1]) < min_space for i in range(len(zebra_final))):
            zebra_final.append([x1,x2,y1,y2])
            #cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 2)    

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
    else:
        return []

models = [
    YOLO("Models\\yolov8n.pt"),
    # YOLO("Models\\traffic_light_v1.pt"), 
    # YOLO("Models\\traffic_light_v1.pt"),
    # YOLO("Models\\zebra_crossing.pt") 
    
]
# classes for each model usually number of classes
classes_list = [
    [0, 1, 2],
]

# names of classes for each model
class_names_list = [
    ["person", "nothing", "car"],
]

#buffer
buffer_size = 10
frame_buffer = deque(maxlen=buffer_size)
output = {}

def send_data(queue):
    while True:
        pass
        #print("Sending data")
        #output = combine_filter(frame_buffer)
        #queue.put(output)
        #frame_buffer.clear()
        #time.sleep(0.5)  

if __name__ == '__main__':
    print("Creating queue")
    print("CUDA", torch.cuda.is_available())
    # Create a queue
    queue = multiprocessing.Queue()
    
    # Start the sender process
    sender_process = multiprocessing.Process(target=send_data, args=(queue,))
    sender_process.start()
    
    # Start the receiver process
    receiver_process = multiprocessing.Process(target=receive_data, args=(queue,))
    receiver_process.start()

    while True:
        # success is a boolean that indicates if frame was read successfully img is the frame
        success_front, img_front = cap_front.read()
        #img_front = 
        success_rear, img_rear = cap_rear.read()

        # removes any detections
        objects_by_type = {}
        # model_index contains index, model is the actual model
        for model_index, model in enumerate(models):
            # apply model to frame
            if model_index == 0:
                results_front = model.predict(img_front, classes=[0, 2], save=False, verbose=False)
            else:
                results_front = model(img_front, stream=True)

            for results in results_front:
                # boxes gives coordinates of edges of box (bottom left and top right)
                boxes = results.boxes
                for box in boxes:
                    # dislays confidence
                    confidence = math.ceil((box.conf[0] * 100)) / 100
                    if confidence < 0.4:
                        continue

                    # prints confidence
                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    # prints name of class
                    cls = int(box.cls[0])
                    class_name = get_class_name(cls, model_index)

                    # extraction = [class_name, x1, y1, x2, y2]
                    extraction = [x1, y1, x2, y2]
                    if class_name in objects_by_type:
                        objects_by_type[class_name].append(extraction)
                    else:
                        objects_by_type[class_name] = [extraction]
           
        # results rear only checks model with car
        results_rear = models[0](img_rear, stream=True, verbose=False)
        
        # similar steps as in front camera
        for results in results_rear:
            boxes = results.boxes
            for box in boxes:
                cls = int(box.cls[0])
                class_name = get_class_name(cls, 0)  # model index 0 corresponds to the first model

                if class_name != "car":
                    continue  # skip to the next detection if the class is not a car

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = math.ceil((box.conf[0] * 100)) / 100
                
                extraction = [x1, y1, x2, y2]

                if "rear_car" in objects_by_type:
                    objects_by_type["rear_car"].append(extraction)
                else:
                    objects_by_type["rear_car"] = [extraction]

        # If there are mutiple readings of one speed from the speed limit finder only the first one will be used
        #img = cv2.imread(img_front, cv2.IMREAD_COLOR)
        detection = speedlimitfinder(img_front)
        coordinates_10 = detection[0]
        coordinates_15 = detection[1]
        coordinates_20 = detection[2]
        if coordinates_10 != None:
            if "10" in objects_by_type:
                objects_by_type["10"].append(coordinates_10)
            else:
                objects_by_type["10"] = [coordinates_10]
        if coordinates_15 != None:
            if "15" in objects_by_type:
                objects_by_type["15"].append(coordinates_15)
            else:
                objects_by_type["15"] = [coordinates_15]
        if coordinates_20 != None:
            if "20" in objects_by_type:
                objects_by_type["20"].append(coordinates_20)
            else:
                objects_by_type["20"] = [coordinates_20]  


        coordinates_crosswalk = Crosswalk(img_front)
        if coordinates_crosswalk != None:
            if "crossing" in objects_by_type:
                objects_by_type["crossing"].append(coordinates_crosswalk)
            else:
                objects_by_type["crossing"] = [coordinates_crosswalk]



        
        frame_buffer.append(objects_by_type)

        if len(frame_buffer) == buffer_size:
            output = combine_filter(frame_buffer) # output of the code
            print("internal ", output)
            queue.put(output)
            frame_buffer.clear()
        
