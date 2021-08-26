# stuff
from enum import IntEnum
from panda3d.core import BitMask32, NodePath
from direct.showbase.DirectObject import DirectObject
import events
from config import get_globals

_Globals = get_globals()


class Direction(IntEnum):
    Forward = 1
    Back = -1
    Left = -4
    Right = 4
    ForwardRight = Forward + Right
    ForwardLeft = Forward + Left
    BackRight = Back + Right
    BackLeft = Back + Left
    Undefined = 0
    pass

class BitMasks:
    Solid = BitMask32(5)
    Interactable = BitMask32(8)
    Empty = BitMask32.allOff()

    @staticmethod
    def fromInt(num):
        return BitMask32(num)


class EventMap:
    _EVENT_MAP = {"closed_door": events.NoticeText("Apri", onClick=events.NoticeText("La porta è chiusa"))}

    @staticmethod
    def update(event_id, event):
        EventMap._EVENT_MAP[event_id] = event
        return

    @staticmethod
    def remove(event_id):
        try:
            EventMap._EVENT_MAP.pop(event_id)
            return
        except KeyError:
            return
        return
    
    @staticmethod
    def startEvent(event_id):
        if event_id in EventMap._EVENT_MAP:
            _Globals.gui_fsm(EventMap._EVENT_MAP[event_id])
            return True
        return False
    
    @staticmethod
    def clickEvent(event_id):
        _Globals.gui_fsm(EventMap._EVENT_MAP[event_id].onClick)
        return
    pass


