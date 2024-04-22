import multiprocessing
from Traffic_Light import Traffic_Light
from Lane_Keeping_Maneouvre import Lane_Keeping_Maneouvre
from Pedestrian_Manoeuvre import Pedestrian_Maneouvre
from Speed_Limit import Speed_Limit

# Global :)
objectList = []

global traffic_light_instance, speed_limit_instance, pedestrian_instance
traffic_light_instance = Traffic_Light()
speed_limit_instance = Speed_Limit()
pedestrian_instance = Pedestrian_Maneouvre()

def updateObjectList(obj, remove=False):
    global objectList
    objectList.append(obj)

def clearObjectList():
    global objectList
    objectList = []

def getObjectList():
    global objectList
    return objectList

def priorityDecider(objectList):
    tSpeed = 0
    lDistance = float('inf')
    
    for obj in objectList:
        if obj.getDistance() < lDistance:
            lDistance = obj.getDistance()
            tSpeed = obj.getTSpeed()

    return [tSpeed, lDistance]

def finalFunction(objectList, overtaking_mode:bool, lane_keeping):
    sAngle = lane_keeping.getsAngle()

    if overtaking_mode: #complete
        tSpeed, lDistance = [123, 123]
        sAngle = 0
    else:
        # Normal mode
        tSpeed, lDistance = priorityDecider(objectList)

    print(f"tSpeed: {tSpeed}, lDistance: {lDistance}, sAngle: {sAngle}, overtaking_mode: {overtaking_mode}")
    return [tSpeed, lDistance, sAngle]

def receive_data(queue):
    while True:
        data = queue.get() 
        print("Received data:", data)  
        process_data_temp(data)
        #process_data(data)
        #save_data(data)

def process_data(data):
    actions = {
        'person': lambda value: (pedestrian_instance.pedestrian_logic(value), updateObjectList(pedestrian_instance)),
        'crossing': lambda value: (pedestrian_instance.pedestrian_logic(value), updateObjectList(pedestrian_instance)),
        '10': lambda value: (speed_limit_instance.speed_sign(10, value), updateObjectList(speed_limit_instance)),
        '15': lambda value: (speed_limit_instance.speed_sign(15, value), updateObjectList(speed_limit_instance)),
        '20': lambda value: (speed_limit_instance.speed_sign(20, value), updateObjectList(speed_limit_instance)),
        'red': lambda value: (traffic_light_instance.TL_Logic('red', value), updateObjectList(traffic_light_instance)),
        'green': lambda value: (traffic_light_instance.TL_Logic('green', value), updateObjectList(traffic_light_instance), print(getObjectList())),
        'car': lambda value: print("Car at:", value), #overtaking
        'rear_car': lambda value: print("Rear car at:", value) #overtaking
    }
    for key, value in data.items():
        if key in actions:
            if value:  # Check if the list is not empty
                actions[key](value)
        else:
            print(f"Unrecognized key: {key}")
        
def process_data_temp(data):
    actions = {
        'person': lambda value: print("Person at:", value),
        'crossing': lambda value: print("Crossing at:", value),
        '10': lambda value: print("Speed 10 at:", value),
        '15': lambda value: print("Speed 15 at:", value),
        '20': lambda value: print("Speed 20 at:", value),
        'red': lambda value: print("Red TL at:", value),
        'green': lambda value: print("Green TL at:", value),
        'car': lambda value: print("Car at:", value),
        'rear_car': lambda value: print("Rear car at:", value)
    }
    for key, value in data.items():
        if key in actions:
            if value:  # do if list not empty
                actions[key](value)
        else:
            print(f"Unrecognized key: {key}")
        


def save_data(data):
    with open("output1.txt", "a") as file:
        file.write(str(data) + "\n")



if __name__ == "__main__":
    
    traffic_light_instance = Traffic_Light()
    speed_limit_instance = Speed_Limit()
    pedestrian_instance = Pedestrian_Maneouvre()

    # create  multiprocessing Queue
    queue = multiprocessing.Queue()

    # start  receiver process
    receiver_process = multiprocessing.Process(target=receive_data, args=(queue,))
    receiver_process.start()

    # to keep the receiver process running
    receiver_process.join()
