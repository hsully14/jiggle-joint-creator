# STYLE ***************************************************************************
# content = assignment
#
# date    = 2022-01-07
# email   = contact@alexanderrichtertd.com
# ************************************************************************************

# original: logging.init.py

def findCaller(self):
    """
    Find the stack frame of the caller so that we can note the source
    file name, line number and function name.
    """
    
    # On some versions of IronPython, currentframe() returns None if
    # IronPython isn't run with -X:Frames.
    current_frame = currentframe()

    if current_frame:
        current_frame = current_frame.f_back

    rv = "(unknown file)", 0, "(unknown function)"

    while hasattr(current_frame, "f_code"):
        frame_code = current_frame.f_code
        filename = os.path.normcase(frame_code.co_filename)

        if filename == _srcfile:
            current_frame = current_frame.f_back
            continue
        rv = (frame_code.co_filename, current_frame.f_lineno, frame_code.co_name)
        break

    return rv

# How can we make this code better?
# Question - I see the example solution in the book. I'm unclear on what rv is doing and why we need to edit it 
# as seen in the example. 