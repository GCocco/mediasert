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
        config.init_config(self)
        self.disableMouse()
        
        self.accept("escape", exit)

        def showcolliders():
            for collider in self.render.findAllMatches("**/+CollisionNode"):
                collider.getParent().show()

        self.accept("c", showcolliders)
        pass



if __name__ == "__main__":
    ms = Mediasert()
    me = FPController(ms)
    light = ms.camera.attachNewNode(DirectionalLight("light"))
    from actors import MaleNPC

    npc = MaleNPC()
    npc.setY(-4)
    npc.reparentTo(ms.render)
    npc.loop("Idle")
    
    ms.render.setLight(light)
    
    map = Map_01(ms)
    ms.run()
