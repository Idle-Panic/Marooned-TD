import pygame
import os

BASE_IMG_PATH = "Images/"
BASE_AUDIO_PATH = "Audio/"

pygame.init()

font1 = pygame.font.Font("Font/fs-marianne.ttf", 32)
font2 = pygame.font.Font("Font/fs-marianne.ttf", 16)

def load_image(path):
    image = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    return image

def load_images(path):
    images = []
    for image_name in os.listdir(BASE_IMG_PATH + path):
        images.append(load_image(path + "/" + image_name))
    return images

def load_audio(path, type):
	if type == "music":
		return(pygame.mixer.music.load(BASE_AUDIO_PATH + path))
	else:
		return(pygame.mixer.Sound(BASE_AUDIO_PATH + path))

def convert_tilemap(file, tile_size, tile_diameter):
    tile_data = {}
    text_file = open(file, encoding="utf8")
    for y in range(tile_diameter):
        line = text_file.readline().strip("\n")
        line = line.split(",")
        for x in range(tile_diameter):
            tile = line[x]
            tile_data[str(x+1) + ";" + str(y+1)] = {"position": (x*tile_size, y*tile_size), "type": tile}
    text_file.close()
    return tile_data

def process_font(text, color, position, screen):
    font = font2
    if (text == "Stats" or text == "Build") and color != (123, 123, 123):
        font = font1
    text_rendered = font.render(text, False, color)
    text_rect = text_rendered.get_rect(midtop = (position))
    screen.blit(text_rendered, text_rect)
    
class SortedGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        
    def draw(self, surface, camera_offset, bgd=None, special_flags=0):
        sprites = sorted(self.sprites(), key = lambda spr: spr.rect.midbottom[1])
        if hasattr(surface, "blits"):
            self.spritedict.update(
                zip(
                    sprites,
                    surface.blits(
                        (spr.image, (spr.rect.x + camera_offset[0], spr.rect.y + camera_offset[1]), None, special_flags) for spr in sprites
                    ),
                )
            )
        else:
            for spr in sprites:
                self.spritedict[spr] = surface.blit(
                    spr.image, spr.rect, None, special_flags
                )
        self.lostsprites = []
        dirty = self.lostsprites

        return dirty
