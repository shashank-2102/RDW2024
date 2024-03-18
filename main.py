# This is the top level file for the project. It is the file that should be run to start the program.
# It is responsible to call and control all other files and classes.
from RT import RT
# from FrameWork_Thread.Framework1 import FrameWork1
from threading import Thread
from central_Logic import Func1
from time import sleep

def framework():
    for i in range(10):
        print(1)
        sleep(1)
    #Here call the framework
    # framework = FrameWork1()
    # framework.run()
    pass
def  logic():
    for i in range(10):
        print(2)
        sleep(1)
    # Here call main logic
    # logic = RT()
    pass


if __name__ == "__main__":


    Thread(target = framework).start()
    Thread(target = logic).start()




def check_update():
    #Check if the framework has updated any of the values
    pass
