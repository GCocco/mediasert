# events and interactions utils
from config import get_globals
from direct.shobase.DirectObject import DirectObject
# shouldn't import other modules


_Globals = get_globals()

class Event:
    
    def __init__(self, func, *args):
        self._on_call = func
        self._args = args
        self._next = None
        pass

    def __call__(self):
        self._on_call(*self._args)
        if self._next:
            self._next()
        return

    @staticmethod
    def chainEvents(first, *tail):
        last = first
        for ev in tail:
            last._next = ev
            last = ev
        return first
    pass

class GUIEvent(Event):
    def __init__(self, state, *args):
        Event.__init__(self, _Globals.gui_fsm, *args)
        self._state = state
        pass
    pass

class NoticeEvent(GUIEvent):
    def __init__(self, text):
        GUIEvent.__init__(self, "Notice", text)
        pass
    pass

class ClickableEvent(Event, DirectObject):
    def __init__(self, func, *args, onClick=None):
        Event.__init__(self, func, *args)
        self._on_click = lambda: print("missing_function")
        if onClick:
            self._on_click = onClick
            pass
        pass
    def __call__(self):
        self.accept("mouse1", self._on_click)
        Event.__call__(self)
        pass
    pass
    
    
