import ctypes
from panda3d.core import LVector3


class Coordinate(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int),
                ("y", ctypes.c_int)]
    
    def __repr__(self):
        return f"Coordinate ({self.x},{self.y})"
    
    pass


class PathNode(ctypes.Structure):

    def __repr__(self):
        return f"PathNode {self.coord}"
    
    pass

PathNode._fields_ = [("coord", Coordinate),
                     ("next", ctypes.POINTER(PathNode))]    


class NavMesh:
    c_lib = ctypes.CDLL("./navmesh.so")
    
    def __init__(self, filename):
        self._pointer = self.c_lib.newNavmesh(ctypes.c_char_p(filename.encode("utf-8")))
        pass

    def _find(self, x, y):
        return Coordinate.from_address(self.c_lib.find(self._pointer, ctypes.c_double(x), ctypes.c_double(y)))

    def find_path(self, start_x, start_y, end_x, end_y):
        return self.c_lib.find_path(self._pointer,
                                    ctypes.c_double(start_x), ctypes.c_double(start_y),
                                    ctypes.c_double(end_x), ctypes.c_double(end_y))    
    def __del__(self):
        self.c_lib.del_navmesh(self._pointer)
        return
    
    def navigate(self, pos_start, pos_end):
        ppointer = PathPointer(self.find_path(pos_start.getX(),
                                              pos_start.getY(),
                                              pos_end.getX(),
                                              pos_end.getY()))
        
        return ppointer
    pass




class PathPointer:
    c_lib = NavMesh.c_lib
    def __init__(self, path_list):
        self._head = ctypes.pointer(PathNode.from_address(path_list))
        self._raw_pointer = path_list
        pass

    def pop(self):
        head = self._head
        self._head = self._head.contents.next
        return head
    
    @property
    def head(self):
        return self._head.contents
    
    def __del__(self):
        self.c_lib.free_path(self._raw_pointer)
        return

    @property
    def list(self):
        head = self._head
        path_list = []
        while bool(head):
            path_list.append(head.contents.coord)
            head = head.contents.next
            pass
        return path_list
            
        
    pass





if __name__ == "__main__":
    nm = NavMesh("./mynavmesh.csv")
    print(nm)
    culo = nm.navigate(LVector3(.8, .06, .0), LVector3(.1, .1, .0))
    print("ayylmao")
    print(culo.list)
