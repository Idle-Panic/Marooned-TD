import pygame
from Scripts.utilities import load_image, load_images

class Wave_Data:
    def __init__(self, main, txtfile):
        self.main = main
        self.wave_amount = 6
        self.wave_enemies = []
        self.wave_pauses = []
        self.wave_started = False
        self.wave = 1
        self.wave_index = 0
        open_txtfile = open(txtfile, encoding="utf8")
        for ln in range(self.wave_amount):
            self.wave_enemies.append([])
            self.wave_pauses.append([])
            line = open_txtfile.readline().strip("\n")
            line = line.split(";")
            for i in line:
                i = i.split(",")
                self.wave_enemies[ln].append(i[0])
                self.wave_pauses[ln].append(float(i[1]))
        open_txtfile.close()
        
        self.ticks_last_spawned = 0
        self.ticks_next_spawn = 0
        
    def check_and_add(self, wave, wave_started):
        self.wave = wave - 1
        self.wave_started = wave_started
        if wave_started and self.wave_started:
            if self.wave_index != len(self.wave_enemies[self.wave]):
                if pygame.time.get_ticks() >= self.ticks_next_spawn:
                    self.main.add_enemy(self.wave_enemies[self.wave][self.wave_index])
                    self.ticks_next_spawn = pygame.time.get_ticks() + 1000 * self.wave_pauses[self.wave][self.wave_index]
                    self.wave_index += 1
            elif self.main.wave < self.wave_amount:
                self.main.wave_started = False
                self.main.wave += 1
                self.wave_index = 0
        elif wave_started and not self.wave_started:
            self.wave_started = True
            self.ticks_next_spawn = pygame.time.get_ticks() + 1000 * self.wave_pauses[self.wave][0]

class Enemy(pygame.sprite.Sprite):
    def __init__(self, data, main):
        super().__init__()
        self.START_LOCATION = (368, 112)
        self.images = self.get_imgs(data)
        self.image = self.images[0]
        self.position = list(self.START_LOCATION)
        self.path_index = 1
        self.rect = self.image.get_rect()
        
        self.speed = data["speed"]
        self.max_health = data["health"]
        self.health = data["health"]
        self.init_time = pygame.time.get_ticks()
        self.distance_travelled = 0
        
        self.healthbar = Healthbar()
        main.render_group.add(self.healthbar)
        
    def get_imgs(self, data):
        return load_images("enemies/" + data["type"])

    def update(self, screen, camera_offset, path, main, dt):
        distance = (self.get_sign(self.position[0] - path[self.path_index][0])**2 + self.get_sign(self.position[1] - path[self.path_index][1])**2)**0.5
        if distance != 0:
            self.position[0] -= self.get_sign(self.position[0] - path[self.path_index][0]) / distance * self.speed * dt
            self.position[1] -= self.get_sign(self.position[1] - path[self.path_index][1]) / distance * self.speed * dt
        elif main.health > 0:
            self.kill()
            self.healthbar.kill()
            main.health -= self.health
        else:
            pass
        if (round(self.position[0]), round(self.position[1])) == path[self.path_index]:
            self.position = [path[self.path_index][0], path[self.path_index][1]]
            if self.path_index + 1 != len(path):
                self.path_index += 1
        if self.health <= 0:
            self.kill()
            self.healthbar.kill()
            main.coins += int(self.max_health / 2)
        self.image = self.images[int((pygame.time.get_ticks() - self.init_time) / 200 * self.speed) % len(self.images)]
        self.rect = self.image.get_rect(center = self.position)
        
        self.distance_travelled = (pygame.time.get_ticks() - self.init_time) * self.speed
        
        self.healthbar.update(self.health, self.max_health, self.position, main)
        
    def get_sign(self, num):
        if num > 0:
            return 1
        elif num < 0:
            return -1
        return 0
        
class Healthbar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((32, 36))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(midtop = (368, 112 - 20))
        
    def update(self, health, max_health, pos, main):
        self.rect.centerx = int(pos[0])
        self.rect.centery = int(pos[1]) - 2
        pygame.draw.line(self.image, main.colors["dark_blue"], (0, 1), (32, 1), 4)
        pygame.draw.line(self.image, main.colors["red"], (1, 1), (30, 1), 2)
        pygame.draw.line(self.image, main.colors["green"], (1, 1), (health / max_health * 29 + 1 , 1), 2)
