import ctypes
navmeshlib = ctypes.cdll.LoadLibrary("./navmesh.so")


class NavMesh:
    def __init__(self, filename):
        self._pointer = navmeshlib.newNavmesh()
        navmeshlib.loadFromFile(self._pointer, ctypes.c_char_p(filename.encode("utf-8")))
        navmeshlib.check(self._pointer)
        pass

    def _find(self, x, y):
        navmeshlib.find(self._pointer, ctypes.c_double(x), ctypes.c_double(y))
        return

    def __del__(self):
        navmeshlib._del_navmesh(self._pointer)
        return

class Coordinate(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int),
                ("y", ctypes.c_int)]
    pass



if __name__ == "__main__":
    nm = NavMesh("./mynavmesh.csv")
    nm._find(-1000000000000, .0)
