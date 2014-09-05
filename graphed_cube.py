"""

Another type of simulating a Rubik's Cube.
Using graphs.

"""

from __future__ import print_function

from functools import reduce

from collections import namedtuple
Square = namedtuple("Square", ["uid", "colour"])
Square.type = "square"
Cuboid = namedtuple("Cuboid", ["x", "y", "z"])
Cuboid.type = "cuboid"

from re import sub

from colorama import init, Back
init()

__relations__ = {
    (-1, -1, -1) : [6 , 53, 33], 
    (-1, -1,  0) : [7 , 30], 
    (-1, -1,  1) : [8 , 24, 27], 
    (-1,  0, -1) : [3 , 50], 
    (-1,  0,  0) : [4], 
    (-1,  0,  1) : [5 , 21], 
    (-1,  1, -1) : [0 ,  9, 47], 
    (-1,  1,  0) : [1 , 12], 
    (-1,  1,  1) : [2 , 15, 18], 
    (0 , -1, -1) : [52, 34], 
    (0 , -1,  0) : [31], 
    (0 , -1,  1) : [25, 28], 
    (0 ,  0, -1) : [49], 
    (0 ,  0,  0) : [], 
    (0 ,  0,  1) : [22], 
    (0 ,  1, -1) : [10, 46], 
    (0 ,  1,  0) : [13], 
    (0 ,  1,  1) : [16, 19], 
    (1 , -1, -1) : [35, 44, 51], 
    (1 , -1,  0) : [32, 43], 
    (1 , -1,  1) : [26, 29, 42], 
    (1 ,  0, -1) : [41, 48], 
    (1 ,  0,  0) : [40], 
    (1 ,  0,  1) : [23, 39], 
    (1 ,  1, -1) : [11, 38, 45], 
    (1 ,  1,  0) : [14, 37], 
    (1 ,  1,  1) : [17, 20, 36]
}

class Cube:
    """A cuboid based Rubik's Cube."""
    def __init__(self, colours=reduce(lambda x,y:x+y, map(lambda x:[x]*9, "LUFDRB"))):
        self.cube_g = {}
        for x in range(-1, 2):
            for y in range(-1, 2):
                for z in range(-1, 2):
                    key = Cuboid(x, y, z)
                    self.cube_g[key] = set()
                    for axis in "xyz":
                        for j in [-1, 1]:
                            if abs(eval("key.{} + j".format(axis))) != 2:
                                neighbor = eval("key._replace({0}=key.{0}+j)".format(axis))
                                self.cube_g[key].add(neighbor)
                    for index in __relations__[key]:
                        _key = Square(index, colours[index])
                        self.cube_g[key].add(_key)
                        self.cube_g[_key] = set([key])
        for i in range(6):
            for j in range(9):
                key = Square(i*9+j, colours[i*9+j])
                for check, val in [("j+3<9", 3), ("(j+1)%3 != 0", 1)]:
                    if eval(check):
                        _key = Square(key.uid+val, colours[key.uid+val])
                        self.cube_g[key].add(_key)
                        self.cube_g[_key].add(key)

    def __repr__(self):
        result = ""
        for i in range(3):
            result += Back.RESET + "       "
            result += self["FROM SQUARES"]

    def __getitem__(self, query):
        """
        This can filter the cube graph.

        Cube[{ "key" : ["its.colour == 'R'"] , "nbr" : ["its.type == 'cuboid'"] }] =>

        {Square(uid=36, colour='R'): {Cuboid(x=1, y=1, z=1)},
         Square(uid=37, colour='R'): {Cuboid(x=1, y=1, z=0)},
         Square(uid=38, colour='R'): {Cuboid(x=1, y=1, z=-1)},
         Square(uid=39, colour='R'): {Cuboid(x=1, y=0, z=1)},
         Square(uid=40, colour='R'): {Cuboid(x=1, y=0, z=0)},
         Square(uid=41, colour='R'): {Cuboid(x=1, y=0, z=-1)},
         Square(uid=42, colour='R'): {Cuboid(x=1, y=-1, z=1)},
         Square(uid=43, colour='R'): {Cuboid(x=1, y=-1, z=0)},
         Square(uid=44, colour='R'): {Cuboid(x=1, y=-1, z=-1)}}
        """
        _query = {"key":[], "nbr":[]}
        _query.update(query)
        result = dict(zip(self.cube_g.keys(), map(lambda x:x.copy(), self.cube_g.values())))
        deleted = set()
        for exp in _query["key"]:
            for its in self.cube_g:
                if its not in deleted:
                    try:
                        if not eval(exp):
                            deleted.add(its)
                    except AttributeError:
                        deleted.add(its)
        for obj in deleted:
            del result[obj]
        for key in result:
            deleted = set()
            for exp in _query["nbr"]:
                for its in result[key]:
                    if its not in deleted:
                        try:
                            if not eval(exp):
                                deleted.add(its)
                        except AttributeError:
                            deleted.add(its)
            for obj in deleted:
                result[key].remove(obj)
        return result


if __name__ == "__main__":
    a = Cube()
    print(a[{"key": ["its.colour == 'R'"], "nbr": ["its.type == 'cuboid'"]}])
