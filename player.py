from direct.showbase.DirectObject import DirectObject
from panda3d.core import NodePath

from settings import ControllerSettings
from utils import Direction, BitMasks
from panda3d.core import CollisionTraverser, CollisionSphere, CollisionNode, CollisionHandlerPusher
from panda3d.core import CollisionLine, CollisionHandlerQueue, CollisionRay
from panda3d.core import Thread
from events import EVENT_MAP
from config import GUI_FSM
SIN45 = 0.7071


class _InteractHandler(DirectObject):
    def __init__(self):
        self._interrupt = False
        self._last_collided = None

    def onHover(self):
        if self._last_collided is not None:
            GUI_FSM(EVENT_MAP[self._last_collided.getTag("interactable_id")])

    def onClick(self):
        if self._last_collided is not None:
            GUI_FSM(EVENT_MAP[self._last_collided.getTag("interactable_id")].onClick)
    
    def onHoverLeave(self):
        if self._last_collided:
            GUI_FSM.close()
        return

    def __call__(self, new):
        if new != self._last_collided:
            self.onHoverLeave()
            self._last_collided = new
            if new is not None:
                self.onHover()
            


class FPController(DirectObject, NodePath):
    _angleMap = {
        Direction.Forward: (0, ControllerSettings.Speed, 0),
        Direction.Back: (0, -ControllerSettings.Speed, 0),
        Direction.Left: (-ControllerSettings.Speed, 0, 0),
        Direction.Right: (ControllerSettings.Speed, 0, 0),
        Direction.ForwardRight: (SIN45*ControllerSettings.Speed, SIN45*ControllerSettings.Speed, 0),
        Direction.ForwardLeft: (-SIN45*ControllerSettings.Speed, SIN45*ControllerSettings.Speed, 0),
        Direction.BackRight: (SIN45*ControllerSettings.Speed, -SIN45*ControllerSettings.Speed, 0),
        Direction.BackLeft: (-SIN45*ControllerSettings.Speed, -SIN45*ControllerSettings.Speed, 0)}
    
    def __init__(self, base):

        NodePath.__init__(self, "player")
        self._mouseWatcher = base.mouseWatcherNode
        self._win = base.win
        self._renderNP = base.render
        self.reparentTo(base.render)
        self.camera = base.camera
        self.camera.setZ(2.5)
        self.camera.setY(-.2)
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

        self.doMethodLater(.01, self._controllerTask, "move-task")

        # collision management

        self._trav = CollisionTraverser()
        _col_node = CollisionNode("playerCollider")
        _col_node.addSolid(CollisionSphere(0.0, 0.0, 0.0, 1.5))
        _col_node.setFromCollideMask(BitMasks.Solid) 
        _col_node.setIntoCollideMask(BitMasks.Empty)
        _col_np = self.attachNewNode(_col_node)
        self._pusher = CollisionHandlerPusher()
        self._pusher.addCollider(_col_np, self)
        self._trav.addCollider(_col_np, self._pusher)

        # raycast interaction

        _ray_node = CollisionNode("RayCollider")
        _ray_np = base.camera.attachNewNode(_ray_node)
        _ray_node.setFromCollideMask(BitMasks.Interactable)
        _ray_node.setIntoCollideMask(BitMasks.Empty)
        _ray_np.show()
        _ray_node.addSolid(CollisionLine((.0, .0, .0), (.0, -.4,.0)))
        self._queue = CollisionHandlerQueue()
        self._interact_trav = CollisionTraverser()
        self._interact_trav.addCollider(_ray_np, self._queue)
        self.doMethodLater(.02, self._interactTask, "interact-task")

        self._interact_handler = _InteractHandler()

        #debug
        self.accept("l", self.ls)
        self.accept("p", lambda: print(self.getPos()))
        self.accept("o", base.render.ls)

        self.DEBUG_TASKFLAG = False
        
        def dbg_cam():
            base.oobe()
            self.DEBUG_TASKFLAG = not self.DEBUG_TASKFLAG

        self.accept("k", dbg_cam)
        self._moveswitch = True
        self.accept("mouse1", self._interact_handler.onClick)

    def setMovement(self, val):
        if val and not self._moveswitch:
            self.doMethodLater(.01, self._controllerTask, "movement-task")
            self.doMethodLater(.02, self._interactTask, "interact-task")
            self._moveswitch = True
        elif not val and self._moveswitch:
            self.removeAllTasks()
            self._moveswitch = False
        return
        
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
        if self._mouseWatcher.hasMouse():
            if self.DEBUG_TASKFLAG:
                return task.again
            x, y = self._mouseWatcher.getMouseX(), self._mouseWatcher.getMouseY()
            self.setH(self, -x * ControllerSettings.RotationSpeed)
            self.camera.setP(self.camera, y *ControllerSettings.RotationSpeed)
            if self.camera.getP() > ControllerSettings.MaxP:
                self.camera.setP(ControllerSettings.MaxP)
            elif self.camera.getP() < ControllerSettings.MinP:
                self.camera.setP(ControllerSettings.MinP)            
            props = self._win.getProperties()
             
            self._win.movePointer(0,
                         props.getXSize() // 2,
                         props.getYSize() // 2)
        self._trav.traverse(self._renderNP)
            
        return task.again

    def _interactTask(self, task):
        self._interact_trav.traverse(self._renderNP)
        if self._queue.getNumEntries():
            self._queue.sortEntries()
            self._interact_handler(self._queue.getEntry(0).getIntoNode())
            return task.again
        self._interact_handler(None)
        return task.again

    


