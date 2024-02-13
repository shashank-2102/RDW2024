# Video capture code
# import extensions
from ultralytics import YOLO
import cv2
import math

# Input the models
models = [
    YOLO("yolov8n.pt"),
    #YOLO("traffic sign model location.pt"),
    #YOLO("traffic light model location.pt"),
    #YOLO("zebra crossing location.pt")
]

# Classes for each model usually number of classes yolov8n has more
classes_list = [
    [0, 1, 2],
    [0, 1, 2, 3, 4],
    [0, 1],
    [0]
]

# Names of classes for each model
class_names_list = [
    ["person", "nothing", "car"],
    ["10", "20", "30", "Parking", "Pedestrian"],
    ["green", "red"],
    ["crossing"]
]

# Returns the classname for a specific index of the class
def get_class_name(index, model_index):
    classes = classes_list[model_index]
    class_names = class_names_list[model_index]
    if index < len(classes):
        return class_names[index]
    else:
        return 0

# Read the video file
video_path = "Path to video.mp4"
cap = cv2.VideoCapture(video_path)

# Define the codec and create VideoWriter object
output_path = "Path if output.avi"
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output_path, fourcc, 20.0)  # Adjust the parameters as needed

while True:
    # Read a frame from the video
    success, frame = cap.read()

    # Break the loop if the video is finished
    if not success:
        break

    # Model evaluation for each model
    for model_index, model in enumerate(models):
        results = model(frame)

        # Apply model to frame
        for results_per_model in results:
            # Boxes give coordinates of edges of box (bottom left and top right)
            boxes = results_per_model.boxes

            for box in boxes:
                # Displays confidence above a threshold
                confidence = math.ceil((box.conf[0] * 100)) / 100
                # if confidence < threshold:
                #    continue

                # Prints confidence
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

                # Prints name of class
                cls = int(box.cls[0])
                class_name = get_class_name(cls, model_index)

                # For yolo model containing more categories
                if class_name not in ["car", "person", "10", "20", "30", "Parking", "Pedestrian", "green", "red", "crossing"]:
                    continue

                org = [x1, y1]

                # Prints class and confidence on frame
                text = f"{class_name}: {confidence:.2f}"
                cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # Write the frame to the output video file
        out.write(frame)

# Release the video capture object, VideoWriter object, and close all windows
cap.release()
out.release()
cv2.destroyAllWindows()