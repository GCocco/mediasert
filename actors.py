# actors and actors utilities

from direct.actor.Actor import Actor
from random import seed, random, choice
from panda3d.core import LColor, Material
seed()

def alter(base, delta): # slightly changes a [0-1] float by adding or subtracting a [0-delta] value
    return base + ((delta * 2 * random()) - delta) 


class MaleNPC(Actor):
    def __init__(self):
        Actor.__init__(self, "./models/actors/male.egg",
                       {"Walk": "./models/actors/male-Walk.egg",
                        "Idle": "./models/actors/male-Idle.egg",
                        "Pain": "./models/actors/male-Pain.egg"})

        shirt_material = Material()
        shirt_material.setDiffuse(LColor(random(), random(), random(), 1.0))
        shirt_material.setAmbient(LColor(.0, .0, .0, 1.0))
        skin_material = Material()
        skin_material.setDiffuse(LColor(1.0, alter(.75, .12), alter(.8, .1), 1.0))
        shirt_material.setAmbient(LColor(.0, .0, .0, 1.0))

        pants_material = Material()
        pants_material.setDiffuse(LColor(random(), random(), random(), 1.0))
        pants_material.setAmbient(LColor(.0, .0, .0, 1.0))
        
        self.replaceMaterial(self.findMaterial("Shirt"), shirt_material)
        self.replaceMaterial(self.findMaterial("Skin"), skin_material)
        self.replaceMaterial(self.findMaterial("Convertible"), choice([skin_material, shirt_material]))
        self.replaceMaterial(self.findMaterial("Pants"), pants_material)
        pass
    pass
