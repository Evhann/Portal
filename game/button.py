from ursina import *

class Button(Entity):
    def __init__(self, player, position=(0,0,0)):
        super().__init__(
            model='Button',
            texture='Button',
            position=position,
            scale=0.03,
            collider='box'
        )
        self.player = player
        # self.hit_info = raycast(self.world_position + (self.up*.5) , self.direction,
        #                         ignore=(self,), distance=.5, debug=False)
    
    # def update(self):
    #     if self.hit_info.hit:
    #         Audio("ding_on.wav").play()