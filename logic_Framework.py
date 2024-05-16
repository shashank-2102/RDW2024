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
import Speedlimitdetector
import Crossing
from timeit import default_timer as timer

# capture front and back camera
cam_front_index = r"/home/rdw_orin/Desktop/videos/30 Minutes of Cars Driving By in 2009.mp4"   # set index of rear camera
cam_rear_index = r"/home/rdw_orin/Desktop/videos/30 Minutes of Cars Driving By in 2009.mp4"
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

models = [
    YOLO(r"/home/rdw_orin/Desktop/RDW2024-Software-Structure/Models/yolov8n.pt"),
    YOLO(r"/home/rdw_orin/Desktop/RDW2024-Software-Structure/Models/trafficlightv1.pt"), 
    # YOLO("Models\\traffic_light_v1.pt"),
    # YOLO("Models\\zebra_crossing.pt") 
    
]
# classes for each model usually number of classes
classes_list = [
    [0, 1, 2], [0,1]
]

# names of classes for each model
class_names_list = [
    ["person", "nothing", "car"], ["green","red"]
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
    start = timer()
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
                results_front = model(img_front, stream=True,verbose=False)

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
        detection = Speedlimitdetector.speedlimitfinder(img_front)
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


        coordinates_crosswalk = Crossing.Crosswalk(img_front)
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
            end = timer()
            print("time taken for", buffer_size, "frames:", end - start)
            start = timer()
