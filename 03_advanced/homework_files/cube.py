# ADVANCED ***************************************************************************
# content = assignment
#
# date    = 2022-01-07
# email   = contact@alexanderrichtertd.com
#************************************************************************************

"""
CUBE CLASS

1. CREATE an abstract class "Cube" with a variabale name and the functions:
   translate(x, y, z), rotate(x, y, z), scale(x, y, z) and color(R, G, B)
   All functions print out and store the data in the cube (translate, rotate, scale and color)

2. CREATE 3 cube objects with different names (use __init__(name)).

3. ADD the function print_status() which prints all the variables nicely formatted.

4. ADD the function update_transform(ttype, value).
   "ttype" can be "translate", "rotate" and "scale" while "value" is a list of 3 floats: e.g. [1.2, 2.4 ,3.7]
   This function should trigger either the translate, rotate or scale function.

   BONUS: Can you do it without ifs?

5. CREATE a parent class "Object" which has a name, translate, rotate and scale.
   Use Object as the parent for your cube class.
   Update the cube class to not repeat the content of Object.

NOTE: Upload only the final result.

"""


class Object(object):
    # inherits from base class object to get super() method
    def __init__(self, name):
        # initialize class object with name and transform values
        self.name = name
        self.translation = [0.0, 0.0, 0.0]
        self.rotation = [0.0, 0.0, 0.0]
        self.scaling = [0.0, 0.0, 0.0]

    def _set_translate(self, translation_values):
        '''Updates and prints new translation values from given list'''
        self.translation = translation_values
        # print input values
        print('Translate values set to: X:{} Y:{} Z:{}'.format(self.translation[0],
                                                               self.translation[1],
                                                               self.translation[2]))

    def _set_rotate(self, rotation_values):
        '''Updates and prints new rotation values from given list'''
        self.rotation = rotation_values
        # print input values
        print('Rotate values set to: X:{} Y:{} Z:{}'.format(self.rotation[0],
                                                            self.rotation[1],
                                                            self.rotation[2]))

    def _set_scale(self, scale_values):
        '''Updates and prints new scale values from given list'''
        self.scaling = scale_values
        # print input values
        print('Scale values set to: X:{} Y:{} Z:{}'.format(self.scaling[0],
                                                           self.scaling[1],
                                                           self.scaling[2]))

    def _print_status(self):
        '''Prints out data on object naming and transforms'''
        print('This object\'s name is: {}'.format(self.name))
        print('Translate values are: X:{}, Y:{}, Z:{}'.format(self.translation[0],
                                                              self.translation[1],
                                                              self.translation[2]))
        print('Rotate values are: X:{}, Y:{}, Z:{}'.format(self.rotation[0],
                                                           self.rotation[1],
                                                           self.rotation[2]))
        print('Scale values are: X:{}, Y:{}, Z:{}'.format(self.scaling[0],
                                                          self.scaling[1],
                                                          self.scaling[2]))

    def _update_transform(self, ttype, value):
        '''Updates object transforms on given transform type using values list'''

        transform_actions = {'translate' : self.set_translate,
                             'rotate' : self.set_rotate,
                             'scale' : self.set_scale}

        transform_actions[ttype](value)


class Cube(Object):

    def __init__(self, name):
        # use super() to get init setup from Object parent class
        super(Cube, self).__init__(name)
        # add new value in subclass
        self.coloring = [0.0, 0.0, 0.0]

    def _set_color(self, color_values):
        '''Updates and prints new color values from given list'''
        self.coloring = color_values
        # print input values
        print('Color values set to: R:{} G:{} B:{}'.format(self.coloring[0],
                                                           self.coloring[1],
                                                           self.coloring[2]))

    def _print_status(self):
        '''Prints out data on cube object naming and transforms. Overwritten from Object'''
        print('This cube\'s name is: {}'.format(self.name))
        print('Translate values are: X:{}, Y:{}, Z:{}'.format(self.translation[0],
                                                              self.translation[1],
                                                              self.translation[2]))
        print('Rotate values are: X:{}, Y:{}, Z:{}'.format(self.rotation[0],
                                                           self.rotation[1],
                                                           self.rotation[2]))
        print('Scale values are: X:{}, Y:{}, Z:{}'.format(self.scaling[0],
                                                          self.scaling[1],
                                                          self.scaling[2]))
        print('Color values are: R:{}, G:{}, B:{}'.format(self.coloring[0],
                                                          self.coloring[1],
                                                          self.coloring[2]))
