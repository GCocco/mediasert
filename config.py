def init_config(base):
    _Globals.base = base
    Loader._LOADER = base.loader
    GUI.init()

class _Globals:
    base = None

class Loader:
    _LOADER = None
    
    @staticmethod
    def loadModel(path):
        return Loader._LOADER.loadModel(path)


import gui

class GUI:
    NoticeBox = gui.NoticeBox()

    @staticmethod
    def init():
        GUI.NoticeBox.reparentTo(_Globals.base.aspect2d)
    
