# Global 
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



