# maps

from panda3d.core import NodePath, BitMask32
from direct.showbase.DirectObject import DirectObject
from models.prefabs import PREFAB_MAP
from utils import BitMasks
from panda3d.core import AmbientLight
from config import get_globals, set_map

_Globals = get_globals()

class EmptyMap(DirectObject, NodePath):
    
    def __init__(self, model_path, navmesh_path, name="map"):
        NodePath.__init__(self, name)
        self.attachNewNode(_Globals.loader.loadModel(model_path).node())
        self.reparentTo(_Globals.render)
        self._nav_mesh = navmesh_path
        pass
    
    def setMask(self):
        self.find("**/+CollisionNode").node().setIntoCollideMask(BitMasks.Solid)
        self.find("**/+CollisionNode").node().setFromCollideMask(BitMasks.Empty)
        return
    def parse(self):
        for placeholder in self.findAllMatches("**/=prefab"):
            new_node = PREFAB_MAP[placeholder.getTag("prefab")](placeholder=placeholder)
            new_node.reparentTo(self)
            placeholder.removeNode()
            print("found prefab", placeholder.getTag("prefab"))
            pass
        return

    @property
    def navMesh(self):
        return self._nav_mesh
    
    pass


class Map_01(EmptyMap):
    def __init__(self):
        super().__init__("./models/maps/level_01_intro.egg",
                         "./models/maps/level_01.csv", name="lvl_01")
        
        self.ambient = self.attachNewNode(AmbientLight("ambient"))
        self.ambient.node().setColor((.6, .6, .6, 1))
        _Globals.render.setLight(self.ambient)
        
        self.setMask()
        self.parse()
        set_map(self)
        pass
    pass
