# mediasert game by GCocco

from direct.showbase.ShowBase import ShowBase
from panda3d.core import DirectionalLight
import utils # sets masks 
import config
import gui

from player import FPController
from maps import Map_01
from panda3d import ai


class Mediasert(ShowBase):

    def __init__(self):
        super().__init__()

        self.AIWorld = ai.AIWorld(self.render)  # AI
        self.addTask(self._aitask, "aiTask")  # AI
        
        self.render.setScale(70)
        config.init_config(self)
        self.disableMouse()
        
        self.accept("escape", exit)
        pass

    def _aitask(self, task):
        self.AIWorld.update()
        return task.cont
    
    pass



if __name__ == "__main__":
    ms = Mediasert()
    print("A")
    me = FPController(ms)
    print("B")
    light = ms.camera.attachNewNode(DirectionalLight("light"))
    from actors import MaleNPC

    mp = Map_01()

    print("C")
    npc = MaleNPC()
    print("D")
    npc.setY(-4)
    npc.reparentTo(ms.render)
    npc.loop("Idle")


    # AI
    npc_AI = ai.AICharacter("npc", npc, 100, .005, 5)
    ms.AIWorld.addAiChar(npc_AI)

    npc_behav = npc_AI.getAiBehaviors()


    npc_behav.initPathFind("./models/maps/lvl_01.egg")
    
    npc_behav.pursue(me)
    
    ms.render.setLight(light)
    
    ms.run()
