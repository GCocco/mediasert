import ctypes
from panda3d.core import LVector3


class Coordinate(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int),
                ("y", ctypes.c_int)]
    
    def __repr__(self):
        return f"Coordinate ({self.x},{self.y})"
    
    pass


class FCoordinate(ctypes.Structure):
    _fields_ = [("x",ctypes.c_double ),
                ("y",ctypes.c_double)]
    @property
    def vector(self):
        return LVector3(self.x, self.y, 0.0)
    pass

class _PathNode(ctypes.Structure):
    def __repr__(self):
        return f"PathNode {self.coord}"


_PathNode._fields_ = [("coord", Coordinate),
                     ("next", ctypes.POINTER(_PathNode))]



class NavMesh:
    c_lib = ctypes.CDLL("./navmesh.so")
    c_lib.get_world_coordinates.restype = FCoordinate
    c_lib.find.restype = Coordinate
    c_lib.find_path.restype = ctypes.POINTER(_PathNode)
    
    def __init__(self, filename):
        self._pointer = self.c_lib.newNavmesh(ctypes.c_char_p(filename.encode("utf-8")))
        pass

    def _find(self, x, y):
        return self.c_lib.find(self._pointer, ctypes.c_double(x), ctypes.c_double(y))

    def find_path(self, start_x, start_y, end_x, end_y):
        ppointer = NavMesh.c_lib.find_path(self._pointer,
                                           ctypes.c_double(start_x), ctypes.c_double(start_y),
                                           ctypes.c_double(end_x), ctypes.c_double(end_y))
        head = ppointer
        path_list = []
        while bool(head):
            path_list.append(head.contents.coord)
            head = head.contents.next
            pass

        NavMesh.c_lib.free_path(ppointer)
        return path_list

    
    def __del__(self):
        self.c_lib.del_navmesh(self._pointer)
        return


    def coordinate_to_world(self, coord):
        return NavMesh.c_lib.get_world_coordinates(self._pointer, coord).vector
    
    def navigate(self, pos_start, pos_end):
        return self.find_path(pos_start.getX(), pos_start.getY(),
                              pos_end.getX(), pos_end.getY())
    pass







if __name__ == "__main__":
    nm = NavMesh("./mynavmesh.csv")
    print(nm)
    culo = nm.navigate(LVector3(.8, .6, .0), LVector3(.1, .1, .0))
    print("ayylmao")
    for v in culo:
        print(v, v.vector)  # TODO: convert coordinates in world space
        pass
    pass

    
