from panda3d import egg
from panda3d.core import Filename, GeomVertexReader
from math import sqrt
from pprint import pprint
class Vertex:
    def __init__(self, vector):
        self._x = vector.getX()
        self._y = vector.getY()
        self._z = vector.getZ()
        pass
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

colonne = set()

while not reader.isAtEnd():
    colonne.add(reader.getData3().getX())
    pass

colonne = list(colonne)
colonne.sort()
pprint(colonne)
print("Ignora il primo risultato")
print(len(colonne))
p = -100
count = 0
for x in colonne:
    diff = p-x
    print(diff)
    if abs(diff) < 0.00000015:  # controllo errore macchina
        count += 1
    p = x

print(count)
