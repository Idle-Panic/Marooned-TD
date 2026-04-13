import pygame
from Scripts.utilities import load_image

class Wave_Data:
    def __init__(self, main, txtfile):
        self.main = main
        self.wave_amount = 2
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
                    self.ticks_next_spawn = pygame.time.get_ticks() + 1000 * self.wave_pauses[self.wave][0]
                    self.wave_index += 1
            elif self.main.wave < self.wave_amount:
                self.main.wave_started = False
                self.main.wave += 1
                self.wave_index = 0
        elif wave_started and not self.wave_started:
            self.wave_started = True
            self.ticks_next_spawn = pygame.time.get_ticks() + 1000 * self.wave_pauses[self.wave][0]

class Enemy(pygame.sprite.Sprite):
    def __init__(self, data):
        super().__init__()
        self.START_LOCATION = (368, 112)
        self.image = self.get_img(data)
        self.position = list(self.START_LOCATION)
        self.path_index = 1
        
        self.speed = data["speed"]
        self.health = data["health"]
        
    def get_img(self, data):
        return load_image("enemies/" + data["type"] + "/00.png")
        
    def rect(self, pos):
        return self.image.get_rect(center = pos)
        
    def update(self, screen, camera_offset, path):
        self.position[0] -= self.get_sign(self.position[0] - path[self.path_index][0]) * self.speed
        self.position[1] -= self.get_sign(self.position[1] - path[self.path_index][1]) * self.speed
        if (int(self.position[0]), int(self.position[1])) == path[self.path_index]:
            if self.path_index + 1 != len(path):
                self.path_index += 1
        if self.health <= 0:
            self.kill()
        screen.blit(self.image, self.rect((self.position[0] + camera_offset[0], self.position[1] + camera_offset[1])))
        
    def get_sign(self, num):
        return (num > 0) - (num < 0)
