# mediasert game by GCocco

from direct.showbase.ShowBase import ShowBase
from panda3d.core import DirectionalLight

import config
import gui

from player import FPController
from maps import Map_01

class Mediasert(ShowBase):

    def __init__(self):
        super().__init__()
        config.init_config(self)
        self.disableMouse()
        self.accept("escape", exit)
    pass



if __name__ == "__main__":
    ms = Mediasert()
    me = FPController(ms)
    light = ms.camera.attachNewNode(DirectionalLight("light"))
    ms.render.setLight(light)
    
    map = Map_01(ms)
    ms.run()
