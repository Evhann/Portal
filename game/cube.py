from ursina import *

class Cube(Entity):
    def __init__(self, type=1, position=(0,0,0)): #1: normal 2: companion
        super().__init__(
            model="weightedcube",
            position=position,
            collider='box',
            scale=0.03,
        )
        if type == 1:
            self.model = 'weightedcube'
            self.texture = "metal_box"
        else:
            self.model = "compcube"
            self.texture = "metal_box_skin001"
