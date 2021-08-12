# mediasert game by GCocco

from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from panda3d.core import NodePath

from player import FPController

class Mediasert(ShowBase):

    def __init__(self):
        super().__init__()
        # debug stuff:
        smile = self.loader.loadModel("./models/cube.egg")
        smile.reparentTo(self.render)
    pass



if __name__ == "__main__":
    ms = Mediasert()
    me = FPController(ms)
    ms.run()
