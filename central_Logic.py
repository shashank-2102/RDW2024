import multiprocessing

# Global :)
objectList = []


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
        data = queue.get()  # Get data from the queue
        print("Received data:", data)  # Print the received data
        process_data(data)
        save_data(data)

def process_data(data):
    # Add your data processing logic here
    print("Processing received data:", data)

def save_data(data):
    with open("output1.txt", "a") as file:
        file.write(str(data) + "\n")

if __name__ == "__main__":
    # Create a multiprocessing Queue
    queue = multiprocessing.Queue()

    # Start the receiver process
    receiver_process = multiprocessing.Process(target=receive_data, args=(queue,))
    receiver_process.start()

    # Keep the receiver process running
    receiver_process.join()