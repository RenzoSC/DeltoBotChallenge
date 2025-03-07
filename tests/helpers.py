from types import SimpleNamespace

class MyMessage:
    """This class can be used to simulate the Message object from the Telegram library"""
    def __init__(self, text):
        self.text = text
        self.replies = []

    async def reply_text(self, text, **kwargs):
        self.replies.append(text)
        return text    

class MyUpdater:
    """This class can be used to simulate the Update object from the Telegram library"""
    def __init__(self, text):
        self.message = MyMessage(text)
        self.effective_user = SimpleNamespace(id=1)