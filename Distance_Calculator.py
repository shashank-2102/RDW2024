# Given a frame returns area
# input [object name, coordinates]
def Calculate_area(object):
    area = None

    if object[0]=='traffic light':
        area = (object[3]-object[1])*(object[4]-object[2])/(0.3*0.1)

    elif object[0]=='speed sign':
        area = ((object[3]-object[1])*(object[4]-object[2])/(0.6*0.6))

    elif object[0]=='zebra crossing':
        area = ((object[3]-object[1])*(object[4]-object[2])/(2*3))

    else:
        print('other object detected') #debugging statement

    #print(area, object[0])
    return [area, object[0]] #return

#Calculate_area(['traffic light',0.5,0.5,0.6,0.6])