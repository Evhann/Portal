from ursina import *

class Core(Entity):
    def __init__(self, position=(0,0,0), type=1):
        super().__init__(
            model='Glados_ball',
            position=position,
            scale=0.03,
            collider='box'
        )
        if type == 1:
            self.texture = "Glados_ball_01"
        elif type == 2:
            self.texture = "Glados_ball_02"
        else:
            self.texture = "Glados_ball_03"