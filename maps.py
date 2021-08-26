# maps

from panda3d.core import NodePath, BitMask32
from direct.showbase.DirectObject import DirectObject
from models.prefabs import PREFAB_MAP
from utils import BitMasks
from panda3d.core import AmbientLight



class EmptyMap(DirectObject, NodePath):
    
    def __init__(self, base, name="map"):
        NodePath.__init__(self, name)
        self.reparentTo(base.render)

    def setMask(self):
        self.find("**/+CollisionNode").node().setIntoCollideMask(BitMasks.Solid)
        self.find("**/+CollisionNode").node().setFromCollideMask(BitMasks.Empty)
    
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
        self.ambient = self.attachNewNode(AmbientLight("ambient"))
        self.ambient.node().setColor((.6, .6, .6, 1))
        base.render.setLight(self.ambient)
        self.setMask()
        self.parse()

