# gui module

from direct.gui.DirectGui import DirectFrame, OnscreenText
from config import get_globals, init_gui

_Globals = get_globals()


class NoticeBox(DirectFrame):
    def __init__(self):
        super().__init__(frameSize=(-1, 1, -.1, .1), frameColor=(.1, .1, .9, .2), pos=(.0, .0, -.3))
        self.initialiseoptions(NoticeBox)
        self._text = OnscreenText(parent=self, text="sample text", mayChange=True)
        self.hide()
        pass

    def changeText(self, text):
        self._text["text"] = text
        return
    pass


class _GUI:
    NoticeBox = NoticeBox()
    

from direct.fsm.FSM import FSM

class _GUI_FSM(FSM):

    def __init__(self):
        super().__init__("gui-fsm")
        pass

    def __call__(self, event):
        self.request(event.event_type, event)
        return

    def enterNotice(self, event):
        _GUI.NoticeBox.changeText(event.text)
        _GUI.NoticeBox.show()
        return

    def exitNotice(self):
        _GUI.NoticeBox.hide()
        return

    def togglePlayerMovement(self, val):
        _Globals.playercontroller.setMovement(val)

    def close(self):
        self.request("Empty")
        return

    def enterEmpty(self, event):
        pass

    def exitEmpty(self):
        pass

    def enterAction(self, event):
        event()
        return
    
    def exitAction(self):
        return
    pass

init_gui(_GUI_FSM())

