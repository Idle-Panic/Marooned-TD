import pygame
import asyncio
import sys

from Scripts.level import Tilemap, Props
from Scripts.utilities import load_image, load_images, convert_tilemap, process_font
from Scripts.gui import GUI
from Scripts.tower import Tower

if sys.platform == "emscripten":
    platform.window.canvas.style.imageRendering = "pixelated"

class Game:
    def __init__(self):
        pygame.init()

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
        
        self.ground_tilemap = Tilemap(self, self.tile_size, 15, convert_tilemap("ground_tiles.txt", self.tile_size, 15), "ground_tiles", 0, False)
        self.water_tilemap = Tilemap(self, self.tile_size, 21, convert_tilemap("water_tiles.txt", self.tile_size, 21), "water_tiles", -96, True)
        self.path_tilemap = Tilemap(self, self.tile_size, 15, convert_tilemap("path_tiles.txt", self.tile_size, 15), "path_tiles", 0, False)
        
        self.gui = GUI(self)
        self.props = Props()
        
        self.mouse_pos = (0, 0)
        
        self.tower_group = pygame.sprite.Group()

    async def main(self):
        while True:
            
            self.mouse_being_pressed = False
            for i in pygame.mouse.get_pressed():
                if i == True:
                    self.mouse_being_pressed = True
            if self.mouse_being_pressed:
                self.mouse_pos = pygame.mouse.get_pos()
            
            self.gui.components["buttons"].check_collisions(self.mouse_being_pressed, self.mouse_pos)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.tower_amount = len(self.tower_group)
            
            self.gui.components["steering_wheel"].update(self.mouse_being_pressed, self.mouse_pos, self.camera_offset)
            
            self.water_tilemap.sinewave_move()
            self.water_tilemap.render(self.screen, self.camera_offset)
            self.ground_tilemap.render(self.screen, self.camera_offset)
            self.path_tilemap.render(self.screen, self.camera_offset)
            
            self.props.render(self.screen, self.camera_offset)
            self.tower_group.update(self.screen, self.camera_offset, self.mouse_pos)
            
            self.gui.render(self.screen)
            
            pygame.display.update()
            self.clock.tick(60)
            await asyncio.sleep(0)
                                        
asyncio.run(Game().main())

