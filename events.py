# events and interactions utils


class InteractableEvent:
    def __init__(self, notice, on_click):
        pass
    pass


class Event:
    def __init__(self):
        self._next = None

    def append(self, next):
        self._next = next

    @property
    def getNext(self):
        return self._next


class NoticeText(Event):
    def __init__(self, text):
        super().__init__()
        self._text = text

    @property
    def getText(self):
        return self._text



EVENT_MAP = {"closed_door": NoticeText("la porta è chiusa")}
        
