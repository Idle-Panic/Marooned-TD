import pygame
import asyncio
import sys

from Scripts.level import Tilemap, Props
from Scripts.utilities import load_image, load_images, convert_tilemap, process_font, load_audio
from Scripts.gui import GUI
from Scripts.tower import Tower
from Scripts.enemy import Enemy, Wave_Data

if sys.platform == "emscripten":
    platform.window.canvas.style.imageRendering = "pixelated"

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Marooned TD")
        self.screen = pygame.display.set_mode((360, 240), pygame.SCALED)
        
        self.tile_size = 32
        self.camera_offset = [0, 0]
        
        self.colors = {
        "dark_brown" : (35, 23, 18),
        "gray" : (123, 123, 123)
        }
        
        self.assets = {
        "ground_tiles" : load_images("ground_tiles"),
        "water_tiles" : load_images("water_tiles"),
        "path_tiles" : load_images("path_tiles")
        }
        
        self.enemy_stats = [
        {"type" : "crab", "health" : 5, "speed" : 0.25},
        ]
        
        self.tower_stats = [
        {"type" : "coconut_launcher", "price" : 25, "attack" : 1, "speed" : 2, "range" : 80, "attack_type" : "normal"},
        ]
        
        self.ground_tilemap = Tilemap(self, self.tile_size, 15, convert_tilemap("ground_tiles.txt", self.tile_size, 15), "ground_tiles", 0, False)
        self.water_tilemap = Tilemap(self, self.tile_size, 21, convert_tilemap("water_tiles.txt", self.tile_size, 21), "water_tiles", -96, True)
        self.path_tilemap = Tilemap(self, self.tile_size, 15, convert_tilemap("path_tiles.txt", self.tile_size, 15), "path_tiles", 0, False)
        
        load_audio("main_theme.ogg", "music")
        pygame.mixer.music.play(-1, 0.0, 4000)
        
        self.gui = GUI(self)
        self.props = Props()
        self.wave_data = Wave_Data(self, "waves.txt")
        
        self.mouse_pos = (0, 0)
        
        self.path = [(368, 112), (368, 176), (304, 176), (304, 112), (240, 112), (240, 192), (272, 224), (272, 320), (320, 368), (368, 368), (368, 288),
        (320, 240), (224, 240), (176, 288), (176, 368), (112, 368), (112, 240), (144, 240), (144, 176), (112, 176), (112, 144)]
        
        self.tower_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.projectile_group = pygame.sprite.Group()
        
        self.wave = 1
        self.wave_started = False
        
        self.coins = 80
        self.health = 100
        self.tower_amount = 0
        
    def add_tower(self, type, position):
        for i in self.tower_stats:
            if type == i["type"]:
                self.tower_group.add(Tower(self.tower_stats[self.tower_stats.index(i)], position))
                
    def add_enemy(self, type):
        for i in self.enemy_stats:
            if type == i["type"]:
                self.enemy_group.add(Enemy(self.enemy_stats[self.enemy_stats.index(i)]))
                
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

    async def main(self):
        while True:
            
            self.mouse_being_pressed = False
            for i in pygame.mouse.get_pressed():
                if i == True:
                    self.mouse_being_pressed = True
            if self.mouse_being_pressed:
                self.mouse_pos = pygame.mouse.get_pos()
            
            self.gui.components["buttons"].check_collisions(self.mouse_being_pressed, self.mouse_pos)
            
            self.wave_data.check_and_add(self.wave, self.wave_started)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and self.wave_started == False:
                        self.wave_started = True
                        
                # DETERMINE PATH INDICES (DEVELOPMENT ONLY)
                #    if event.key in [pygame.K_SPACE, pygame.K_LEFT, pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN]:
                #        self.determine_path_index(event.key, pygame.mouse.get_pos())
                
            self.tower_amount = len(self.tower_group)
            
            self.gui.components["steering_wheel"].update(self.mouse_being_pressed, self.mouse_pos, self.camera_offset)
            
            self.water_tilemap.sinewave_move()
            self.water_tilemap.render(self.screen, self.camera_offset)
            self.ground_tilemap.render(self.screen, self.camera_offset)
            self.path_tilemap.render(self.screen, self.camera_offset)
            
            self.props.render(self.screen, self.camera_offset)
            self.tower_group.update(self.screen, self.camera_offset, self.enemy_group, self)
            self.enemy_group.update(self.screen, self.camera_offset, self.path)
            self.projectile_group.update(self.screen, self.camera_offset)
            
            self.gui.render(self.screen)
            
            pygame.display.update()
            self.clock.tick(60)
            await asyncio.sleep(0)
                                        
asyncio.run(Game().main())
