# Given a frame, an area and different classes returns the closest class
# input [[object name, coordinates], [object name, coordinates],...]
def Calculate_area(objects):
    closestobject = None
    maxarea = 0
    area = None
    for object in objects:
        if object[0]=='traffic light':
            area = (object[3]-object[1])*(object[4]-object[2])/(0.3*0.1)
            if area > maxarea:
                closestobject = 'traffic light'
                maxarea = area
        elif object[0]=='speed sign':
            area = ((object[3]-object[1])*(object[4]-object[2])/(0.6*0.6))
            if area > maxarea:
                closestobject = 'speed sign'
                maxarea = area
        elif object[0]=='zebra crossing':
            area = ((object[3]-object[1])*(object[4]-object[2])/(2*3))
            if area > maxarea:
                closestobject = 'zebra crossing'
                maxarea = area
        else:
            print('other object detected') #debugging statement
    print(closestobject, maxarea)
    #return closestobject, maxarea
    return maxarea

Calculate_Distance([['traffic light',0.5,0.5,0.6,0.6],['speed sign',0.7,0.5,0.9,0.6],['zebra crossing',0.2,0.1,0.3,0.2]])