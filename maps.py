# maps

from panda3d.core import NodePath, BitMask32
from direct.showbase.DirectObject import DirectObject

class EmptyMap(DirectObject, NodePath):
    def __init__(self, base, name="map"):
        NodePath.__init__(self, name)
        self.reparentTo(base.render)
        pass
    pass


class Map_01(EmptyMap):
    def __init__(self, base):
        super().__init__(base, "lvl_01")
        lvl_map = base.loader.loadModel("./models/maps/level_01_intro.egg")
        lvl_map.reparentTo(self)
        self.find("**/+CollisionNode").node().setIntoCollideMask(BitMask32(7))
