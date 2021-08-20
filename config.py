
def init_config(base):
    _Globals.base = base
    _Globals.loader = base.loader
    GUI.init()

def init_player(controller):
    _Globals.player = controller
    
class _Globals:
    base = None
    player = None
    loader = None

def get_globals():
    return _Globals

import gui

class GUI:
    NoticeBox = gui.NoticeBox()

    @staticmethod
    def init():
        GUI.NoticeBox.reparentTo(_Globals.base.aspect2d)
    

from direct.fsm.FSM import FSM
        
class _GUI_FSM(FSM):
    
    def __init__(self):
        super().__init__("gui-fsm")
        pass

    def __call__(self, event):
        if event is None:
            return
        print("requesting", event)
        self.request(event.type, event)
        return

    def enterNotice(self, event):
        GUI.NoticeBox.changeText(event.text)
        GUI.NoticeBox.show()
        return

    def exitNotice(self):
        GUI.NoticeBox.hide()
        return

    def togglePlayerMovement(self, val):
        _Globals.playercontroller.setMovement(val)

    def close(self):
        self.request("Empty")
        return
    
    def enterEmpty(self):
        pass

    def exitEmpty(self):
        pass

    def enterAction(self, event):
        event()

    def exitAction(self):
        return
GUI_FSM = _GUI_FSM()
