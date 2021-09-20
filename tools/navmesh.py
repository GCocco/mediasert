import ctypes
navmeshlib = ctypes.cdll.LoadLibrary("./navmesh.so")


class NavMesh:
    def __init__(self, filename):
        self._pointer = navmeshlib.newNavmesh(ctypes.c_char_p(filename.encode("utf-8")))
        pass

    def _find(self, x, y):
        return Coordinate.from_address(navmeshlib.find(self._pointer, ctypes.c_double(x), ctypes.c_double(y)))

    def find_path(self, start_x, start_y, end_x, end_y):
        return navmeshlib.find_path(self._pointer,
                                    ctypes.c_double(start_x), ctypes.c_double(start_y),
                                    ctypes.c_double(end_x), ctypes.c_double(end_y))    
    def __del__(self):
        navmeshlib._del_navmesh(self._pointer)
        return
    pass


class Coordinate(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int),
                ("y", ctypes.c_int)]

    def __repr__(self):
        return f"Coordinate ({self.x},{self.y})"
    pass


class path_node(ctypes.Structure):
    pass
path_node._fields_ = [("coord", Coordinate),
                      ("next", ctypes.POINTER(path_node))]


if __name__ == "__main__":
    nm = NavMesh("./mynavmesh.csv")
    
    path = nm.find_path(.4, .3, .6, .2)

    print(path)

    pl = path_node.from_address(path)
    pp = ctypes.pointer(pl)
    print(pp.contents.coord)

    pp = pp.contents.next
    
    print(pp.contents.coord)
