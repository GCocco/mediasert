# prefabs assets

from panda3d.core import NodePath
from config import Loader
from utils import BitMasks

class Prefab(NodePath):
    def __init__(self, model_path):
        super().__init__(Loader.loadModel(model_path))
        pass

    def copyTransform(self, other_node):
        self.setPosHprScale(other_node.getPos(), other_node.getHpr(), other_node.getScale())
        return


class Door_01(Prefab):
    def __init__(self, placeholder=None):
        super().__init__("./models/maps/maps_props/door_01.egg")
        if placeholder:
            self.copyTransform(placeholder)
            self.find("**/+CollisionNode").setTag("interactable_id", placeholder.getTag("interactable_id"))
        self.find("**/+CollisionNode").node().setIntoCollideMask(BitMasks.Interactable)
        self.find("**/+CollisionNode").node().setFromCollideMask(BitMasks.Empty)
        
        
PREFAB_MAP = {"Door_01": Door_01}
