from panda3d import egg
from panda3d.core import Filename, GeomVertexReader, Vec3
from math import sqrt
from pprint import pprint


class Vertex:
    TOLLERANCE_X = .00001
    TOLLERANCE_Y = .00001
    TOLLERANCE_Z = .001
    
    coords_x = set()
    coords_y = set()
    coords_z = set()
    def __init__(self, vector: Vec3):

        closer = self.getCloserX(vector.getX())

        if closer[1] < Vertex.TOLLERANCE_X:
            self._x = closer[0]
        else:
            Vertex.coords_x.add(vector.getX())
            self._x = vector.getX()

            
        closer = self.getCloserY(vector.getY())
        if closer[1] < Vertex.TOLLERANCE_Y:
            self._y = closer[0]
        else:
            Vertex.coords_y.add(vector.getY())
            self._y = vector.getY()

            
        closer = self.getCloserZ(vector.getZ())
        if closer[1] < Vertex.TOLLERANCE_Z:
            self._z = closer[0]
        else:
            Vertex.coords_z.add(vector.getZ())
            self._z = vector.getZ()
        pass
    

    def __repr__(self):
        return f"Vector({self._x},{self._y},{self._z})"

    def __lt__(self, other: "Vertex"):
        return self._y <= other._y and self._x < other._y


    @staticmethod
    def getCloserX(val):
        dist = 100
        closer = 0
        for coord_x in Vertex.coords_x:
            distance = abs(val-coord_x)
            if distance < dist:
                closer = coord_x
                dist = distance
                pass
            pass
        return closer, dist

    @staticmethod
    def getCloserY(val):
        dist = 100
        closer = 0
        for coord_y in Vertex.coords_y:
            distance = abs(val-coord_y)
            if distance < dist:
                closer = coord_y
                dist = distance
                pass
            pass
        return closer, dist


    @staticmethod
    def getCloserZ(val):
        dist = 100
        closer = 0
        for coord_z in Vertex.coords_z:
            distance = abs(val-coord_z)
            if distance < dist:
                closer = coord_z
                dist = distance
                pass
            pass
        return closer, dist
    
    pass


geom = egg.loadEggFile("./mesh_full.egg").getChild(0).getGeom(0)

# help(geom)

from pprint import pprint

primitive = geom.getPrimitive(0)

vdata = geom.getVertexData()

polygons_per_edge = int(sqrt(vdata.getNumRows()) - 1)

# print(polygons_per_edge**2)

print(vdata.getNumRows())

reader = GeomVertexReader(vdata, "vertex")

vertexPool = list()

while not reader.isAtEnd():
    vertexPool.append(Vertex(reader.getData3()))
    pass

print(len(Vertex.coords_x))
print(len(Vertex.coords_y))
print(len(Vertex.coords_z))


print("################")

print(Vertex(Vec3(0, 0, 0)) < Vertex(Vec3(1, 1, 1)))
