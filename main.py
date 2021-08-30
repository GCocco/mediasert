# mediasert game by GCocco

from direct.showbase.ShowBase import ShowBase
from panda3d.core import DirectionalLight
import utils # sets masks 
import config
import gui

from player import FPController
from maps import Map_01


class Mediasert(ShowBase):

    def __init__(self):
        super().__init__()
        self.render.setScale(70)
        config.init_config(self)
        self.disableMouse()
        
        self.accept("escape", exit)
        pass
    
    pass



if __name__ == "__main__":
    ms = Mediasert()
    me = FPController(ms)
    light = ms.camera.attachNewNode(DirectionalLight("light"))
    from actors import MaleNPC

    mp = Map_01()
    npc = MaleNPC()
    npc.setY(-4)
    npc.reparentTo(ms.render)
    npc.loop("Idle")
    
    ms.render.setLight(light)
    
    ms.run()
