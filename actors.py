# actors and actors utilities

from direct.actor.Actor import Actor
from random import seed, random, choice
from panda3d.core import LColor, Material

from panda3d.core import CollisionNode, CollisionBox
from utils import BitMasks, EventMap
from config import get_globals
import events
from direct.fsm.FSM import FSM

seed()
_Globals = get_globals()

def alter(base, delta): # slightly changes a [0-1] float by adding or subtracting a [0-delta] value
    return base + ((delta * 2 * random()) - delta) 

ambient_default = LColor(.0, .0, .0, 1.0)


class NpcFSM(FSM):
    def __init__(self, npc):
        FSM.__init__(self, str(npc.getID))
        self._npc = npc
        pass

    def enterIdle(self):
        self._npc.loop("Idle")

    def enterWalk(self):
        self._npc.loop("Walk")

    def enterPain(self):
        self._npc.loop("Pain")
    pass


class NPC(Actor):
    _id_seed = 0

    @property
    def getID(self):
        return self._id
    
    
    def __init__(self, model, animations):
        super().__init__(model, animations)
        self._id = "NPC_" + str(NPC._id_seed)
        self._id_seed += 1
        self._fsm = NpcFSM(self)
        pass

    def _interact(self):
        print(_Globals.player.holded)
        pass
    pass

class MaleNPC(NPC):
    def __init__(self):
        super().__init__("./models/actors/male.egg",
                         {"Walk": "./models/actors/male-Walk.egg",
                          "Idle": "./models/actors/male-Idle.egg",
                          "Pain": "./models/actors/male-Pain.egg"})

        

        shirt_material = Material()
        shirt_material.setDiffuse(LColor(random(), random(), random(), 1.0))
        shirt_material.setAmbient(ambient_default)
        skin_material = Material()
        skin_material.setDiffuse(LColor(1.0, alter(.75, .12), alter(.8, .1), 1.0))
        skin_material.setAmbient(ambient_default)
        
        pants_material = Material()
        pants_material.setDiffuse(LColor(random(), random(), random(), 1.0))
        pants_material.setAmbient(ambient_default)
        
        self.replaceMaterial(self.findMaterial("Shirt"), shirt_material)
        self.replaceMaterial(self.findMaterial("Skin"), skin_material)
        self.replaceMaterial(self.findMaterial("Face"), skin_material)
        self.replaceMaterial(self.findMaterial("Convertible"), choice([skin_material, shirt_material]))
        self.replaceMaterial(self.findMaterial("Pants"), pants_material)
        self.findMaterial("Hairs").setAmbient(ambient_default)
        self.findMaterial("Mouth").setAmbient(ambient_default) # TODO: posso modificare dal .egg
        self.findMaterial("Shoes").setAmbient(ambient_default) # idem come sopra

        
        self._coll_np = self.attachNewNode(CollisionNode("npc_collider"))

        self._coll_np.node().addSolid(CollisionBox((.0, .0, .9), .2, .2, .9))
        self._coll_np.node().setIntoCollideMask(BitMasks.Solid | BitMasks.Interactable)
        self._coll_np.node().setFromCollideMask(BitMasks.Empty)
        self._coll_np.setTag("interactable_id", self._id)
        self._coll_np.show()
        print("actor-1")
        EventMap.bind(self._id, events.CollisionEvent(events.NoticeEvent("gigi"), on_click=events.Event(self._interact)))


        # ai setup
        # self._ai_behav = _Globals.world.add_npc(self).getAiBehaviors()
        print("actor-2")
        # self._ai_behav.seek(_Globals.player)
        print("actor-3")
        pass
    
    
    pass
