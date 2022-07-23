from ursina import *
from ursina import curve
from settings import SETTINGS

class Portal(Entity):
    def __init__(self, type, position=(0,0,0)): # type 1 = blue, 2 = orange
        super().__init__(
            model='quad',
            texture='white_cube',
            position=position,
            color=color.white,
            scale=Vec2(1.8,2.77),
            double_sided=True
        )
        texture_buffer = base.win.makeTextureBuffer("", 0, 0)
        texture_buffer.setSort(-100)
        buffer_texture = texture_buffer.getTexture()
        cam = base.makeCamera(texture_buffer)
        cam.reparentTo(camera)

        self.texture = Texture(buffer_texture)
        # self.view = Entity(model='quad', scale=self.scale,
        #                    position=self.position)
        # self.view.position.z = self.position.z + 1
        if type == 1:
            self.color = color.blue
        elif type == 2:
            self.color = color.orange

    def on_enable(self):
        Audio('portal_open1.wav').play()
    
    def on_disable(self):
        Audio('portal_close1.wav').play()

class PortalGun(Entity):
    def __init__(self, portal_surfaces: list, model_detail=2):
        super().__init__(
            parent=camera.ui,
            model='portalgun',
            texture='portalgun',
            scale=0.048,
            rotation=(-10,55,20),
            origin=(-12,9,-6)
        )
        # if model_detail == 1:
        #     self.model == "portalgun_low"
        # else:
        #     self.model == "portalgun"
        self.walls = portal_surfaces

    def input(self, key):
        for wall in self.walls:
            if wall.hovered:
                if key == 'left mouse down':
                    portal = Portal(type=1, position=mouse.world_point)
                    Audio('portalgun_shoot_blue1.wav').play()
                    # print("new blue portal at "+str(portal.position))
                    
                if key == 'right mouse down':
                    portal = Portal(type=2, position=mouse.world_point)
                    Audio('portalgun_shoot_red1.wav').play()
                    # print("new orange portal at "+str(portal.position))


"""
Edited ursina.prefabs.first_person_controller.FirstPersonController
https://github.com/pokepetter/ursina/blob/master/ursina/prefabs/first_person_controller.py#L4
"""
class Player(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.speed = 6
        self.height = 2
        self.camera_pivot = Entity(parent=self, y=self.height)

        camera.parent = self.camera_pivot
        camera.position = (0,0,0)
        camera.rotation = (0,0,0)
        camera.fov = 100
        mouse.locked = True
        self.mouse_sensitivity = Vec2(50, 50)

        self.gravity = 1
        self.grounded = False
        self.jump_height = 2.0
        self.jump_up_duration = .25
        self.fall_after = .29 # will interrupt jump up
        self.jumping = False
        self.air_time = 0

        for key, value in kwargs.items():
            setattr(self, key ,value)

        # make sure we don't fall through the ground if we start inside it
        if self.gravity:
            ray = raycast(self.world_position+(0,self.height,0), self.down, ignore=(self,))
            if ray.hit:
                self.y = ray.world_point.y


    def update(self):
        self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]

        self.camera_pivot.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity[0]
        self.camera_pivot.rotation_x= clamp(self.camera_pivot.rotation_x, -90, 90)

        self.direction = Vec3(
            self.forward * (held_keys[str(SETTINGS.keyboard.move_forward)] - held_keys[str(SETTINGS.keyboard.move_backward)])
            + self.right * (held_keys[str(SETTINGS.keyboard.move_right)] - held_keys[str(SETTINGS.keyboard.move_left)])
            ).normalized()

        feet_ray = raycast(self.position+Vec3(0,0.5,0), self.direction, ignore=(self,), distance=.5, debug=False)
        head_ray = raycast(self.position+Vec3(0,self.height-.1,0), self.direction, ignore=(self,), distance=.5, debug=False)
        move_amount = self.direction * time.dt * self.speed
        if not feet_ray.hit and not head_ray.hit:
            if self.speed <= 9.2 and move_amount != Vec3(0):
                self.speed += .02
                move_amount = self.direction * time.dt * self.speed

            if raycast(self.position+Vec3(-.0,1,0), Vec3(1,0,0), distance=.5, ignore=(self,)).hit:
                move_amount[0] = min(move_amount[0], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(-1,0,0), distance=.5, ignore=(self,)).hit:
                move_amount[0] = max(move_amount[0], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(0,0,1), distance=.5, ignore=(self,)).hit:
                move_amount[2] = min(move_amount[2], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(0,0,-1), distance=.5, ignore=(self,)).hit:
                move_amount[2] = max(move_amount[2], 0)

            self.position += move_amount


        if self.gravity:
            # gravity
            ray = raycast(self.world_position+(0,self.height,0), self.down, ignore=(self,))
            # ray = boxcast(self.world_position+(0,2,0), self.down, ignore=(self,))

            if ray.distance <= self.height+.1:
                if not self.grounded:
                    self.land()
                self.grounded = True
                # make sure it's not a wall and that the point is not too far up
                if ray.world_normal.y > .7 and ray.world_point.y - self.world_y < .5: # walk up slope
                    self.y = ray.world_point[1]
                return
            else:
                self.grounded = False

            # if not on ground and not on way up in jump, fall
            self.y -= min(self.air_time, ray.distance-.05) * time.dt * 100
            self.air_time += time.dt * .25 * self.gravity


    def input(self, key):
        if key == 'space':
            self.jump()


    def jump(self):
        if not self.grounded:
            return

        self.grounded = False
        self.animate_y(self.y+self.jump_height, self.jump_up_duration, resolution=int(1//time.dt), curve=curve.out_expo)
        invoke(self.start_fall, delay=self.fall_after)


    def start_fall(self):
        self.y_animator.pause()
        self.jumping = False

    def land(self):
        # print('land')
        self.air_time = 0
        self.grounded = True


    def on_enable(self):
        mouse.locked = True


    def on_disable(self):
        mouse.locked = False
