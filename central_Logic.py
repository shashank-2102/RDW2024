import multiprocessing
from Traffic_Light import Traffic_Light
from Pedestrian_Manoeuvre import Pedestrian_Maneouvre
from Speed_Limit import Speed_Limit

# Global :)
objectList = []
e_STOP = False ###########ADD LOGIC#############

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

def get_e_STOP():
    return e_STOP

def finalFunction(objectList, overtaking_mode:bool, e_STOP:bool):
    if e_STOP: 
        return [0, 0, True]
    
    if overtaking_mode: #complete
        tSpeed, lDistance = [69, 69]
    else:
        # Normal mode
        tSpeed, lDistance = priorityDecider(objectList)

    print(f"tSpeed: {tSpeed}, lDistance: {lDistance}, overtaking_mode: {overtaking_mode}, eSTOP: {e_STOP}")
    return [tSpeed, lDistance, overtaking_mode, e_STOP]

def receive_data(queue):
    while True:
        data = queue.get() 
        #print("Received data:", data)   #########ENABLE IF YOU WAN TO SEE RECIEVED DATA##########
        #process_data_temp(data)
        process_data(data)
        #save_data(data)

def process_data(data):
    for key, value in data.items():
        actions = {
        'person': lambda value: (pedestrian_instance.person_logic(value), updateObjectList(pedestrian_instance)),
        'crossing': lambda value: (pedestrian_instance.crossing_logic(value), updateObjectList(pedestrian_instance)),
        '10': lambda value: (speed_limit_instance.speed_sign(10, value), updateObjectList(speed_limit_instance)),
        '15': lambda value: (speed_limit_instance.speed_sign(15, value), updateObjectList(speed_limit_instance)),
        '20': lambda value: (speed_limit_instance.speed_sign(20, value), updateObjectList(speed_limit_instance)),
        'red': lambda value: (traffic_light_instance.TL_Logic('red', value), updateObjectList(traffic_light_instance)),
        'green': lambda value: (traffic_light_instance.TL_Logic('green', value), updateObjectList(traffic_light_instance)),
        'car': lambda value: print("Car at:", value), #overtaking
        'rear_car': lambda value: print("Rear car at:", value) #overtaking
        }
        if key in actions:
            if value:  # Check if the list is not empty
                actions[key](value)
        else:
            print(f"Unrecognized key: {key}")
    print("Object List:", getObjectList())
    finalFunction(getObjectList(), False, get_e_STOP())
    clearObjectList()
    #print("Object List after clearing:", getObjectList())

        
def process_data_temp(data):
    for key, value in data.items():
        actions = {
        'person': lambda value: print("Person at:", value),
        #'person': (traffic_light_instance.TL_Logic('red', value), updateObjectList(traffic_light_instance)),
        'crossing': lambda value: print("Crossing at:", value),
        '10': lambda value: print("Speed 10 at:", value),
        '15': lambda value: print("Speed 15 at:", value),
        '20': lambda value: print("Speed 20 at:", value),
        'red': lambda value: print("Red TL at:", value),
        'green': lambda value: print("Green TL at:", value),
        'car': lambda value: print("Car at:", value),
        #'car': lambda value: (traffic_light_instance.TL_Logic('green', value), updateObjectList(traffic_light_instance)),
        'rear_car': lambda value: print("Rear car at:", value)
        }

        if key in actions:
            if value:  # do if list not empty
                actions[key](value)
        else:
            print(f"Unrecognized key: {key}")
    print("Object List:", getObjectList())
    clearObjectList()
    print("Object List after clearing:", getObjectList())
        
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
