# stuff
from enum import IntEnum
from panda3d.core import BitMask32

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
    Solid = BitMask32(7)
    Interactable = BitMask32(8)
    Empty = BitMask32.allOff()

    @staticmethod
    def fromInt(num):
        return BitMask32(num)
