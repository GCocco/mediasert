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
    def next(self):
        return self._next

    @property
    def type(self):
        return None


class NoticeText(Event):
    def __init__(self, text):
        super().__init__()
        self._text = text

    @property
    def text(self):
        return self._text

    @property
    def type(self):
        return "Notice"


EVENT_MAP = {"closed_door": NoticeText("la porta è chiusa")}
        
