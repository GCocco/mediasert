from panda3d import egg
from panda3d.core import Filename, GeomVertexReader, Vec3
from math import sqrt
from pprint import pprint

ENABLELOG = True

fp = None
if ENABLELOG:
    fp = open("./.log.txt", "w")

def log(*args):
    if ENABLELOG:
        fp.write(str(args) + "\n")


class Vertex:
    TOLERANCE_X = .000000125
    TOLERANCE_Y = .000000125
    TOLERANCE_Z = .000001
    
    coords_x = set()
    coords_y = set()
    coords_z = set()


    ordered_coors_x = list()
    
    
    map_X = dict()
    
    def __init__(self, vector: Vec3):

        # X
        val = vector.getX()
        closer = self.getCloserX(val)

        if closer[1] < Vertex.TOLERANCE_X:
            self._x = closer[0]
        else:
            Vertex.coords_x.add(val)
            Vertex.ordered_coors_x = sorted(Vertex.coords_x)
            self._x = val

        # Y
        val = vector.getY()
        closer = self.getCloserY(val)
        
        if closer[1] < Vertex.TOLERANCE_Y:
            self._y = closer[0]
        else:
            Vertex.coords_y.add(val)
            self._y = val

        # Z
        val = vector.getZ()
        closer = self.getCloserZ(val)
        if closer[1] < Vertex.TOLERANCE_Z:
            self._z = closer[0]
        else:
            Vertex.coords_z.add(val)
            self._z = val


        self._next = None
        self.sort()
        pass


    def sort(self):
        if self._x in Vertex.map_X:

            head = Vertex.map_X[self._x]
            if self._y < head._y:
                Vertex.map_X[self._x] = self
                self._next = head
                return
            else:
                last = head
                while head._next:
                    if head._next._y > self._y:
                        break
                    head = head._next
                    pass
                self._next = head._next
                head._next = self
                pass
            pass

        else:
            Vertex.map_X[self._x] = self
            pass
        pass


    def as_list(self, tail=None):
        if tail:
            tail.append(self)
        else:
            tail = [self]
        if self._next:
            return self._next.as_list(tail=tail)
        return tail
    
    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    def __repr__(self):
        return f"Vector({self._x},{self._y},{self._z})"

    def __lt__(self, other):
        if self._x <= other._x:
            return self._y < other._y
        return False

    @staticmethod
    def find(x_val, y_val):
        x = Vertex.getCloserX(x_val)[0]
        y = Vertex.getCloserY(y_val)[0]

        count = 0
        head = Vertex.map_X[x]
        while head:
            if head._y == y:
                break
            else:
                head = head._next
                count += 1
            pass
        return Vertex.ordered_coors_x.index(x), count
        
        
    @staticmethod
    def getCloserX(val):
        dist = 100  # miglior distanza ottenuta:
        closer = -100  # da quale vertice
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
from pprint import pprint
primitive = geom.getPrimitive(0)
vdata = geom.getVertexData()

print("expected rows/lines: ", int(sqrt(vdata.getNumRows())))
reader = GeomVertexReader(vdata, "vertex")

reader.setRow(0)
while not reader.isAtEnd():
    Vertex(reader.getData3())
    pass

for x in Vertex.ordered_coors_x:
    log(x)

print("x: ", len(Vertex.coords_x))
print("y: ", len(Vertex.coords_y))
print("z: ", len(Vertex.coords_z))

print("#################")

if False:
    for x in Vertex.map_X:
        pprint(Vertex.map_X[x].as_list())

    for x in Vertex.map_X:
        print(len(Vertex.map_X[x].as_list()))
    pass

pprint(Vertex.ordered_coors_x)
# print(primitive)
tri_coords = None

def vertex_min(v1, v2):
    if v1[1] < v2[1]:
        return v1
    elif v1[1] == v2[1]:
        if v1[0] < v2[0]:
            return v1
    return v2


def index_vertex_min3(v1, v2, v3):
    return (v1, v2, v3).index(vertex_min(vertex_min(v1, v2), v3))

for g in range(geom.getNumPrimitives()):
    prim = geom.getPrimitive(g)
    prim = prim.decompose()
    print("AAAAAA")
    for p in range(prim.getNumPrimitives()):
        s = prim.getPrimitiveStart(p)
        e = prim.getPrimitiveEnd(p)
        # print(s, e)
        # print(prim)
        tri_coords = []
        for i in range(s, e):
            vi = prim.getVertex(i)
            reader.setRow(vi)
            v = reader.getData3()
            tri_coords.append(Vertex.find(v.getX(), v.getY()))
        log(tri_coords)
        log("min:", index_vertex_min3(*tri_coords))
        










if ENABLELOG:
    fp.close()
