# This is the top level file for the project. It is the file that should be run to start the program.
# It is responsible to call and control all other files and classes.
from RT import RT


if __name__ == "__main__":

    process = RT("FOO")
    process.value = "BAR"
    print(process.value)
    process = RT("a")
    print(process.value)
    #Need to make framwork and Logic work on distinct threads
    # IMPORTANT: Only allowed to query from the framework


def check_update():
    #Check if the framework has updated any of the values
    pass
