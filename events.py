# events and interactions utils



class Event:
    def __init__(self, onClick=None):
        self._next = None
        self._onclick = onClick

    def append(self, next):
        self._next = next

    @property
    def next(self):
        return self._next

    @property
    def onClick(self):
        return self._onclick

    @property
    def type(self):
        return None
    
    @staticmethod
    def chainEvents(start_event, *args):
        last = start_event
        for event in args:
            start_event.append(event)
        return last
            

class NoticeText(Event):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self._text = text

    @property
    def text(self):
        return self._text

    @property
    def type(self):
        return "Notice"


EVENT_MAP = {"closed_door": NoticeText("Apri", onClick=NoticeText("Questa porta è chiusa")),
             "kaffe": NoticeText("Compra Kafffffèèèèèèèèèèèèèè")}
        
