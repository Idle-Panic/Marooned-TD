import pygame
from Scripts.utilities import load_image, load_images
import math

class Tower(pygame.sprite.Sprite):
    def __init__(self, img_path, pos):
        super().__init__()
        self.image_lower = load_image("towers/" + img_path + "/platform.png")
        self.image_upper = load_image("towers/" + img_path + "/upper/04.png")
        self.position = pos
        self.rect = self.image_lower.get_rect(center = self.position)
        self.rotation = 180
	
    def update(self, screen, camera_offset, mouse_pos):
        self.rotation = math.degrees(math.atan2(self.position[0] - mouse_pos[0] + camera_offset[0], self.position[1] - mouse_pos[1] + camera_offset[1])) - 180
        rotated_image_upper = pygame.transform.rotate(self.image_upper, self.rotation)
        screen.blit(self.image_lower, (self.position[0] + camera_offset[0], self.position[1] + camera_offset[1]))
        screen.blit(rotated_image_upper, rotated_image_upper.get_rect(center = (self.position[0] + self.image_upper.width / 2 + camera_offset[0],
        self.position[1] + self.image_upper.width / 2 + camera_offset[1] - 12)))
