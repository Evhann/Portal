from ursina import *
from ursina.shaders.unlit_shader import unlit_shader

from sys import argv

from player import Player, PortalGun, Portal

from settings import SETTINGS

from switch import Switch
from cube import Cube
from core import Core
from radio import Radio
from button import Button

portal_surfaces = []

window.title = "Portal"
app = Ursina()
window.borderless = False
window.fullscreen = SETTINGS.graphics.fullscreen
window.exit_button.enabled = False
window.color = color.rgb(0,0,0)

Texture.default_filtering = SETTINGS.graphics.texture_filtering

Entity.default_shader = unlit_shader

if "--debug" in argv: debug_mode = True
else: debug_mode = False

ground = Entity(model='cube', scale=(40, 1, 40), texture="concrete_modular_ceiling2", texture_scale=(12,12))
ground.collider = BoxCollider(ground, size=ground.scale)

ceiling = Entity(model='cube', scale=(40, 1, 40), texture="concrete_modular_ceiling2", texture_scale=(10,10),
                 position=(0, 30, 0))
ceiling.collider = BoxCollider(ceiling, size=ceiling.scale)

wall1 = Entity(model='cube', scale=(1, 30, 40), texture="concrete_modular_wall5", texture_scale=(8,7),
              position=(20,15,0))
wall1.collider = BoxCollider(wall1, size=wall1.scale)

wall2 = Entity(model='cube', scale=(1, 30, 40), texture="concrete_modular_wall5", texture_scale=(8,7),
              position=(-20,15,0))
wall2.collider = BoxCollider(wall2, size=wall2.scale)

wall3 = Entity(model='cube', scale=(1, 30, 40), texture="concrete_modular_wall5", texture_scale=(8,7),
              position=(0,15,-20), rotation=(0,90,0))
wall3.collider = BoxCollider(wall3, size=wall3.scale)

wall4 = Entity(model='cube', scale=(1, 30, 40), texture="concrete_modular_wall5", texture_scale=(8,7),
              position=(0,15,20), rotation=(0,90,0))
wall4.collider = BoxCollider(wall4, size=wall4.scale)

frame = Entity(model="portal_frame", texture="portal_frame", scale=0.026, position=(-1.69,2,-19.31))

incinerator = Entity(model='glados_aperturedoor', texture='glados_aperturedoor',
                     position=(10,.8,0), scale=0.03)

portal_surfaces.append(wall1)
portal_surfaces.append(wall2)
portal_surfaces.append(wall3)
portal_surfaces.append(wall4)
portal_surfaces.append(ceiling)
portal_surfaces.append(ground)

Core(position=(10,1,3), type=1)
Core(position=(10,2,3), type=2)
Core(position=(10,3,3), type=3)

toilet = Entity(model='Toilet', texture='Toilet', position=(10,1.4,5),
              scale=0.03)
toilet.collider = BoxCollider(toilet, size=(17,54,43), center=(0,-2,26))

radio = Radio(position=(0,1,3))

Switch(position=(15,1.2,8))

Cube(position=(-10,1.1,0)) # create a basic cube
Cube(type=2, position=(-10,1.1,4)) # create a companion cube


monitor = Entity(model='lab_monitor_01', texture='lab_monitor', position=(16,10,-10),
              scale=0.15)
monitor.collider = BoxCollider(monitor,size=(23,46,24), center=(11.25,0,0))

door = Entity(model='door', texture='door', position=(-5,0.55,-19.15),
              scale=0.03)

player = Player()
gun = PortalGun(portal_surfaces)

Button(player, position=(10,0.7,8))

# Portal(position=(-1.5,1.9,-19.499), type=1) # create a blue portal
# Portal(position=(1.3,1.9,-19.499), type=2) # create a orange portal

Entity(model="portal_frame", texture="portal_frame", scale=0.026, position=(1.1,2,-19.31))

if debug_mode:
    for e in scene.entities:
        try:
            e.collider.visible = True
        except:
            continue

if debug_mode:
    print("playing assets/voices/glados_welcome_00.wav")
Audio("glados_welcome_00.wav").play()

Audio("ambient_loop1.wav", loop=True).play()

app.run()