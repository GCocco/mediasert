# actors and actors utilities

from direct.actor.Actor import Actor
from random import seed, random
from panda3d.core import LColor


class MaleNPC(Actor):
    def __init__(self):
        Actor.__init__(self, "./models/actors/male.egg",
                       {"Walk": "./models/actors/male-Walk.egg",
                        "Idle": "./models/actors/male-Idle.egg",
                        "Pain": "./models/actors/male-Pain.egg"})
        shirtMaterial = self.findMaterial("Shirt")
        shirtMaterial.setDiffuse(LColor(random(), random(), random(), 1))
        pass
    pass
