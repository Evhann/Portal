from ursina import *

class Radio(Entity):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            model='Radio',
            texture='Radio1',
            position=position,
            scale=0.03,
            color=color.white,
        )
        self.collider=BoxCollider(self, size=(20,16,10), center=(0,-8,15))
        self.song = Audio("looping_radio_mix.wav", loop=True)

        self.song.play()
    
    def on_disable(self):
        self.song.stop()