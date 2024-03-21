# import extensions
from ultralytics import YOLO
from collections import deque
from collections import Counter
import cv2
import math 
import keyboard

# capture front and back camera
cam_front_index = 0 # set index of front camera
cam_rear_index = 1 # set index of rear camera
cap_front = cv2.VideoCapture("C:\\Users\\Jandl\\Downloads\\WhatsApp Video 2024-03-11 at 17.10.40.mp4")
cap_rear = cv2.VideoCapture(cam_rear_index)

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
models = [
    YOLO("yolov8n.pt"),
    YOLO("C:\\Users\\Jandl\\Downloads\\trafficlightv1.pt"),
    YOLO("C:\\Users\\Jandl\\Downloads\\trafficlightv1.pt"),
    YOLO("C:\\Users\\Jandl\\Downloads\\trafficlightv1.pt") 
    
]
# classes for each model usually number of classes
classes_list = [
    [0, 1, 2],
    [0, 1, 2],
    [0, 1],     
    [0]    
]
# names of classes for each model
class_names_list = [
    ["person", "nothing", "car"],
    ["10", "20", "30"],
    ["green", "red"],
    ["crossing"]

              
]
    
#buffer
buffer_size = 10
frame_buffer = deque(maxlen=buffer_size)
output = {}

# establish loop and read cameras
while True:
    # success is a boolean that indicates if frame was read successfully img is the frame
    success_front, img_front = cap_front.read()
    success_rear, img_rear = cap_rear.read()

    # removes any detections
    objects_by_type = {}
    # model_index contains index, model is the actual model
    for model_index, model in enumerate(models):
        # apply model to frame
        if model_index == 0:
            results_front = model.predict(img_front, classes=[0, 2], save=True)
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

                #extraction = [class_name, confidence, x1, y1, x2, y2]
                extraction = [x1, y1, x2, y2]
                if class_name in objects_by_type:
                    objects_by_type[class_name].append(extraction)
                else:
                    objects_by_type[class_name] = [extraction]
       
    # results rear only checks model with car
    results_rear = models[0](img_rear, stream=True)
    
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

            if class_name in objects_by_type:
                objects_by_type["rear_car"].append(extraction)
            else:
                objects_by_type["rear_car"] = [extraction]
    
    frame_buffer.append(objects_by_type)
    # If the desired number of frames was combined info is combined
    if len(frame_buffer) == buffer_size:
        output = combine_filter(frame_buffer)
        frame_buffer.clear()
    if keyboard.is_pressed('q'):
        break
cv2.destroyAllWindows()