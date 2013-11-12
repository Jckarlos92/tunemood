from handler import Handler
from tables import Tag

class Tag(Handler):

    def get(self):
        self.song = self.request.get("song")
        self.tag = self.request.get("tag")



