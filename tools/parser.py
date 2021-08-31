from panda3d import egg
from panda3d.core import Filename
from math import sqrt

class Vertex:
    def __init__(self, x, y):
        self._x = x
        self._y = y
        pass
    pass


geom = egg.loadEggFile("./mesh_full.egg").getChild(0).getGeom(0)

# help(geom)

from pprint import pprint

primitive = geom.getPrimitive(0)

vdata = geom.getVertexData()

polygons_per_edge = int(sqrt(vdata.getNumRows()) - 1)

print(polygons_per_edge**2)

