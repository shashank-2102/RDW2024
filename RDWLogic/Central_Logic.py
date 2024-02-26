def Func1(objectList):
    # Funct1 get constantly recieves all objects
    tSpeed = 0
    lDistance = 0
    for obj in objectList:
        if obj.getDistance() > lDistance:
            lDistance = obj.getDistance()
            tSpeed = obj.getTSpeed()





    return tSpeed, lDistance

def Final_Function():
    pass

