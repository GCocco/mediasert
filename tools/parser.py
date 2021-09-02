from panda3d import egg
from panda3d.core import Filename, GeomVertexReader, Vec3
from math import sqrt
from pprint import pprint

ENABLELOG = True

fp = None
if ENABLELOG:
    fp = open("./.log.txt", "w")

def log(arg):
    if ENABLELOG:
        fp.write(str(arg)  + "\n")


class Vertex:
    TOLERANCE_X = .00000125
    TOLERANCE_Y = .00000125
    TOLERANCE_Z = .000001
    
    coords_x = set()
    coords_y = set()
    coords_z = set()
    
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

    @property
    def next(self):
        return self._next

    def __repr__(self):
        return f"Vector({self._x},{self._y},{self._z})"

    def __lt__(self, other):
        if self._x <= other._x:
            return self._y < other._y
        return False


    @staticmethod
    def reset():
        Vertex.map_X = dict()
        Vertex.coords_x = set()
        Vertex.coords_y = set()
        Vertex.coords_Z = set()
        return
    
    @staticmethod
    def getCloserX(val):
        dist = 100
        closer = -100
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


from pprint import pprint



def top_left(v1, v2):
    if v1[1] < v2[1]:
        return v1
    elif v1[1] == v2[1]:
        if v1[0] < v2[0]:
            return v1
    return v2

def index_top_left3(v1, v2, v3):
    return (v1, v2, v3).index(top_left(top_left(v1, v2), v3))


def top_right(v1, v2):
    if v1[0] >= v2[0] and v1[1] < v2[1]:
        return v1
    return v2

def index_top_right3(v1, v2, v3):
    return (v1, v2, v3).index(top_right(top_right(v1, v2), v3))


class NavMesh:
    def __init__(self, mod_path, coll_path):
        self.grid_geom = egg.loadEggFile(mod_path).getChild(0).getGeom(0)
        vdata = self.grid_geom.getVertexData()
        
        reader = GeomVertexReader(vdata, "vertex")
        reader.setRow(0)
        
        while not reader.isAtEnd():
            Vertex(reader.getData3())
            pass

        print("Parsed ", vdata.getNumRows(), "vertices")
        print("found ", len(Vertex.coords_x), " x levels")
        print("found ", len(Vertex.coords_y), " y levels")
        print("found ", len(Vertex.coords_z), " z levels")
        
        self._grid_x_coords = sorted(Vertex.coords_x)
        self._grid_y_coords = sorted(Vertex.coords_y)
        self._map_X = Vertex.map_X


        self._grid_vertices = []
        
        for g in range(self.grid_geom.getNumPrimitives()):  # TODO: questi cicli possono essere sostituiti da uno sugli elementi in self._map_X
            prim = self.grid_geom.getPrimitive(g).decompose() # (credo)

            for p in range(prim.getNumPrimitives()):
                s = prim.getPrimitiveStart(p)
                e = prim.getPrimitiveEnd(p)
                tri_coords = []
                for i in range(s, e):
                    reader.setRow(prim.getVertex(i))
                    tri_coords.append(self.find(reader.getData3()))
                tl = index_top_left3(*tri_coords)
                if tl != index_top_right3(*tri_coords):
                    self._grid_vertices.append(tri_coords[tl])
                    pass
                pass
            pass
        for gv in self._grid_vertices:
            log(gv)

        coll_geom = egg.loadEggFile(coll_path).getChild(0).getGeom(0)
        vdata = coll_geom.getVertexData()
        reader = GeomVertexReader(vdata, "vertex")
        reader.setRow(0)
        for g in range(coll_geom.getNumPrimitives()):
            prim = coll_geom.getPrimitive(g).decompose()

            for p in range(prim.getNumPrimitives()):
                s = prim.getPrimitiveStart(p)
                e = prim.getPrimitiveEnd(p)
                tri_coords = []
                for i in range(s, e):
                    reader.setRow(prim.getVertex(i))
                    tri_coords.append(self.find(reader.getData3()))
                tl = index_top_left3(*tri_coords)
                if tl != index_top_right3(*tri_coords):
                    self._grid_vertices.remove(tri_coords[tl])
                    pass
                pass
            pass
        log("AYYLMAO")
        for gv in self._grid_vertices:
            log(gv)        

        
        pass


    def getCloser(self, x_val, y_val):
        closer_x = self._grid_x_coords[0]
        closer_y = self._grid_y_coords[0]
        diff = 1000
        for x in self._grid_x_coords:
            if abs(x-x_val) < diff:
                closer_x = x
                diff = abs(x-x_val)
                pass
            pass
        diff = 1000
        for y in self._grid_y_coords:
            if abs(y-y_val) < diff:
                closer_y = y
                diff = abs(y-y_val)
                pass
            pass
        return closer_x, closer_y
        

    def find(self, vert):
        x, y = self.getCloser(vert.getX(), vert.getY())
        
        count = 0
        head = self._map_X[x]
        while head:
            if head._y == y:
                break
            else:
                head = head.next
                count += 1
            pass
        return self._grid_x_coords.index(x), count


    








if __name__ == "__main__":
    nv = NavMesh("./mesh_full.egg", "./mesh_full.egg")

