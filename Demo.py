import cv2
import math
import keyboard  # Ensure this is necessary, it may require elevated permissions
import multiprocessing
import time
import numpy as np
from ultralytics import YOLO
from collections import deque, Counter
from central_Logic import receive_data  # Ensure this module is in your path
import torch
import Crossing  # Ensure this module is in your path
from timeit import default_timer as timer

# Initialize front camera
cap_front = cv2.VideoCapture(0)

# Set camera resolution
cap_front.set(3, 640)
cap_front.set(4, 480)

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
            self.classes[class_name] = coords

# Combine and filter buffer data
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

# Get class name by index
def get_class_name(index, model_index):
    classes = classes_list[model_index]
    class_names = class_names_list[model_index]
    if index < len(classes):
        return class_names[index]
    else:
        return 0

# Load models
models = [
    YOLO("yolov8n.pt"),
    YOLO("C:\\Users\\Jandl\\Downloads\\trafficlightv1.pt"),
]

# Classes and class names for each model
classes_list = [[0, 1, 2], [0, 1]]
class_names_list = [["person", "nothing", "car"], ["green", "red"]]

# Initialize buffer
buffer_size = 10
frame_buffer = deque(maxlen=buffer_size)
output = {}

def send_data(queue):
    while True:
        pass

if __name__ == '__main__':
    print("Creating queue")
    print("CUDA", torch.cuda.is_available())
    
    queue = multiprocessing.Queue()
    
    sender_process = multiprocessing.Process(target=send_data, args=(queue,))
    sender_process.start()
    
    receiver_process = multiprocessing.Process(target=receive_data, args=(queue,))
    receiver_process.start()
    
    start = timer()
    while True:
        success_front, img_front = cap_front.read()
        objects_by_type = {}

        for model_index, model in enumerate(models):
            if model_index == 0:
                results_front = model.predict(img_front, classes=[0, 2], save=False, verbose=False)
            else:
                results_front = model(img_front, stream=True, verbose=False)

            for results in results_front:
                boxes = results.boxes
                for box in boxes:
                    confidence = math.ceil((box.conf[0] * 100)) / 100
                    if confidence < 0.4:
                        continue

                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cls = int(box.cls[0])
                    class_name = get_class_name(cls, model_index)
                    extraction = [x1, y1, x2, y2]
                    if class_name in objects_by_type:
                        objects_by_type[class_name].append(extraction)
                    else:
                        objects_by_type[class_name] = [extraction]
        
        coordinates_crosswalk = Crossing.Crosswalk(img_front)
        #if coordinates_crosswalk:
        #    if "crossing" in objects_by_type:
         #       objects_by_type["crossing"].append(coordinates_crosswalk)
          #  else:
           #     objects_by_type["crossing"] = [coordinates_crosswalk]

        # Draw bounding boxes on the frame
        for class_name, coords_list in objects_by_type.items():
            for (x1, y1, x2, y2) in coords_list:
                cv2.rectangle(img_front, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Blue box with thickness 2
                cv2.putText(img_front, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)  # Blue text
        
        # Show the output frame
        cv2.imshow('Camera Output', img_front)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap_front.release()
    cv2.destroyAllWindows()


        
       
