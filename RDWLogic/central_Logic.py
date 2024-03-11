def Func1(objectList):
    tSpeed = 0
    lDistance = float('inf') 
    for obj in objectList:
        if obj.getDistance() < lDistance:
            lDistance = obj.getDistance()
            tSpeed = obj.getTSpeed()

    return [tSpeed, lDistance]



def Final_Function():
    pass



