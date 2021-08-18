# gui module

from direct.gui.DirectGui import DirectFrame, OnscreenText

class NoticeBox(DirectFrame):
    def __init__(self):
        super().__init__(frameSize=(-1, 1, -.1, .1), frameColor=(.1, .1, .9, .2), pos=(.0, .0, -.3))
        self.initialiseoptions(NoticeBox)
        self._text = OnscreenText(parent=self, text="sample text", mayChange=True)

    def changeText(self, text):
        self._text["text"] = text
        return
