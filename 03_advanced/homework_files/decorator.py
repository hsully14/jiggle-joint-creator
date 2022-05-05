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

from datetime import datetime

#*********************************************************************
# DECORATOR


def print_process(func):
    def wrapper(*args, **kwargs):
        # get name of function
        function_name = func.__name__

        # start timer count
        start_time = datetime.now()

        # print function running next
        print("START: {} ----------".format(function_name))

        # main function call
        func(*args)

        # count up time and finish wrapper call
        end_time = (datetime.now() - start_time)
        print("END {} ----------".format(end_time))

    return wrapper


#*********************************************************************
# FUNC

@print_process
def shortest_sleeping():
    print("so sleepy")


@print_process
def short_sleeping(test):
    time.sleep(.1)
    print(test)


@print_process
def mid_sleeping():
    time.sleep(2)


@print_process
def long_sleeping():
    time.sleep(4)
