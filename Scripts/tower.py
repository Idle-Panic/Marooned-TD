import pygame
from Scripts.utilities import load_image, load_images
import math

class Tower(pygame.sprite.Sprite):
    def __init__(self, type_dict, pos, main):
        super().__init__()
        self.main = main
        self.type_dict = type_dict
        self.image_lower = load_image("towers/" + type_dict["type"] + "/platform.png")
        self.images_upper = load_images("towers/" + type_dict["type"] + "/upper")
        self.image_upper = self.images_upper[0]
        self.position = pos
        self.rect = self.image_lower.get_rect(center = self.position)
        self.image = load_image("towers/" + type_dict["type"] + "/platform.png")
        self.level = 1
        self.attack = type_dict["attack"][0]
        self.speed = type_dict["speed"][0]
        self.range = type_dict["range"][0]
        self.attack_type = type_dict["attack_type"]
        self.rotation = 180
        self.enemy_attacking_pos = (self.position[0], self.position[1] - 64)
        self.last_time_fired = 0
        self.time_sped_up_last = 0
	
    def update(self, screen, camera_offset, enemy_group, main):
        self.attack = self.type_dict["attack"][self.level-1]
        self.speed = self.type_dict["speed"][self.level-1]
        self.range = self.type_dict["range"][self.level-1]
        time_sped_up = main.time_sped_up
        surface = pygame.Surface((32, 63))
        surface.set_colorkey((0, 0, 0))
        
        if len(enemy_group) != 0:
            for enemy in enemy_group:
                if pygame.math.Vector2(enemy.position).distance_to(pygame.math.Vector2((self.position[0], self.position[1] + 12))) < self.range:
                    self.enemy_attacking_pos = enemy.position
                    if pygame.time.get_ticks() + (time_sped_up - self.time_sped_up_last) >= self.last_time_fired + 1000 * self.speed:
                        main.projectile_group.add(Projectile(self.type_dict, (self.rect.center[0], self.rect.center[1]), enemy, self.main, self.attack))
                        self.last_time_fired = pygame.time.get_ticks()
                        self.time_sped_up_last = time_sped_up
                        if self.type_dict["type"] == "coconut_launcher":
                            self.main.sounds["slingshot"].play()
                        if self.type_dict["type"] == "puckle_gun":
                            self.main.sounds["gunshot"].play()
                    break
        
        self.image_upper = self.images_upper[pygame.math.clamp(int(
        (pygame.time.get_ticks() - self.last_time_fired) / 1000 * self.speed * main.gamespeed * len(self.images_upper)
        ), 0, len(self.images_upper) - 1)]
        self.rotation = math.degrees(math.atan2(self.position[0] - self.enemy_attacking_pos[0], self.position[1] + 12 - self.enemy_attacking_pos[1])) - 180
        rotated_image_upper = pygame.transform.rotate(self.image_upper, self.rotation)
        
        surface.blit(self.image_lower, (0, 31))
        surface.blit(rotated_image_upper, rotated_image_upper.get_rect(center = (16, 35)))
        self.rect = surface.get_rect(center = self.position)
        self.image = surface
        # What are all of these random values in this method? I don't know, but it works!

class Projectile(pygame.sprite.Sprite):
    def __init__(self, type_dict, pos, enemy, main, attack):
        super().__init__()
        self.main = main
        self.position = pygame.math.Vector2(pos)
        self.enemy = enemy
        self.type_dict = type_dict
        self.attack = attack
        self.attack_type = type_dict["attack_type"]
        self.image = load_image("towers/" + type_dict["type"] + "/projectile.png")
        
        self.target_position = pygame.math.Vector2(self.enemy.position)
        self.target_direction = self.target_position - self.position
        self.movement = self.target_direction.normalize()
        
    def rect(self, pos):
        return self.image.get_rect(center = pos)

    def update(self, screen, camera_offset, dt, gamespeed):
        self.position += self.movement * 4 * dt * gamespeed
        if self.position.distance_to(self.target_position) < 4 + gamespeed * 2 - 1:
            if self.attack_type == "normal":
                self.enemy.health -= self.attack
            elif self.attack_type == "area_attack":
                self.main.area_attack_group.add(Area_Attack(self.type_dict, self.position, self.main, self.attack))
                self.main.sounds["explosion"].play()
            self.kill()
        screen.blit(self.image, self.rect((self.position[0] + camera_offset[0], self.position[1] + camera_offset[1])))
        
class Area_Attack(pygame.sprite.Sprite):
    def __init__(self, type_dict, pos, main, attack):
        super().__init__()
        self.main = main
        self.position = pygame.math.Vector2(pos)
        self.attack = attack
        self.images = load_images("towers/" + type_dict["type"] + "/area_attack")
        self.image = self.images[0]
        self.init_time = pygame.time.get_ticks()
        for enemy in self.main.enemy_group:
            if pygame.math.Vector2(enemy.position).distance_to(pygame.math.Vector2((self.position[0], self.position[1]))) < 32:
                enemy.health -= self.attack
                
    def rect(self, pos):
        return self.image.get_rect(center = pos)
        
    def update(self, screen, camera_offset, dt, gamespeed):
        if pygame.time.get_ticks() > self.init_time + 720 / gamespeed:
            self.kill()
        self.image = self.images[pygame.math.clamp(int((pygame.time.get_ticks() - self.init_time) / 720 * gamespeed * len(self.images)), 0, len(self.images) - 1)]
        screen.blit(self.image, self.rect((self.position[0] + camera_offset[0], self.position[1] + camera_offset[1])))
