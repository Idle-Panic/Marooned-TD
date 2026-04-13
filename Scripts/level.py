import pygame
from Scripts.utilities import load_image
import math

class Tilemap:
    def __init__(self, main, tile_size, tile_diameter, tile_data, tile_layer, native_offset, camera_independence):
        self.main = main
        self.tile_size = tile_size
        self.tile_diameter = tile_diameter
        self.tile_data = tile_data
        self.tile_layer = tile_layer
        self.native_offset = native_offset
        self.extra_offset = [0, 0]
        self.surface = pygame.surface.Surface((720+64, 480+64))
        self.surface.set_colorkey((0, 0, 0))
        self.camera_independence = camera_independence
        for y in range(self.tile_diameter):
            for x in range(self.tile_diameter):
                self.surface.blit(self.main.assets[self.tile_layer][int(self.tile_data[str(x+1) + ";" + str(y+1)]["type"])],
                (self.tile_data[str(x+1) + ";" + str(y+1)]["position"][0] + self.native_offset,
                self.tile_data[str(x+1) + ";" + str(y+1)]["position"][1] + self.native_offset))
        
    def sinewave_move(self):
        self.extra_offset[0] = math.sin(pygame.time.get_ticks() / 2000) * self.tile_size
        self.extra_offset[1] = pygame.time.get_ticks() / 2000 * self.tile_size % 64
    
    def render(self, screen, camera_offset):
        if self.camera_independence == False:
            screen.blit(self.surface, (self.native_offset + self.extra_offset[0] + camera_offset[0], self.native_offset + self.extra_offset[1] + camera_offset[1]))
        else:
            screen.blit(self.surface, (self.native_offset + self.extra_offset[0] + (camera_offset[0] % self.tile_size),
            self.native_offset + self.extra_offset[1] + (camera_offset[1] % self.tile_size)))

class Props:
    def __init__(self):
        self.images = {
        "cave" : load_image("props/cave.png"),
        "palm" : load_image("props/palm.png")
        }
        
        self.rects = {
        "cave" : (self.img_to_rect("cave", (368, 128)), ),
        "palm" : (self.img_to_rect("palm", (160, 124)), self.img_to_rect("palm", (284, 94)), self.img_to_rect("palm", (414, 160)), self.img_to_rect("palm", (388, 278)),
        self.img_to_rect("palm", (254, 394)), self.img_to_rect("palm", (64, 320)),),
        }
        
    def img_to_rect(self, image, pos):
        rect = self.images[image].get_rect(midbottom = pos)
        return rect
        
    def render(self, screen, camera_offset):
        for img in self.images:
            for rect in self.rects:
                if img == rect:
                    for p in self.rects.get(rect):
                        screen.blit(self.images[img], (p[0] + camera_offset[0], p[1] + camera_offset[1]))
