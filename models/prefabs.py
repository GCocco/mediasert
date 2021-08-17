# prefabs assets

from panda3d.core import NodePath
from config import Loader

class Prefab(NodePath):
    def __init__(self, model_path):
        super().__init__(Loader.loadModel(model_path))
        pass


class Door_01(Prefab):
    def __init__(self):
        super().__init__("./models/maps/maps_props/door_01.egg")
    

PREFAB_MAP = {"Door_01": Door_01}
