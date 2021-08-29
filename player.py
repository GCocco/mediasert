from direct.showbase.DirectObject import DirectObject
from panda3d.core import NodePath

from settings import ControllerSettings
from utils import Direction, BitMasks
from panda3d.core import CollisionTraverser, CollisionNode
from panda3d.core import CollisionSegment, CollisionHandlerQueue, CollisionRay, CollisionBox
from panda3d.core import Thread
from utils import EventMap
from config import get_globals, init_player

_Globals = get_globals()

SIN45 = 0.7071


class _InteractHandler(DirectObject):
    def __init__(self, raynode):
        self._interrupt = False
        self._last_collided = None
        self._queue = CollisionHandlerQueue()
        _Globals.base.cTrav.addCollider(raynode, self._queue)
        pass

    @property
    def collidingNP(self):
        return self._last_collided

    def interactTask(self, task):
        if self._queue.getNumEntries():
            self._queue.sortEntries()
            self(self._queue.getEntry(0).getIntoNode().getTag("interactable_id"))
            return task.again
        else:
            self(None)
            return task.again
        return task.again

    def onHover(self):
        try:
            print("hovering", self._last_collided)
            EventMap.hover(self._last_collided)
        except KeyError:
            print("No event for id", self._last_collided)
            return
        return

    def onClick(self):
        if self._last_collided is not None:
            EventMap.click(self._last_collided)
            return True
        return False
    
    def onHoverLeave(self):
        if self._last_collided:
            EventMap.hoverLeave(self._last_collided)
            return
        return

    def __call__(self, new):
        if new != self._last_collided:
            self.onHoverLeave()
            self._last_collided = new
            if new is not None:
                self.onHover()
            return
        return
    pass


class FPController(DirectObject, NodePath):
    _angleMap = {
        Direction.Forward: (.0, ControllerSettings.Speed, .0),
        Direction.Back: (.0, -ControllerSettings.Speed, .0),
        Direction.Left: (-ControllerSettings.Speed, .0, .0),
        Direction.Right: (ControllerSettings.Speed, .0, .0),
        Direction.ForwardRight: (SIN45*ControllerSettings.Speed, SIN45*ControllerSettings.Speed, .0),
        Direction.ForwardLeft: (-SIN45*ControllerSettings.Speed, SIN45*ControllerSettings.Speed, .0),
        Direction.BackRight: (SIN45*ControllerSettings.Speed, -SIN45*ControllerSettings.Speed, .0),
        Direction.BackLeft: (-SIN45*ControllerSettings.Speed, -SIN45*ControllerSettings.Speed, .0)}

    def __init__(self, base):
        NodePath.__init__(self, "player")
        init_player(self)
        self._mouseWatcher = base.mouseWatcherNode
        self._win = base.win
        self._renderNP = base.render
        self.reparentTo(base.render)
        self.camera = base.camera
        self.camera.setZ(1.8)
        self.camera.setY(-.6)
        self.camera.reparentTo(self)
        # movement controller                                                                                                                                 
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

        self.doMethodLater(.01, self._controllerTask, "move-task")

        self._holderNP = self.camera.attachNewNode("holder")

        # collision management
        
        _col_node = CollisionNode("playerCollider")
        _col_node.addSolid(CollisionBox((.0, .0, .9), .4, .4, .9))
        _col_node.setFromCollideMask(BitMasks.Solid)
        _col_node.setIntoCollideMask(BitMasks.Empty)
        _col_np = self.attachNewNode(_col_node)
        _col_np.show()
        _Globals.pusher.addCollider(_col_np, self)
        _Globals.base.cTrav.addCollider(_col_np, _Globals.pusher)

        # raycast interaction

        _ray_node = CollisionNode("RayCollider")
        _ray_np = base.camera.attachNewNode(_ray_node)
        _ray_node.setFromCollideMask(BitMasks.Interactable)
        _ray_node.setIntoCollideMask(BitMasks.Empty)
        _ray_np.show()
        _ray_node.addSolid(CollisionSegment(.0, .0, .0, .0, 4, .0))
        
        self._interact_handler = _InteractHandler(_ray_np)
        self._interact_handler.doMethodLater(.02, self._interact_handler.interactTask, "interact-task")
        self._holded = None

        #debug
        self.accept("l", self.ls)
        self.accept("p", lambda: print(self.getPos()))
        self.accept("o", base.render.ls)

        self.DEBUG_TASKFLAG = False

        def dbg_cam():
            base.oobe()
            self.DEBUG_TASKFLAG = not self.DEBUG_TASKFLAG
            pass

        self.accept("k", dbg_cam)
        self._moveswitch = True
        self.accept("mouse1", self._on_click_1)
        self.accept("mouse3", self._on_click_3)
        
        pass


    def _on_click_1(self):
        if self._interact_handler.onClick():
            return
        if self._holded:
            self._holded.onClick()
            return
        return

    def _on_click_3(self):
        try:
            self._holded.drop()
            self._holded = None
            return
        except AttributeError:
            return
        return
            
    def setHolded(self, holded_np):
        if self._holded:
            self._holded.drop()
        self._holded = holded_np
        return

    @property
    def holded(self):
        return self._holded

    @property
    def holder(self):
        return self._holderNP

    def setMovement(self, val):
        if val and not self._moveswitch:
            self.doMethodLater(.01, self._controllerTask, "movement-task")
            self._interact_handler.doMethodLater(.02, self._interact_handler.interactTask, "interact-task")
            self._moveswitch = True
            pass
        elif not val and self._moveswitch:
            self.removeAllTasks()
            self._moveswitch = False
            pass
        return
        
    def _changeValue(self, key, val):
        self._inputs[key] = val
        return

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
        return Direction.Undefined

    def _controllerTask(self, task):
        if self.DEBUG_TASKFLAG:
            return task.again
        self.setZ(.0)
        dire = self._getDirection()
        if dire is not Direction.Undefined:
            self.setFluidPos(self, self._angleMap[dire])
            pass
        # self.setZ(self, -.2)
        if self._mouseWatcher.hasMouse():
            x, y = self._mouseWatcher.getMouseX(), self._mouseWatcher.getMouseY()
            self.setH(self, -x * ControllerSettings.RotationSpeed)
            self.camera.setP(self.camera, y *ControllerSettings.RotationSpeed)
            if self.camera.getP() > ControllerSettings.MaxP:
                self.camera.setP(ControllerSettings.MaxP)
                pass
            elif self.camera.getP() < ControllerSettings.MinP:
                self.camera.setP(ControllerSettings.MinP)
                pass
            props = self._win.getProperties()
            self._win.movePointer(0,
                         props.getXSize() // 2,
                         props.getYSize() // 2)
        return task.again
    pass
    


