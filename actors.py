# actors and actors utilities

from direct.actor.Actor import Actor
from random import seed, random, choice
from panda3d.core import LColor, Material

from panda3d.core import CollisionCapsule, CollisionNode, CollisionBox
from utils import BitMasks

seed()

def alter(base, delta): # slightly changes a [0-1] float by adding or subtracting a [0-delta] value
    return base + ((delta * 2 * random()) - delta) 

ambient_default = LColor(.0, .0, .0, 1.0)

class MaleNPC(Actor):
    def __init__(self):
        Actor.__init__(self, "./models/actors/male.egg",
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


        coll_node = CollisionNode("npc_collider")
        self._coll_np = self.attachNewNode(coll_node)

        coll_node.addSolid(CollisionBox((.3, .3, .0), (-.3, -.3, 1.8)))
        coll_node.setIntoCollideMask(BitMasks.Solid)
        coll_node.setFromCollideMask(BitMasks.Empty)
        self._coll_np.show()
        pass
    pass
