class Traffic_Light:
    _distance = 0
    _Go = False
    def __init__(self):
        # Logic
        self.__lane_keeping_maneouvre = None

    def getTSpeed(self):
        return self._Go

    def getDistance(self):
        return self._distance


