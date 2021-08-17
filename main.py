# mediasert game by GCocco

from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from panda3d.core import NodePath

from config import Loader

from player import FPController
from maps import EmptyMap, Map_01


class Mediasert(ShowBase):

    def __init__(self):
        super().__init__()
        Loader.init(self.loader)
        self.disableMouse()
        # debug stuff:
        smile = self.loader.loadModel("./models/cube.egg")
        smile.reparentTo(self.render)
        from models.prefabs import PREFAB_MAP
        door = PREFAB_MAP["Door_01"]()
        door.reparentTo(self.render)
        self.accept("escape", exit)
    pass



if __name__ == "__main__":
    ms = Mediasert()
    me = FPController(ms)
    map = Map_01(ms)
    ms.run()
