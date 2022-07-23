from ursina import *

class PotatOS(Entity):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            model='potatOS',
            texture='potatOS',
            position=position,
            scale=0.03,
            color=color.white
        )