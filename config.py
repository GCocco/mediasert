# QUESTO MODULO NON DEVE IMPORTARE MODULI CUSTOM IN QUANTO
# RISCHIA DI CREARE DIPENDENZE CIRCOLARI


def init_config(base):
    from panda3d.core import CollisionTraverser
    
    _Globals.base = base
    _Globals.base.cTrav = CollisionTraverser()
    _Globals.loader = base.loader
    _Globals.render = base.render
    return

def init_gui(gui_fsm):
    _Globals.gui_fsm = gui_fsm
    return

def init_player(controller):
    _Globals.player = controller
    return
    
class _Globals:
    base = None
    player = None
    loader = None
    render = None
    gui_fsm = None

def get_globals():
    return _Globals
