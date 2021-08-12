from direct.showbase.DirectObject import DirectObject
from .settings import ControllerSettings

class PlayerController(DirectObject):
    def __init__(self):
        self._inputs = {ControllerSettings.Forward: False,
                        ControllerSettings.Back: False,
                        ControllerSettings.Left: False,
                        ControllerSettings.Right: False}

    def changeValue(self, key, val):
        self._inputs[key] = val

    def getDirection(self):
        direction = 0
        if self._inputs[ControllerSettings.Forward]:
            direction += 1
        if self._inputs[ControllerSettings.Back]:
            direction += 2
        if self._inputs[ControllerSettings.Left]:
            direction += 4
        if self._inputs[ControllerSettings.Right]:
            direction += 8
        return direction
        


class FPController(DirectObject, NodePath):
    def __init__(self, base):
        NodePath.__init__(self, "player")
        self.reparentTo(base.render)
        self.camera = base.camera
        
        # movement ontroller
        
        self.camera.reparentTo(self)

        self.accept("l", self.ls)
        pass
    pass
