# prefabs assets

from direct.showbase.DirectObject import DirectObject
from panda3d.core import NodePath
from config import get_globals
from utils import BitMasks
import events
from direct.directutil.Mopath import Mopath
from direct.interval.MopathInterval import MopathInterval

_Globals = get_globals()

class Prefab(NodePath):
    def __init__(self, model_path, placeholder=None):
        super().__init__(_Globals.loader.loadModel(model_path))
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
    _IDs = []
    _lowest_id = 1
    _timer = 20

    anim = Mopath()
    _anim_path = "./models/atkpath.egg"
    _anim_is_loaded = False

    @staticmethod
    def _load_mopath():
        Holdable.anim.loadFile(Holdable._anim_path)
        Holdable._anim_is_loaded = True
        return
    
    def __init__(self, model_path, placeholder=None, unholded_event=None):
        super().__init__(model_path, placeholder=placeholder)
        self._instance_id = 0
        if not self._anim_is_loaded:
            self._load_mopath()
            pass
        self._generate_id()
        self.find("**/+CollisionNode").setTag("interactable_id", str(self._instance_id))
        self._set_event()
        pass


    def _set_event(self, text="prendi", onClick=None):
        if onClick:
            events.EventMap.update(str(self._instance_id), events.NoticeText(text, onClick=onClick))
            return
        else:
            events.EventMap.update(str(self._instance_id), events.NoticeText(text, onClick=events.ActionEvent(self.hold)))
            return
    
    def __del__(self):
        self._free_id()
        events.EventMap.remove(str(self._instance_id))
        return

    def _generate_id(self):
        while Holdable._lowest_id in  Holdable._IDs:
            Holdable._lowest_id += 1
        self._instance_id = Holdable._lowest_id
        Holdable._lowest_id += 1
        return

    def _free_id(self):
        try:
            Holdable._IDs.remove(self._instance_id)
        except ValueError:
            pass
        if self._instance_id < Holdable._lowest_id:
            Holdable._lowest_id = self._instance_id
        return

    def _rotateTask(self, task):
        self.setP(_Globals.base.render, .0)
        self.setH(self, .1)
        self.setR(_Globals.base.render, .0)
        return task.again

    def hold(self):
        _Globals.player.setHolded(self)
        self.reparentTo(_Globals.player.holder)
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
        self.reparentTo(_Globals.render)
        self.setPos(_Globals.player.getPos())
        self.setP(0)
        self.setR(0)
        try:
            self.find("**/=mask=interactable").node().setIntoCollideMask(BitMasks.Interactable)
            pass
        except AssertionError:
            pass
        self.removeTask("rotate")
        self.doMethodLater(self._timer, lambda x: self.removeNode(), "destroy")
        return
    
    def onClick(self):
        interval = MopathInterval(self.anim, _Globals.player.holder, .02, name="atkaction")
        interval.start()
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
        pass
    pass


class Lamp_01(Prefab):
    def __init__(self, placeholder=None):
        super().__init__("./models/maps/maps_props/lamp_01.egg", placeholder=placeholder)
        


PREFAB_MAP = {"Door_01": Door_01,
              "CoffeMachine": CoffeMachine,
              "Lamp_01": Lamp_01}
