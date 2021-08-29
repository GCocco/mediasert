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
    Solid = BitMask32(0x11)
    Interactable = BitMask32(0x1100)
    Empty = BitMask32.allOff()

    @staticmethod
    def fromInt(num):
        return BitMask32(num)


class EventMap:
    _EVENT_MAP = {"closed_door": events.CollisionEvent(events.NoticeEvent("Apri"),
                                                       on_click=events.NoticeEvent("La porta è chiusa"))}

    @staticmethod
    def bind(event_id, event):
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
    def hover(event_id):
        try:
            EventMap._EVENT_MAP[event_id].on_hover()
            pass
        except KeyError:
            pass
        return
    
    @staticmethod
    def click(event_id):
        try:
            EventMap._EVENT_MAP[event_id].on_click()
            pass
        except KeyError:
            pass
        return
    
    @staticmethod
    def hoverLeave(event_id):
        try:
            EventMap._EVENT_MAP[event_id].on_leave()
            pass
        except:
            pass
        return
    pass


