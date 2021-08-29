# events and interactions utils
from config import get_globals
from direct.showbase.DirectObject import DirectObject
from types import FunctionType
# shouldn't import other modules


_Globals = get_globals()

class Event:
    @staticmethod
    def _blank():
        print("SSSS")
        return

    @staticmethod
    def chainEvents(first, *tail):
        last = first
        for ev in tail:
            last._next = ev
            last = ev
        return first

    def append(self, ev):
        self._next = ev

    def __init__(self, func, *args):
        self._func = func
        self._args = args
        self._next = None
        pass
    
    def __call__(self):
        self._func(*self._args)
        if callable(self._next):
            return self._next()
        return
    pass


class CollisionEvent(Event):
    def __init__(self, on_hover, on_click=None, on_leave=None):
        self._on_hover = on_hover

        self._on_click = Event._blank
        if on_click:
            self._on_click = on_click
            
        self._on_leave = CleanGUIEvent
        if on_leave:
            self._on_leave = on_leave
        self._next = None
        pass

    def on_click(self):
        self._on_click()
        return

    def on_leave(self):
        self._on_leave()
        return

    def on_hover(self):
        self._on_hover()
        return


class GUIEvent(Event):
    def __init__(self, state):
        self._state = state
        pass

    @property
    def event_type(self):
        return self._state

    def __call__(self):
        _Globals.gui_fsm(self)
        return
    pass

class CleanGUIEvent(Event):
    event_type = "Empty"
    
    def __init__(self):
        _Globals.gui_fsm(type(self))
        pass


class NoticeEvent(GUIEvent):
    def __init__(self, text):
        GUIEvent.__init__(self, "Notice")
        self._text = text
        pass

    @property
    def text(self):
        return self._text
    
    pass

    
    
