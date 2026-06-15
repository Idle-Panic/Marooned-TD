import pygame
import asyncio
import sys

from Scripts.level import Tilemap, Prop
from Scripts.utilities import load_image, load_images, convert_tilemap, process_font, load_audio, SortedGroup
from Scripts.gui import GUI
from Scripts.tower import Tower
from Scripts.enemy import Enemy, Wave_Data

if sys.platform == "emscripten":
    platform.window.canvas.style.imageRendering = "pixelated"

class Game:
    def __init__(self):
        pygame.init()
        
        self.clock = pygame.time.Clock()
        
        self.flags = False
        if sys.platform != "emscripten":
            self.flags = pygame.SCALED
        
        pygame.display.set_caption("Marooned TD")
        self.screen = pygame.display.set_mode((360, 240), self.flags)
        
        self.state = "title"
        self.gamespeed = 1
        self.time_sped_up = 0
        
        self.render_group = SortedGroup()
        
        self.tile_size = 32
        self.camera_offset = [0, 0]
        
        self.colors = {
        "dark_brown" : (35, 23, 18),
        "gray" : (123, 123, 123),
        "green" : (88, 211, 50),
        "red" : (224, 60, 40),
        "dark_blue" : (13, 32, 48),
        "light_blue" : (152, 220, 255),
        "yellow" : (255, 231, 55),
        "black" : (21, 21, 21)
        }
        
        self.sounds = {
        "click" : load_audio("click.ogg", "sfx"),
        "sword" : load_audio("sword.ogg", "sfx"),
        "construction" : load_audio("construction.ogg", "sfx"),
        "slingshot" : load_audio("slingshot.ogg", "sfx"),
        "explosion" : load_audio("explosion.ogg", "sfx"),
        "gunshot" : load_audio("gunshot.ogg", "sfx")
        }
        for sound in self.sounds:
            self.sounds[sound].set_volume(0.4)
        
        self.assets = {
        "ground_tiles" : load_images("ground_tiles"),
        "water_tiles" : load_images("water_tiles"),
        "path_tiles" : load_images("path_tiles")
        }
        
        self.prop_images = {
        "cave" : load_image("props/cave.png"),
        "palm" : load_image("props/palm.png"),
        "camp" : load_image("props/camp.png"),
        }

        self.prop_rects = {
        "cave" : (self.img_to_rect("cave", (368, 128)),),
        "camp" : (self.img_to_rect("camp", (96, 162)),),
        "palm" : (self.img_to_rect("palm", (160, 124)), self.img_to_rect("palm", (284, 94)), self.img_to_rect("palm", (414, 160)), self.img_to_rect("palm", (388, 278)),
        self.img_to_rect("palm", (254, 394)), self.img_to_rect("palm", (64, 320)),),
        }
        self.prop_group = pygame.sprite.Group()
        
        for img in self.prop_images:
            for rect in self.prop_rects:
                if img == rect:
                    for r in self.prop_rects[img]:
                        prop = Prop(self.prop_images.get(img), r)
                        self.prop_group.add(prop)
                        self.render_group.add(prop)
        
        self.enemy_stats = [
        {"type" : "crab", "health" : 6, "speed" : 0.3, "coins" : 1},
        {"type" : "bat", "health" : 8, "speed" : 0.5, "coins" : 2},
        {"type" : "snapping_turtle", "health" : 28, "speed" : 0.2, "coins" : 3},
        {"type" : "pirate", "health" : 32, "speed" : 0.35, "coins" : 3},
        {"type" : "captain", "health" : 99, "speed" : 0.3, "coins" : 5},
        ]
        
        self.tower_stats = [
        {"type" : "coconut_launcher", "price" : [30, 20, 60], "attack" : [1, 1, 3], "speed" : [2, 1.3, 1], "range" : [80, 95, 120], "attack_type" : "normal"},
        {"type" : "cannon", "price" : [55, 50, 95], "attack" : [3, 7, 18], "speed" : [4, 3.5, 3], "range" : [60, 65, 75], "attack_type" : "area_attack"},
        {"type" : "puckle_gun", "price" : [60, 65, 99], "attack" : [1, 1, 2], "speed" : [0.8, 0.5, 0.3], "range" : [75, 85, 95], "attack_type" : "normal"},
        ]
        
        self.ground_tilemap = Tilemap(self, self.tile_size, 15, convert_tilemap("ground_tiles.txt", self.tile_size, 15), "ground_tiles", 0, False)
        self.water_tilemap = Tilemap(self, self.tile_size, 21, convert_tilemap("water_tiles.txt", self.tile_size, 21), "water_tiles", -96, True)
        self.path_tilemap = Tilemap(self, self.tile_size, 15, convert_tilemap("path_tiles.txt", self.tile_size, 15), "path_tiles", 0, False)
        self.path_mask = pygame.mask.from_surface(self.path_tilemap.surface)
        
        self.gui = GUI(self)
        self.wave_data = Wave_Data(self, "waves.txt")
        
        self.mouse_pos = (0, 0)
        
        self.path = [(368, 112), (368, 176), (304, 176), (304, 112), (240, 112), (240, 192), (272, 224), (272, 320), (320, 368), (368, 368), (368, 288),
        (320, 240), (224, 240), (176, 288), (176, 368), (112, 368), (112, 240), (144, 240), (144, 176), (112, 176), (112, 144)]
        
        self.tower_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.projectile_group = pygame.sprite.Group()
        self.area_attack_group = pygame.sprite.Group()
        
        self.wave = 1
        self.wave_started = False
        
        self.coins = 80
        self.health = 100
        self.tower_amount = 0
    
    def img_to_rect(self, image, pos):
        rect = self.prop_images[image].get_rect(midbottom = pos)
        return rect
    
    def add_tower(self, type, position):
        if self.tower_stats[type]["price"][0] <= self.coins:
            tower = Tower(self.tower_stats[type], position, self)
            self.tower_group.add(tower)
            self.render_group.add(tower)
            
            self.coins -= self.tower_stats[type]["price"][0]
            self.sounds["construction"].play()
                
    def add_enemy(self, type):
        for i in self.enemy_stats:
            if type == i["type"]:
                enemy = Enemy(self.enemy_stats[self.enemy_stats.index(i)], self)
                self.enemy_group.add(enemy)
                self.render_group.add(enemy)
                
    def determine_path_index(self, key, position):
        if key == 1073741903:
            self.path.append((int((position[0] - self.camera_offset[0]) - (position[0] - self.camera_offset[0]) % self.tile_size) + 32, 
            int((position[1] - self.camera_offset[1]) - (position[1] - self.camera_offset[1]) % self.tile_size) + 16))
        if key == 1073741904:
            self.path.append((int((position[0] - self.camera_offset[0]) - (position[0] - self.camera_offset[0]) % self.tile_size), 
            int((position[1] - self.camera_offset[1]) - (position[1] - self.camera_offset[1]) % self.tile_size) + 16))
        if key == 1073741905:
            self.path.append((int((position[0] - self.camera_offset[0]) - (position[0] - self.camera_offset[0]) % self.tile_size) + 16, 
            int((position[1] - self.camera_offset[1]) - (position[1] - self.camera_offset[1]) % self.tile_size) + 32))
        if key == 1073741906:
            self.path.append((int((position[0] - self.camera_offset[0]) - (position[0] - self.camera_offset[0]) % self.tile_size) + 16, 
            int((position[1] - self.camera_offset[1]) - (position[1] - self.camera_offset[1]) % self.tile_size)))
        if key == 32:
            self.path.append((int((position[0] - self.camera_offset[0]) - (position[0] - self.camera_offset[0]) % self.tile_size) + 16, 
            int((position[1] - self.camera_offset[1]) - (position[1] - self.camera_offset[1]) % self.tile_size) + 16))
            
    def check_mouse_collisions(self, mouse_being_pressed):
        if self.mouse_pos[0] > 210:
            return None
        if self.gui.components["steering_wheel"].being_held == True:
            return None
            
        self.gui.tower_displaying = None
        self.gui.enemy_displaying = None
        
        for tower in self.tower_group:
            if tower.image_lower.get_rect(center = tower.position).move((0, 16)) \
            .collidepoint(self.mouse_pos[0] - self.camera_offset[0], self.mouse_pos[1] - self.camera_offset[1]):
                self.gui.gui_mode = "viewing_tower"
                self.gui.tower_displaying = tower
                return True
        for enemy in self.enemy_group:
            if enemy.rect.collidepoint(self.mouse_pos[0] - self.camera_offset[0], self.mouse_pos[1] - self.camera_offset[1]):
                self.gui.gui_mode = "viewing_enemy"
                self.gui.enemy_displaying = enemy
                return True
        return False
    
    async def main(self):
        while True:
            keyboard_movement = [0, 0]
            
            if sys.platform == "emscripten":
                self.dt = self.clock.tick()/16.6
            else:
                self.clock.tick(60)
                self.dt = 1
                
            self.time_sped_up += self.clock.get_time() * (self.gamespeed - 1)
            
            if self.state != "playing":
                self.gui.gui_mode = self.state
            elif self.state == "playing" and self.gui.gui_mode == "title":
                self.gui.gui_mode = "stats"
            
            self.mouse_being_pressed = False
            for i in pygame.mouse.get_pressed():
                if i == True:
                    self.mouse_being_pressed = True
            if self.mouse_being_pressed:
                self.mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11 and sys.platform != "emscripten":
                        if self.flags == pygame.SCALED:
                            self.flags = pygame.SCALED | pygame.FULLSCREEN
                        else:
                            self.flags = pygame.SCALED
                        pygame.display.set_mode((360, 240), self.flags)
            if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]:
                keyboard_movement[0] -= 1
            if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
                keyboard_movement[0] += 1
            if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]:
                keyboard_movement[1] -= 1
            if pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]:
                keyboard_movement[1] += 1
                    #DETERMINE PATH INDICES (DEVELOPMENT ONLY)
                    #if event.key in [pygame.K_SPACE, pygame.K_LEFT, pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN]:
                    #    self.determine_path_index(event.key, pygame.mouse.get_pos())
            
            if self.state == "playing":
                self.gui.components["steering_wheel"].update(self.mouse_being_pressed, self.mouse_pos, self.camera_offset, self.dt, keyboard_movement)
            
            self.gui.components["buttons"].check_collisions(self.mouse_being_pressed, self.mouse_pos)
            if self.mouse_being_pressed:
                if self.check_mouse_collisions(self.mouse_being_pressed) == False:
                    if self.gui.gui_mode in ["viewing_enemy", "viewing_tower"]:
                        self.gui.gui_mode = "stats"
            
            self.wave_data.check_and_add(self.wave, self.wave_started, self.time_sped_up)
            
            self.tower_amount = len(self.tower_group)
            
            self.camera_offset = [pygame.math.clamp(self.camera_offset[0], -120-256, 256), pygame.math.clamp(self.camera_offset[1], -240-128, 128)]
            render_offset = [int(self.camera_offset[0]), int(self.camera_offset[1])]
            if self.state == "playing":
                self.water_tilemap.sinewave_move(self.gamespeed)
                self.water_tilemap.render(self.screen, render_offset)
                self.ground_tilemap.render(self.screen, render_offset)
                self.path_tilemap.render(self.screen, render_offset)
                
                self.enemy_group.update(self.screen, render_offset, self.path, self, self.dt, self.gamespeed)
                self.sorted_enemy_group = sorted(self.enemy_group.sprites(), key = lambda spr: spr.distance_travelled, reverse=True)
                self.tower_group.update(self.screen, render_offset, self.sorted_enemy_group, self)
                
                self.render_group.draw(self.screen, render_offset)
                self.projectile_group.update(self.screen, render_offset, self.dt, self.gamespeed)
                self.area_attack_group.update(self.screen, render_offset, self.dt, self.gamespeed)
            
            self.gui.render(self.screen, render_offset)

            pygame.display.update()
            
            await asyncio.sleep(0)

asyncio.run(Game().main())
