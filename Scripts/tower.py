import pygame
from Scripts.utilities import load_image, load_images
import math

class Tower(pygame.sprite.Sprite):
    def __init__(self, type_dict, pos):
        super().__init__()
        self.type_dict = type_dict
        self.image_lower = load_image("towers/" + type_dict["type"] + "/platform.png")
        self.image_upper = load_image("towers/" + type_dict["type"] + "/upper/04.png")
        self.position = pos # 180, 120
        self.rect = self.image_lower.get_rect(center = self.position)
        self.attack = type_dict["attack"]
        self.speed = type_dict["speed"]
        self.range = type_dict["range"]
        self.rotation = 180
        self.enemy_attacking_pos = (self.position[0], self.position[1] - 64)
        self.last_time_fired = 0
	
    def update(self, screen, camera_offset, enemy_group, main):
        if len(enemy_group) != 0:
            for enemy in enemy_group:
                if pygame.math.Vector2(enemy.position).distance_to(pygame.math.Vector2((self.position[0], self.position[1]))) < self.range:
                    self.enemy_attacking_pos = enemy.position
                    if pygame.time.get_ticks() >= self.last_time_fired + 1000 * self.speed:
                        main.projectile_group.add(Projectile(self.type_dict, (self.rect.center[0], self.rect.center[1]), enemy))
                        self.last_time_fired = pygame.time.get_ticks()
                    break
        self.rotation = math.degrees(math.atan2(self.position[0] - self.enemy_attacking_pos[0], self.position[1] - 12 - self.enemy_attacking_pos[1])) - 180
        rotated_image_upper = pygame.transform.rotate(self.image_upper, self.rotation)
        screen.blit(self.image_lower, (self.rect.x + camera_offset[0], self.rect.y + 16 + camera_offset[1]))
        screen.blit(rotated_image_upper, rotated_image_upper.get_rect(center = (self.rect.x  + 16 + camera_offset[0],
        self.rect.y + 16 + camera_offset[1])))

class Projectile(pygame.sprite.Sprite):
    def __init__(self, type_dict, pos, enemy):
        super().__init__()
        self.position = pygame.math.Vector2(pos)
        self.enemy = enemy
        self.attack = type_dict["attack"]
        self.image = load_image("towers/" + type_dict["type"] + "/projectile.png").convert_alpha()
        
        self.target_position = pygame.math.Vector2(self.enemy.position)
        self.target_direction = self.target_position - self.position
        self.movement = self.target_direction.normalize()
        
    def rect(self, pos):
        return self.image.get_rect(center = pos)

    def update(self, screen, camera_offset):
        self.position += self.movement * 4
        if self.position.distance_to(self.target_position) < 2:
            self.enemy.health -= self.attack
            self.kill()
        screen.blit(self.image, self.rect((self.position[0] + camera_offset[0], self.position[1] + camera_offset[1])))
