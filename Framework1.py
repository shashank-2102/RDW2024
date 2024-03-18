# import extensions
from ultralytics import YOLO
import cv2
import math

# capture front and back camera
cam_front_index = 0  # set index of front camera
cam_rear_index = 1  # set index of rear camera
cap_front = cv2.VideoCapture(cam_front_index)  # capture front camera
cap_rear = cv2.VideoCapture(cam_rear_index)  # capture rear camera

# setting width and height of camera (pixels)
cap_front.set(3, 640)
cap_front.set(4, 480)
cap_rear.set(3, 640)
cap_rear.set(4, 480)

# input the models
models = [
    YOLO("yolov8n.pt"),
    YOLO("path to traffic sign model.pt"),
    YOLO("path to traffic light model.pt"),
    YOLO("path to zebra crossing model.pt")

]
# classes for each model usually number of classes
classes_list = [
    [0, 1, 2],
    [0, 1, 2, 3, 4],
    [0, 1],
    [0]
]
# names of classes for each model
class_names_list = [
    ["person", "nothing", "car"],
    ["10", "20", "30", "Parking", "Pedestrian"],
    ["green", "red"],
    ["crossing"]

]


# returns the classname for a specific index of the class
def get_class_name(index, model_index):
    classes = classes_list[model_index]
    class_names = class_names_list[model_index]
    if index < len(classes):
        return class_names[index]
    else:
        return 0


# properties of text in frame
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
color = (120, 120, 120)
thickness = 1

# establish loop and read cameras
while True:
    # success is a boolean that indicates if frame was read successfully img is the frame
    success_front, img_front = cap_front.read()
    success_rear, img_rear = cap_rear.read()
    # model_index contains index, model is the actual model
    for model_index, model in enumerate(models):
        # apply model to frame
        results_front = model(img_front, stream=True)

        for results in results_front:
            # boxes gives coordinates of edges of box (bottom left and top right)
            boxes = results.boxes
            # checks if class detected later
            person_detected = False
            front_car_detected = False

            for box in boxes:

                # dislays confidence
                confidence = math.ceil((box.conf[0] * 100)) / 100
                # adding condition for confidence
                if confidence < 0.4:
                    continue
                print("Confidence = ", confidence)

                # prints confidence
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(img_front, (x1, y1), (x2, y2), (255, 0, 255), 3)
                print()

                # prints name of class
                cls = int(box.cls[0])
                class_name = get_class_name(cls, model_index)
                print("Class name = ", class_name)

                if class_name not in ["car", "person", "10", "20", "30", "Parking", "Pedestrian", "green", "red",
                                      "crossing"]:
                    continue

                # useful later
                if class_name == "car":
                    front_car_detected = True
                if class_name == "person":
                    person_detected = True

                org = [x1, y1]

                # prints class and confidence on frame
                text = f"{class_name}: {confidence:.2f}"
                cv2.putText(img_front, text, (x1, y1 - 10), font, fontScale, color, thickness)

    # prints if no detection is made: Useful later for implementing logic
    if not person_detected:
        print("person not detected")
    if not front_car_detected:
        print("car not detected")

    # results rear only checks model with car
    results_rear = models[0](img_rear, stream=True)

    rear_car_detected = False  # track if a car is detected
    # similar steps as in front camera
    for results in results_rear:
        boxes = results.boxes
        for box in boxes:
            cls = int(box.cls[0])
            class_name = get_class_name(cls, 0)  # model index 0 corresponds to the first model

            if class_name != "car":
                continue  # skip to the next detection if the class is a person

            rear_car_detected = True
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence = math.ceil((box.conf[0] * 100)) / 100

            cv2.rectangle(img_rear, (x1, y1), (x2, y2), (255, 0, 255), 3)
            org = [x1, y1]

            text = f"{class_name}: {confidence:.2f}"
            cv2.putText(img_rear, text, (x1, y1 - 10), font, fontScale, color, thickness)

    if not rear_car_detected:
        print("rear car not detected")

        # cv2.imshow('Rear Camera', img_rear)  # display rear camera feed in a window named 'Rear Camera'
    cv2.imshow('Front Camera', img_front)  # display front camera feed in a window named 'Front Camera'

    if cv2.waitKey(1) == ord('q'):
        break

cap_front.release()
cap_rear.release()
cv2.destroyAllWindows()