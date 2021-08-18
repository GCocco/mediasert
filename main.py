# mediasert game by GCocco

from direct.showbase.ShowBase import ShowBase

import config

from player import FPController
from maps import Map_01

class Mediasert(ShowBase):

    def __init__(self):
        super().__init__()
        config.init_config(self)
        self.disableMouse()
        self.accept("escape", exit)
    pass



if __name__ == "__main__":
    ms = Mediasert()
    me = FPController(ms)
    config.init_player(me)
    map = Map_01(ms)
    ms.run()
