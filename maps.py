# maps

from panda3d.core import NodePath, BitMask32
from direct.showbase.DirectObject import DirectObject
from models.prefabs import PREFAB_MAP

class EmptyMap(DirectObject, NodePath):
    _bitmask = BitMask32(7)
    
    def __init__(self, base, name="map"):
        NodePath.__init__(self, name)
        self.reparentTo(base.render)

    def setMask(self):
        self.find("**/+CollisionNode").node().setIntoCollideMask(self._bitmask)
    
    def parse(self):
        for placeholder in self.findAllMatches("**/=prefab"):
            new_node = PREFAB_MAP[placeholder.getTag("prefab")](placeholder=placeholder)
            new_node.reparentTo(self)
            placeholder.removeNode()
            print("found prefab", placeholder.getTag("prefab"))
    pass


class Map_01(EmptyMap):
    def __init__(self, base):
        super().__init__(base, "lvl_01")
        lvl_map = base.loader.loadModel("./models/maps/level_01_intro.egg")
        lvl_map.reparentTo(self)
        self.setMask()
        self.parse()
