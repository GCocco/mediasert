from direct.showbase.DirectObject import DirectObject
from panda3d.core import NodePath

from settings import ControllerSettings
from utils import Direction

SIN45 = 0.7071

class FPController(DirectObject, NodePath):
    _angleMap = {
        Direction.Forward: (0, ControllerSettings.Speed, 0),
        Direction.Back: (0, -ControllerSettings.Speed, 0),
        Direction.Left: (-ControllerSettings.Speed, 0, 0),
        Direction.Right: (ControllerSettings.Speed, 0, 0),
        Direction.ForwardRight: (SIN45, SIN45, 0),
        Direction.ForwardLeft: (-SIN45, SIN45, 0),
        Direction.BackRight: (SIN45, -SIN45, 0),
        Direction.BackLeft: (-SIN45, SIN45, 0)}
    
    def __init__(self, base):

        NodePath.__init__(self, "player")
        self.reparentTo(base.render)
        self.camera = base.camera
        self.camera.reparentTo(self)
        # movement ontroller                                                                                                                                 
        self._inputs = {ControllerSettings.Forward: False,
                        ControllerSettings.Back: False,
                        ControllerSettings.Left: False,
                        ControllerSettings.Right: False}

        self.accept(ControllerSettings.Forward, self._changeValue,
                    extraArgs=[ControllerSettings.Forward, True])
        self.accept(ControllerSettings.Back, self._changeValue,
                    extraArgs=[ControllerSettings.Back, True])
        self.accept(ControllerSettings.Left, self._changeValue,
                    extraArgs=[ControllerSettings.Left, True])
        self.accept(ControllerSettings.Right, self._changeValue,
                    extraArgs=[ControllerSettings.Right, True])
        
        self.accept((ControllerSettings.Forward + "-up"), self._changeValue,
                    extraArgs= [ControllerSettings.Forward, False])
        self.accept((ControllerSettings.Back + "-up"), self._changeValue,
                    extraArgs=[ControllerSettings.Back, False])
        self.accept((ControllerSettings.Left + "-up"), self._changeValue,
                    extraArgs=[ControllerSettings.Left, False])
        self.accept((ControllerSettings.Right + "-up"), self._changeValue,
                    extraArgs=[ControllerSettings.Right, False])

        self.doMethodLater(.01, self._controllerTask, "mnove-it")

    def _changeValue(self, key, val):
        self._inputs[key] = val

    def _getDirection(self):
        dire = 0
        if self._inputs[ControllerSettings.Forward]:
            dire += 1
        if self._inputs[ControllerSettings.Back]:
            dire -= 1
        if self._inputs[ControllerSettings.Left]:
            dire -= 4
        if self._inputs[ControllerSettings.Right]:
            dire += 4
        try:
            return Direction(dire)
        except ValueError:
            return Direction.Undefined

    def _controllerTask(self, task):
        dire = self._getDirection()
        if dire is not  Direction.Undefined:
            self.setPos(self, self._angleMap[dire])
        return task.again

    


