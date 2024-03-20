def priorityDecider(objectList):
    tSpeed = 0
    lDistance = float('inf')

    
    for obj in objectList:
        if obj.getDistance() < lDistance:
            lDistance = obj.getDistance()
            tSpeed = obj.getTSpeed()

    return [tSpeed, lDistance]


def Final_Function(objectList, overtaking_mode:bool, lane_keeping):
    
    sAngle = lane_keeping.getsAngle()

    if overtaking_mode:
        tSpeed, lDistance = [123, 123]

    else:
        # Normal mode
        tSpeed, lDistance = priorityDecider(objectList)
    

    print(f"tSpeed: {tSpeed}, lDistance: {lDistance}, sAngle: {sAngle}, overtaking_mode: {overtaking_mode}")



