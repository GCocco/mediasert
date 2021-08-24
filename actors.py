# actors and actors utilities

from direct.actor.Actor import Actor

class MaleNPC(Actor):
    def __init__(self):
        Actor.__init__(self, "./models/actors/male.egg",
                       {"Walk": "./models/actors/male-Walk.egg",
                        "Idle": "./models/actors/male-Idle.egg",
                        "Pain": "./models/actors/male-Pain.egg"})
        pass
    pass
