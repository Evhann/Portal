from ursina import *


class Switch(Button):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            parent=scene,
            model='switch001',
            texture='switch001',
            position=position,
            scale=0.03,
            color=color.white
        )
        # self.collider=BoxCollider(self, size=(30,70,30), center=(100,0,0))
        # self.collider.visible = True
        self.on_click = self._on_click_

    def _on_click_(self):
        Audio('ding_on.wav').play()