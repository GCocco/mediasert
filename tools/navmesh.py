import ctypes
navmeshlib = ctypes.cdll.LoadLibrary("./navmesh.so")

class Y_Obstacle(ctypes.Structure):
    pass
Y_Obstacle._fields_ = [("coll_start", ctypes.c_int),
                       ("next", ctypes.POINTER(Y_Obstacle)),
                       ("coll_end", ctypes.c_int)]

class ABC_Y(ctypes.Structure):
    _fields_ = [("start", ctypes.c_int),
                ("obstacles", ctypes.POINTER(Y_Obstacle)),
                ("end", ctypes.c_int)]
    pass

class _Nav_Mesh(ctypes.Structure):
    _fields_ = [("x_lines", ctypes.c_int),
                ("y_lines", ctypes.c_int),
                ("x_coords", ctypes.POINTER(ctypes.c_longdouble)),
                ("y_coords", ctypes.POINTER(ctypes.c_longdouble)),
                ("boundings", ctypes.POINTER(ABC_Y))]

    pass
    

print("\n")

a = navmeshlib.load_from_file(ctypes.c_char_p("./mynavmesh.csv".encode("utf-8")));
print(a)
print("AAAAAAAAA")
navmeshlib.ayy_lmao(ctypes.c_int(0))
# print(a)
