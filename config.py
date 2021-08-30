# QUESTO MODULO NON DEVE IMPORTARE MODULI CUSTOM IN QUANTO
# RISCHIA DI CREARE DIPENDENZE CIRCOLARI


def init_config(base):
    from panda3d.core import CollisionTraverser, CollisionHandlerPusher
    
    _Globals.base = base
    _Globals.base.cTrav = CollisionTraverser()
    _Globals.base.cTrav.setRespectPrevTransform(True)
    _Globals.pusher = CollisionHandlerPusher()
    _Globals.loader = base.loader
    _Globals.render = base.render
    return

def init_gui(gui_fsm):
    _Globals.gui_fsm = gui_fsm
    return

def init_player(controller):
    _Globals.player = controller
    return

def init_world(world):
    _Globals.world = world
    print("AAAAAAAAAAAAAAAA")
    return

def set_map(_map):
    _Globals.map = _map
    return

class _Globals:
    base = None
    player = None
    loader = None
    render = None
    gui_fsm = None
    world = None

def get_globals():
    return _Globals
