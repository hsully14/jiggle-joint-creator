# ADVANCED ***************************************************************************
# content = assignment
#
# date    = 2022-01-07
# email   = contact@alexanderrichtertd.com
#************************************************************************************


"""
0. CONNECT the decorator with all functions. Print START and END before and after.

START
main_function
END



1. Print the processing time of all sleeping func

END - 00:00:00



2. PRINT also the name of the function

START - long_sleeping



3. INCLUDE a decorator into your own application
"""


import time


#*********************************************************************
# DECORATOR
def print_process(func):
    def wrapper(*args, **kwargs):
        func(arg)                  # main_function
    return wrapper


#*********************************************************************
# FUNC
@print_process
def short_sleeping(test):
    time.sleep(.1)
    print(test)

def mid_sleeping():
    time.sleep(2)

def long_sleeping():
    time.sleep(4)

short_sleeping("so sleepy")
