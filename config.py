class Loader:
    _LOADER = None
    @staticmethod
    def init(panda_loader):
        if Loader._LOADER is not None:
            raise Exception("loader already defined")
        Loader._LOADER = panda_loader

    @staticmethod
    def loadModel(path):
        return Loader._LOADER.loadModel(path)

