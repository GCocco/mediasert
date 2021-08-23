# prefabs assets

from direct.showbase.DirectObject import DirectObject
from panda3d.core import NodePath
from config import get_globals
from utils import BitMasks
import events

Globals = get_globals()

class Prefab(NodePath):
    def __init__(self, model_path, placeholder=None):
        super().__init__(Globals.loader.loadModel(model_path))
        if placeholder:
            self.copyTransform(placeholder)
            pass
        pass

    def copyTransform(self, other_node):
        self.setPosHprScale(other_node.getPos(), other_node.getHpr(), other_node.getScale())
        return
    
    def set_masks(self):
        
        for interactable in self.findAllMatches("**/=mask=interactable"):
            interactable.node().setIntoCollideMask(BitMasks.Interactable)
        for solid in self.findAllMatches("**/=mask=solid"):
            solid.node().setIntoCollideMask(BitMasks.Solid)
        for collider in self.findAllMatches("**/+CollisionNode"):
            collider.node().setFromCollideMask(BitMasks.Empty)
        return
    pass


class Holdable(Prefab, DirectObject):
    _timer = 20
    def __init__(self, model_path, placeholder=None):
        super().__init__(model_path, placeholder=placeholder)
        pass

    def _rotateTask(self, task):
        self.setP(Globals.base.render, .0)
        self.setH(self, .1)
        self.setR(Globals.base.render, .0)
        return task.again

    def hold(self):
        Globals.player.setHolded(self)
        self.reparentTo(Globals.player.holder)
        self.setScale(.3)
        self.setPos(.4, 1.9, -.3)
        try:
            self.find("**/=mask=interactable").node().setIntoCollideMask(BitMasks.Empty)
            pass
        except AssertionError:
            pass
        self.doMethodLater(.01, self._rotateTask, "rotate")
        self.removeTask("destroy")
        return

    def drop(self):
        self.reparentTo(Globals.render)
        self.setPos(Globals.player.getPos())
        self.setP(0)
        self.setR(0)
        self.setScale(1)
        try:
            self.find("**/=mask=interactable").node().setIntoCollideMask(BitMasks.Interactable)
            pass
        except AssertionError:
            pass
        self.removeTask("rotate")
        self.doMethodLater(self._timer, lambda x: self.removeNode(), "destroy")
        return
    
    def onClick(self, collided): # to be overridden, changes based on prefab
        pass

    def throw(self): # launches the model (straight line? mopath?)
        pass # todo: implement
    pass


class Door_01(Prefab):
    def __init__(self, placeholder=None):
        super().__init__("./models/maps/maps_props/door_01.egg", placeholder=placeholder)
        if placeholder:
            self.find("**/+CollisionNode").setTag("interactable_id", placeholder.getTag("interactable_id"))
        self.set_masks()
        return
    pass


class CoffeMachine(Prefab):
    def __init__(self, placeholder=None):
        super().__init__("./models/maps/maps_props/coffe_machine.egg")
        if placeholder:
            self.copyTransform(placeholder)
        self.set_masks()
        events.EventMap.update(self.find("**/=interactable_id").getTag("interactable_id"),
                               events.NoticeText("Compra KAFFEEEEEEEE", onClick=events.ActionEvent(self.dispense_coffe)))

    def dispense_coffe(self):
        coffe = Coffe(self.find("**/cup_placeholder"))
        coffe.reparentTo(self)
        return
    pass


class Coffe(Holdable):
    def __init__(self, placeholder=None):
        super().__init__("./models/props/coffe_cup.egg", placeholder=placeholder)
        self.set_masks()
        events.EventMap.update(self.find("**/=interactable_id").getTag("interactable_id"),
                               events.NoticeText("prendi", onClick=events.ActionEvent(self.hold)))
        pass
    pass


class Lamp_01(Prefab):
    def __init__(self, placeholder=None):
        super().__init__("./models/maps/maps_props/lamp_01.egg", placeholder=placeholder)
        


PREFAB_MAP = {"Door_01": Door_01,
              "CoffeMachine": CoffeMachine,
              "Lamp_01": Lamp_01}
