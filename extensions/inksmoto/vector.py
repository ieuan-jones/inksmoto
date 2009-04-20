#!/usr/bin/python
"""
Copyright (C) 2006,2009 Emmanuel Gorse, e.gorse@gmail.com

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

from math import sqrt, atan2, cos, sin, radians

class Vector:
    def __init__(self, *args):
        nbArgs = len(args)
        if nbArgs == 0:
            self.vector = [0, 0]
        elif nbArgs == 1:
            self.vector = args[0]
        elif nbArgs == 2:
            self.vector = [args[0], args[1]]
        else:
            raise Exception("Vector::__init__::wrong parameters: %s"
                            % (str(args)))

    def x(self):
        return self.vector[0]
    
    def y(self):
        return self.vector[1]
    
    def length(self):
        return sqrt(self.vector[0]*self.vector[0]
                    + self.vector[1]*self.vector[1])
    
    def dot(self, v):
        result = 0.0
        for x, y in zip(self.vector, v.vector):
            result += x * y
        return result

    def angle(self, v):
        """ the old formula (with acos) handles only angles between 1
            and 180 degrees, the one with atan2 handles every angles
            atan2(v2.y,v2.x) - atan2(v1.y,v1.x)
            see http://www.euclideanspace.com/maths/algebra/vectors/angleBetween/index.htm
        """
        return atan2(v.y(), v.x()) - atan2(self.y(), self.x())

    def normal(self):
        return Vector(-self.vector[1], self.vector[0])

    def rotate(self, angle):
        # x' = x*cos(a) - y*sin(a)
        # y' = x*sin(a) + y*cos(a)
        angle = radians(angle)
        cosAngle = cos(angle)
        sinAngle = sin(angle)
        return Vector(self.x() * cosAngle - self.y() * sinAngle,
                      self.x() * sinAngle + self.y() * cosAngle)

    def __str__(self):
        return str(self.vector)
