# mediasert game by GCocco

from direct.showbase.ShowBase import ShowBase

from config import Loader

from player import FPController
from maps import Map_01


class Mediasert(ShowBase):

    def __init__(self):
        super().__init__()
        Loader.init(self.loader)
        self.disableMouse()
        self.accept("escape", exit)
    pass



if __name__ == "__main__":
    ms = Mediasert()
    me = FPController(ms)
    map = Map_01(ms)
    ms.run()
