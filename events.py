# events and interactions utils
from config import get_globals

_Globals = get_globals()


class Event:
    def __init__(self, onClick=None):
        self._next = None
        self._onclick = onClick

    def append(self, next):
        self._next = next

    @property
    def next(self):
        return self._next

    @property
    def onClick(self):
        return self._onclick

    @property
    def type(self):
        return None
    
    @staticmethod
    def chainEvents(start_event, *args):
        last = start_event
        for event in args:
            start_event.append(event)
        return last
            

class NoticeText(Event):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self._text = text

    @property
    def text(self):
        return self._text

    @property
    def type(self):
        return "Notice"


class ActionEvent(Event):
    def __init__(self, *args):
        self._actions = args

    @property
    def type(self):
        return "Action"

    @property
    def actions(self):
        return self._actions

    def __call__(self):
        for action in self._actions:
            action()
        

class EventMap:
    _EVENT_MAP = {"closed_door": NoticeText("Apri", onClick=NoticeText("La porta è chiusa"))}
    @staticmethod
    def update(event_id, event):
        EventMap._EVENT_MAP[event_id] = event
        return

    @staticmethod
    def remove(event_id):
        EventMap._EVENT_MAP.pop(event_id)

    @staticmethod
    def startEvent(event_id):
        _Globals.gui_fsm(EventMap._EVENT_MAP[event_id]) 

    def clickEvent(event_id):
        _Globals.gui_fsm(EventMap._EVENT_MAP[event_id].onClick)
