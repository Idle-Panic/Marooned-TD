import pygame
from Scripts.utilities import load_image, process_font, load_audio, swap_img_colors
from Scripts.tower import Tower

class GUI:
    def __init__(self, main):
        self.main = main
        self.gui_mode = "stats"
        self.background_pos = ()
        self.background_width = 150
        self.viewing_tower = 0
        self.hovering_over_upgrade = False
        self.hidden = False
        self.move_information_text_exists = True
        self.images = {
        "title_background" : load_image("gui/title_background.png"),
        "title" : load_image("gui/title.png"),
        "driftwood_icon" : load_image("gui/driftwood_icon.png"),
        "doubloon" : load_image("gui/doubloon.png"),
        "wave" : load_image("gui/wave.png"),
        "health" : load_image("gui/health.png"),
        "towers_icon" : load_image("gui/towers_icon.png"),
        "panel_icon1" : load_image("gui/panel_icon1.png"),
        "panel_icon2" : load_image("gui/panel_icon2.png"),
        "panel_icon3" : load_image("gui/panel_icon3.png"),
        "sabre_button_up_left" : load_image("gui/sabre_button_up.png"),
        "sabre_button_up_right" : pygame.transform.flip(load_image("gui/sabre_button_up.png"), True, False),
        "sabre_button_down_left" : load_image("gui/sabre_button_down.png"),
        "sabre_button_down_right" : pygame.transform.flip(load_image("gui/sabre_button_down.png"), True, False),
        "build_button_up" : load_image("gui/build_button_up.png"),
        "build_button_down" : load_image("gui/build_button_down.png"),
        "coconut_launcher_blueprint_green" : load_image("towers/coconut_launcher/blueprint_green.png"),
        "coconut_launcher_blueprint_red" : load_image("towers/coconut_launcher/blueprint_red.png"),
        "cannon_blueprint_green" : load_image("towers/cannon/blueprint_green.png"),
        "cannon_blueprint_red" : load_image("towers/cannon/blueprint_red.png"),
        "startwave_button_up" : load_image("gui/startwave_button_up.png"),
        "startwave_button_down" : load_image("gui/startwave_button_down.png"),
        "startwave_button_gray" : load_image("gui/startwave_button_gray.png"),
        "compass_button_up_right" : load_image("gui/compass_button_up.png"),
        "compass_button_down_right" : load_image("gui/compass_button_down.png"),
        "compass_button_up_left" : pygame.transform.flip(load_image("gui/compass_button_up.png"), True, False),
        "compass_button_down_left" : pygame.transform.flip(load_image("gui/compass_button_down.png"), True, False),
        "doubloon_icon" : load_image("gui/doubloon_icon.png"),
        "attack_icon" : load_image("gui/attack_icon.png"),
        "range_icon" : load_image("gui/range_icon.png"),
        "speed_icon" : load_image("gui/speed_icon.png"),
        "title_start_button_up" : load_image("gui/title_start_button_up.png"),
        "title_start_button_down" : load_image("gui/title_start_button_down.png"),
        "hp_icon" : load_image("gui/hp_icon.png"),
        "empty_32x32" : pygame.Surface((32, 64)),
        "gamespeed_button_1x_up" : load_image("gui/gamespeed_button_1x_up.png"),
        "gamespeed_button_2x_up" : load_image("gui/gamespeed_button_2x_up.png"),
        "gamespeed_button_3x_up" : load_image("gui/gamespeed_button_3x_up.png"),
        "gamespeed_button_1x_down" : load_image("gui/gamespeed_button_1x_down.png"),
        "gamespeed_button_2x_down" : load_image("gui/gamespeed_button_2x_down.png"),
        "gamespeed_button_3x_down" : load_image("gui/gamespeed_button_3x_down.png"),
        "entity_background" : load_image("gui/entity_background.png"),
        "entity_background2" : load_image("gui/entity_background2.png"),
        "blue_panel" : load_image("gui/blue_panel.png"),
        "upgrade_button_up" : load_image("gui/upgrade_button_up.png"),
        "upgrade_button_down" : load_image("gui/upgrade_button_down.png"),
        "sell_button_up" : load_image("gui/sell_button_up.png"),
        "sell_button_down" : load_image("gui/sell_button_down.png"),
        "puckle_gun_blueprint_green" : load_image("towers/puckle_gun/blueprint_green.png"),
        "puckle_gun_blueprint_red" : load_image("towers/puckle_gun/blueprint_red.png"),
        "arrow_button_up_right" : load_image("gui/arrow_button_up.png"),
        "arrow_button_down_right" : load_image("gui/arrow_button_down.png"),
        "arrow_button_up_left" : pygame.transform.flip(load_image("gui/arrow_button_up.png"), True, False),
        "arrow_button_down_left" : pygame.transform.flip(load_image("gui/arrow_button_down.png"), True, False),
        }
        self.components = {"background" : Background(), "buttons" : Buttons(self), "blueprints": Blueprints(self), "icons" : Icons(self), "texts" : Texts(self),
        "steering_wheel" : Steering_Wheel(self)}
        
        self.buttons_when_hidden = [self.components["buttons"].buttons[3], self.components["buttons"].buttons[13]]
        self.tower_displaying = False
        self.enemy_displaying = False
        
        self.components["icons"].icons[25]["image"].set_colorkey((0, 0, 0))
        self.components["icons"].icons[26]["image"].set_colorkey((0, 0, 0))
    
    def render(self, screen, camera_offset):
        if self.tower_displaying and self.gui_mode == "viewing_tower":
            pygame.draw.circle(screen, (140, 214, 18), (self.tower_displaying.rect.center[0] + camera_offset[0], self.tower_displaying.rect.center[1] + 12 + camera_offset[1]),
            self.tower_displaying.range, 2)
        
        if self.main.state == "title":
            screen.blit(self.images["title_background"], (0, 0 - pygame.mouse.get_pos()[1]**0.7))
            screen.blit(self.images["title"], (0, 0))
            
        elif self.main.state == "playing":
            if self.hidden:
                for button in self.buttons_when_hidden:
                    if button["image_up"] == self.images["startwave_button_up"] and self.main.wave_started == True:
                        screen.blit(self.images["startwave_button_gray"], button["rect"])
                    elif button["being_pressed"] == False:
                        screen.blit(button["image_up"], button["rect"])
                    else:
                        screen.blit(button["image_down"], button["rect"])
                screen.blit(self.components["steering_wheel"].rotated_image, 
                self.components["steering_wheel"].rotated_image.get_rect(center = self.components["steering_wheel"].position))
                return None
            if self.gui_mode == "build":
                self.components["blueprints"].update(self.main.camera_offset)
                if self.components["blueprints"].valid == True:
                    screen.blit(self.components["blueprints"].blueprints[self.viewing_tower]["image_green"], self.components["blueprints"].rect)
                    pygame.draw.circle(screen, (140, 214, 18), (self.components["blueprints"].rect.centerx, self.components["blueprints"].rect.centery + 2),
                    self.main.tower_stats[self.viewing_tower]["range"][0], 2)
                else:
                    screen.blit(self.components["blueprints"].blueprints[self.viewing_tower]["image_red"], self.components["blueprints"].rect)
                    pygame.draw.circle(screen, (224, 60, 40), (self.components["blueprints"].rect.centerx, self.components["blueprints"].rect.centery + 2), 
                    self.main.tower_stats[self.viewing_tower]["range"][0], 2)
            
            screen.blit(self.components["background"].image, self.components["background"].position)
            
            self.components["icons"].icons[25]["image"].fill((0, 0, 0))
            self.components["icons"].icons[26]["image"].fill((0, 0, 0))
            
            if self.tower_displaying:
                self.components["icons"].icons[25]["image"].blit(self.tower_displaying.image, (0, -16))
            if self.enemy_displaying:
                self.components["icons"].icons[26]["image"].blit(self.enemy_displaying.image, (0, 0))
            
            for icon in self.components["icons"].icons:
                if not icon["mode"] or icon["mode"] == self.gui_mode:
                    screen.blit(icon["image"], icon["rect"])
                elif type(icon["mode"]) == list:
                    for mode in icon["mode"]:
                        if mode == self.gui_mode:
                            screen.blit(icon["image"], icon["rect"])
                    
            self.components["texts"].update()
            for text in self.components["texts"].texts:
                if text["mode"] == self.gui_mode:
                    if text["color"] == self.main.colors["dark_brown"]:
                        process_font(text["text"], text["color"], text["position"], self.main.screen)
                elif type(text["mode"]) == list:
                    for mode in text["mode"]:
                        if mode == self.gui_mode and text["color"] != (123, 123, 123):
                            process_font(text["text"], text["color"], text["position"], self.main.screen)
                elif not text["mode"]:
                    process_font(text["text"], text["color"], text["position"], self.main.screen)
                    
        for button in self.components["buttons"].buttons:
            if button in self.components["buttons"].valid_buttons:
                if button["image_up"] == self.images["startwave_button_up"] and self.main.wave_started == True:
                    screen.blit(self.images["startwave_button_gray"], button["rect"])
                elif button["being_pressed"] == False:
                    screen.blit(button["image_up"], button["rect"])
                else:
                    screen.blit(button["image_down"], button["rect"])
            
        if self.main.state == "playing":
            for text in self.components["texts"].texts:
                if text["mode"] == self.gui_mode:
                    if "upgrade" in text["text"]:
                        if self.tower_displaying.level != 3:
                            surface1 = pygame.Surface((84, 20))
                            surface1.set_colorkey((0, 0, 0))
                            process_font(text["text"], text["color"], (40, 0), surface1)
                            surface1.scroll(int(pygame.time.get_ticks() / 90 * -1), 0, pygame.SCROLL_REPEAT)
                            surface2 = pygame.Surface((60, 20))
                            surface2.set_colorkey((0, 0, 0))
                            surface2.blit(surface1, (0, 0))
                            screen.blit(surface2, surface2.get_rect(midtop = text["position"]))
                        else:
                            process_font("Max", text["color"], text["position"], self.main.screen)
                        continue
                    if text["color"] != self.main.colors["dark_brown"]:
                        process_font(text["text"], text["color"], text["position"], self.main.screen)
                elif type(text["mode"]) == list:
                    for mode in text["mode"]:
                        if mode == self.gui_mode and text["color"] == (123, 123, 123):
                            process_font(text["text"], text["color"], text["position"], self.main.screen)
            screen.blit(self.components["steering_wheel"].rotated_image, 
            self.components["steering_wheel"].rotated_image.get_rect(center = self.components["steering_wheel"].position))
        
class Background:
    def __init__(self):
        self.image = load_image("gui/background.png")
        self.position = (210, 0)
        GUI.background_pos = self.position
        
class Blueprints:
    def __init__(self, gui):
        self.gui = gui
        self.image = self.gui.images["coconut_launcher" + "_blueprint_green"]
        self.position = (360 / 2, 240 / 2 - 14)
        self.blueprints = [
        dict(zip(["image_red", "image_green", "rect"], self.get_blueprint_dict("coconut_launcher"))),
        dict(zip(["image_red", "image_green", "rect"], self.get_blueprint_dict("cannon"))),
        dict(zip(["image_red", "image_green", "rect"], self.get_blueprint_dict("puckle_gun"))),
        ]
        self.rect = self.blueprints[0]["rect"]
        self.collision_rect = pygame.Rect(self.position[0] - 16, self.position[1] + 14, 32, 32)
        self.mask = pygame.mask.Mask(size=(32, 32))
        self.mask.fill()
        self.valid = False
        
    def get_blueprint_dict(self, tower):
        img_green = self.gui.images[tower + "_blueprint_green"]
        img_red = self.gui.images[tower + "_blueprint_red"]
        return(img_red, img_green, img_green.get_rect(midtop = self.position))
        
    def update(self, camera_offset):
        colliding_with_path = True
        colliding_with_tower = True
        colliding_with_props = True
        colliding_with_water = True
        
        if self.gui.main.path_mask.overlap_area(self.mask, (self.position[0] - 16 - camera_offset[0], self.position[1] + 15 - camera_offset[1])) == 0:
            colliding_with_path = False
        if len(self.gui.main.tower_group) > 0:
            if not self.check_tower_collision(camera_offset):
                colliding_with_tower = False
        else:
             colliding_with_tower = False
            
        for prop_name in self.gui.main.prop_rects:
            if prop_name == "cave":
                if self.gui.main.prop_rects[prop_name][0].colliderect(self.collision_rect.move((- camera_offset[0], - camera_offset[1]))):
                    break
            if prop_name == "camp":
                if self.gui.main.prop_rects[prop_name][0].colliderect(self.collision_rect.move((- camera_offset[0], - camera_offset[1]))):
                    break
            if prop_name == "palm":
                if not self.check_palm_collision(camera_offset):
                    colliding_with_props = False
                    
        if self.is_on_land(camera_offset):
            colliding_with_water = False
                
        if not colliding_with_path  and not colliding_with_tower and not colliding_with_props and not colliding_with_water:
            self.valid = True
        else:
            self.valid = False
            
    def check_tower_collision(self, camera_offset):
        for tower in self.gui.main.tower_group:
            if tower.image_lower.get_rect(center = tower.position).move((0, 16)).colliderect(self.collision_rect.move((- camera_offset[0], - camera_offset[1]))):
                return True
        return False
    
    def check_palm_collision(self, camera_offset):
        for palm_rect in self.gui.main.prop_rects["palm"]:
            if pygame.Vector2((palm_rect.midbottom[0] + camera_offset[0], palm_rect.midbottom[1] + camera_offset[1] - 8))\
            .distance_to(pygame.Vector2(self.collision_rect.center)) < 22:
                return True
        return False
        
    def is_on_land(self, camera_offset):
        blueprint_center = (self.position[0], self.position[1] + 30)
        blueprint_tile_location = str(int((blueprint_center[0] - camera_offset[0]) / 32 + 1)) + ";" + str(int((blueprint_center[1] - camera_offset[1]) / 32 + 1))
        if blueprint_tile_location in self.gui.main.ground_tilemap.tile_data:
            if self.gui.main.ground_tilemap.tile_data[blueprint_tile_location]["type"] == "4":
                return True
        return False
    
class Buttons:
    def __init__(self, gui):
        self.gui = gui
        self.buttons = [
        dict(zip(["image_up", "image_down", "rect", "mode", "being_pressed"], self.get_button_rect("sabre_button_up_right", (360-self.gui.background_width+100, 37), "stats"))),
        dict(zip(["image_up", "image_down", "rect", "mode", "being_pressed"], self.get_button_rect("sabre_button_up_left", (360-self.gui.background_width+36, 1),
        ["build", "viewing_tower", "viewing_enemy"]))),
        dict(zip(["image_up", "image_down", "rect", "mode", "being_pressed"], self.get_button_rect("build_button_up", (360-self.gui.background_width+75, 142), "build"))),
        dict(zip(["image_up", "image_down", "rect", "mode", "being_pressed"], self.get_button_rect("startwave_button_up", (26, 2), False))),
        dict(zip(["image_up", "image_down", "rect", "mode", "being_pressed"], self.get_button_rect("compass_button_up_right", (360-self.gui.background_width/2+40, 144), "build"))),
        dict(zip(["image_up", "image_down", "rect", "mode", "being_pressed"], self.get_button_rect("compass_button_up_left", (360-self.gui.background_width/2-40, 144), "build"))),
        dict(zip(["image_up", "image_down", "rect", "mode", "being_pressed"], self.get_button_rect("title_start_button_up", (180, 136), "title"))),
        dict(zip(["image_up", "image_down", "rect", "mode", "being_pressed"], self.get_button_rect("gamespeed_button_1x_up", (360-self.gui.background_width/2-40, 204), False))),
        dict(zip(["image_up", "image_down", "rect", "mode", "being_pressed"], self.get_button_rect("gamespeed_button_2x_up", (360-self.gui.background_width/2-2, 204), False))),
        dict(zip(["image_up", "image_down", "rect", "mode", "being_pressed"], self.get_button_rect("gamespeed_button_3x_up", (360-self.gui.background_width/2+40, 204), False))),
        dict(zip(["image_up", "image_down", "rect", "mode", "being_pressed"], self.get_button_rect("upgrade_button_up", (360-self.gui.background_width/2-34, 172), "viewing_tower"))),
        dict(zip(["image_up", "image_down", "rect", "mode", "being_pressed"], self.get_button_rect("sell_button_up", (360-self.gui.background_width/2+34, 172), "viewing_tower"))),
        dict(zip(["image_up", "image_down", "rect", "mode", "being_pressed"], self.get_button_rect("arrow_button_up_right", (360-self.gui.background_width-18, 0), False))),
        dict(zip(["image_up", "image_down", "rect", "mode", "being_pressed"], self.get_button_rect("arrow_button_up_left", (360-self.gui.background_width-18, 0), False))),
        ]
        self.valid_buttons = []
        
    def get_button_rect(self, img, pos, mode):
        img_up = self.gui.images[img]
        img_down = self.gui.images[img.replace("_up", "_down")]
        return(img_up, img_down, img_up.get_rect(midtop = pos), mode, False)
        
    def check_collisions(self, mouse_being_pressed, mouse_pos):
        self.valid_buttons = []
        for button in self.buttons:
            if not self.gui.hidden and button["image_up"] == self.gui.images["arrow_button_up_left"]:
                continue
            if self.gui.hidden and button["image_up"] == self.gui.images["arrow_button_up_right"]:
                continue
            if button["mode"] == self.gui.gui_mode or (not button["mode"] and self.gui.main.state == "playing") or button["mode"] == self.gui.main.state:
                self.valid_buttons.append(button)
            elif type(button["mode"]) == list:
                for mode in button["mode"]:
                    if mode == self.gui.gui_mode or mode == self.gui.main.state:
                        self.valid_buttons.append(button)
                        break
                        
        for button in self.valid_buttons:
            if button["image_up"] == self.gui.images["upgrade_button_up"] and button["rect"].collidepoint(pygame.mouse.get_pos()):
                self.gui.hovering_over_upgrade = True
            elif button["image_up"] == self.gui.images["upgrade_button_up"] and not button["rect"].collidepoint(pygame.mouse.get_pos()):
                self.gui.hovering_over_upgrade = False
            if mouse_being_pressed:
                if button["rect"].collidepoint(mouse_pos):
                    button["being_pressed"] = True
                else:
                    button["being_pressed"] = False
            else:
                if button["rect"].collidepoint(mouse_pos):
                    if button["being_pressed"] == True:
                        button["being_pressed"] = False
                        if button["image_up"] != self.gui.images["startwave_button_up"]:
                            if not self.gui.hidden or button["image_up"] == self.gui.images["arrow_button_up_left"]:
                                self.gui.main.sounds["click"].play()
                        else:
                            self.gui.main.sounds["sword"].play()
                        if button["image_up"] == self.gui.images["startwave_button_up"]:
                            if not self.gui.main.wave_started:
                                self.gui.main.wave_started = True
                                self.gui.main.coins += int(((self.gui.main.wave - 1) * 10)**0.7)
                        if button["image_up"] == self.gui.images["arrow_button_up_left"]:
                            self.gui.hidden = False
                        if button["image_up"] == self.gui.images["arrow_button_up_right"]:
                            self.gui.hidden = True
                        if self.gui.hidden:
                            return None
                        if button["image_up"] == self.gui.images["sabre_button_up_right"]:
                            self.gui.gui_mode = "build"
                        if button["image_up"] == self.gui.images["sabre_button_up_left"]:
                            self.gui.gui_mode = "stats"
                        if button["image_up"] == self.gui.images["gamespeed_button_1x_up"]:
                            self.gui.main.gamespeed = 1
                        if button["image_up"] == self.gui.images["gamespeed_button_2x_up"]:
                            self.gui.main.gamespeed = 2
                        if button["image_up"] == self.gui.images["gamespeed_button_3x_up"]:
                            self.gui.main.gamespeed = 3
                        if button["image_up"] == self.gui.images["upgrade_button_up"]:
                            tower = self.gui.tower_displaying
                            if tower.level < 3 and self.gui.main.coins >= tower.type_dict["price"][tower.level]:
                                self.gui.main.coins -= tower.type_dict["price"][tower.level]
                                tower.level += 1
                                if self.gui.tower_displaying.level == 2:
                                    tower.images_upper = swap_img_colors(tower.images_upper, [(255, 130, 206), (224, 60, 40), (135, 22, 70)], 
                                    [(255, 231, 55), (255, 187, 49), (204, 143, 21)])
                                    tower.image_lower = swap_img_colors(tower.image_lower, [(255, 130, 206), (224, 60, 40), (135, 22, 70)], 
                                    [(255, 231, 55), (255, 187, 49), (204, 143, 21)])
                                else:
                                    tower.images_upper = swap_img_colors(tower.images_upper, [(255, 231, 55), (255, 187, 49), (204, 143, 21)], 
                                    [(91, 168, 255), (10, 137, 255), (2, 74, 202)])
                                    tower.image_lower = swap_img_colors(tower.image_lower, [(255, 231, 55), (255, 187, 49), (204, 143, 21)], 
                                    [(91, 168, 255), (10, 137, 255), (2, 74, 202)])
                        if button["image_up"] == self.gui.images["sell_button_up"]:
                            if self.gui.tower_displaying:
                                self.gui.main.coins += round(self.gui.tower_displaying.type_dict["price"][0]*(2/3))
                                self.gui.tower_displaying.kill()
                                self.gui.tower_displaying = None
                                self.gui.gui_mode = "stats"
                        if button["image_up"] == self.gui.images["build_button_up"]:
                            if self.gui.components["blueprints"].valid == True:
                                self.gui.main.add_tower(self.gui.viewing_tower, (360 / 2 - self.gui.main.camera_offset[0], 240 / 2 - self.gui.main.camera_offset[1]))
                        if button["image_up"] == self.gui.images["title_start_button_up"]:
                            self.gui.main.state = "playing"
                            load_audio("main_theme.ogg", "music")
                            pygame.mixer.music.play(-1, 0.0, 8000)
                            pygame.mixer.music.set_volume(0.5)
                                
                        if button["image_up"] == self.gui.images["compass_button_up_right"] and self.gui.gui_mode == "build":
                            self.gui.viewing_tower = pygame.math.clamp(self.gui.viewing_tower + 1, 0, len(self.gui.main.tower_stats) - 1)
                        if button["image_up"] == self.gui.images["compass_button_up_left"] and self.gui.gui_mode == "build":
                            self.gui.viewing_tower = pygame.math.clamp(self.gui.viewing_tower - 1, 0, len(self.gui.main.tower_stats) - 1)
                else:
                    button["being_pressed"] = False

class Icons:
    def __init__(self, gui):
        self.gui = gui
        self.icons = [
        dict(zip(["image", "rect", "mode"], self.get_icon_rect("driftwood_icon", (360-self.gui.background_width/2, 8), False))),
        dict(zip(["image", "rect", "mode"], self.get_icon_rect("doubloon", (360-self.gui.background_width+20, 64), "stats"))),
        dict(zip(["image", "rect", "mode"], self.get_icon_rect("wave", (360-self.gui.background_width+20, 96), "stats"))),
        dict(zip(["image", "rect", "mode"], self.get_icon_rect("health", (360-self.gui.background_width+20, 128), "stats"))),
        dict(zip(["image", "rect", "mode"], self.get_icon_rect("towers_icon", (360-self.gui.background_width+20, 160), "stats"))),
        dict(zip(["image", "rect", "mode"], self.get_icon_rect("panel_icon1", (360-self.gui.background_width+84, 62), "stats"))),
        dict(zip(["image", "rect", "mode"], self.get_icon_rect("panel_icon1", (360-self.gui.background_width+84, 94), "stats"))),
        dict(zip(["image", "rect", "mode"], self.get_icon_rect("panel_icon1", (360-self.gui.background_width+84, 126), "stats"))),
        dict(zip(["image", "rect", "mode"], self.get_icon_rect("panel_icon1", (360-self.gui.background_width+84, 158), "stats"))),
        dict(zip(["image", "rect", "mode"], self.get_icon_rect("panel_icon2", (360-self.gui.background_width/2, 56), ["build", "viewing_tower", "viewing_enemy"]))),
        dict(zip(["image", "rect", "mode"], self.get_icon_rect("panel_icon3", (360-self.gui.background_width/2-34, 86), ["build", "viewing_tower", "viewing_enemy"]))),
        dict(zip(["image", "rect", "mode"], self.get_icon_rect("panel_icon3", (360-self.gui.background_width/2+34, 86), "build"))),
        dict(zip(["image", "rect", "mode"], self.get_icon_rect("panel_icon3", (360-self.gui.background_width/2-34, 116), ["build", "viewing_tower", "viewing_enemy"]))),
        dict(zip(["image", "rect", "mode"], self.get_icon_rect("panel_icon3", (360-self.gui.background_width/2+34, 116), "build"))),
        dict(zip(["image", "rect", "mode"], self.get_icon_rect("doubloon_icon", (360-self.gui.background_width/2-52, 89), "build"))),
        dict(zip(["image", "rect", "mode"], self.get_icon_rect("attack_icon", (360-self.gui.background_width/2+16, 89), "build"))),
        dict(zip(["image", "rect", "mode"], self.get_icon_rect("range_icon", (360-self.gui.background_width/2-52, 119), ["build", "viewing_tower"]))),
        dict(zip(["image", "rect", "mode"], self.get_icon_rect("speed_icon", (360-self.gui.background_width/2+16, 119), "build"))),
        dict(zip(["image", "rect", "mode"], self.get_icon_rect("panel_icon3", (360-self.gui.background_width/2-34, 146), "viewing_tower"))),
        dict(zip(["image", "rect", "mode"], self.get_icon_rect("attack_icon", (360-self.gui.background_width/2-52, 89), "viewing_tower"))),
        dict(zip(["image", "rect", "mode"], self.get_icon_rect("speed_icon", (360-self.gui.background_width/2-52, 149), "viewing_tower"))),
        dict(zip(["image", "rect", "mode"], self.get_icon_rect("hp_icon", (360-self.gui.background_width/2-52, 89), "viewing_enemy"))),
        dict(zip(["image", "rect", "mode"], self.get_icon_rect("speed_icon", (360-self.gui.background_width/2-52, 119), "viewing_enemy"))),
        dict(zip(["image", "rect", "mode"], self.get_icon_rect("entity_background", (360-self.gui.background_width/2+32, 96), "viewing_enemy"))),
        dict(zip(["image", "rect", "mode"], self.get_icon_rect("entity_background2", (360-self.gui.background_width/2+32, 96), "viewing_tower"))),
        dict(zip(["image", "rect", "mode"], self.get_icon_rect("empty_32x32", (360-self.gui.background_width/2+32, 100), "viewing_tower"))),
        dict(zip(["image", "rect", "mode"], self.get_icon_rect("empty_32x32", (360-self.gui.background_width/2+32, 100), "viewing_enemy"))),
        dict(zip(["image", "rect", "mode"], self.get_icon_rect("blue_panel", (360-self.gui.background_width/2+32, 76), "viewing_tower"))),
        ]
        
    def get_icon_rect(self, img, pos, mode):
        img = self.gui.images[img]
        return(img, img.get_rect(midtop = pos), mode)

class Texts:
    def __init__(self, gui):
        self.gui = gui
        self.coins = 80
        self.wave = 1
        self.health = 100
        self.towers = 0
        self.texts = [
        {"text" : "Stats", "color" : self.gui.main.colors["dark_brown"], "position" : (360-self.gui.background_width/2, 14), "mode" : "stats"},
        {"text" : f"Coins : {self.coins}", "color" : self.gui.main.colors["dark_brown"], "position" : (360-self.gui.background_width/2+8, 67), "mode" : "stats"},
        {"text" : f"Wave : {self.wave}", "color" : self.gui.main.colors["dark_brown"], "position" : (360-self.gui.background_width/2+8, 99), "mode" : "stats"},
        {"text" : f"HP : {self.health}", "color" : self.gui.main.colors["dark_brown"], "position" : (360-self.gui.background_width/2+8, 132), "mode" : "stats"},
        {"text" : f"Towers : {self.towers}", "color" : self.gui.main.colors["dark_brown"], "position" : (360-self.gui.background_width/2+8, 163), "mode" : "stats"},
        {"text" : "Build", "color" : self.gui.main.colors["gray"], "position" : (360-self.gui.background_width+118, 44), "mode" : "stats"},
        {"text" : "Stats", "color" : self.gui.main.colors["gray"], "position" : (360-self.gui.background_width+16, 7), "mode" : ["build", "viewing_tower", "viewing_enemy"]},
        {"text" : "Build", "color" : self.gui.main.colors["dark_brown"], "position" : (360-self.gui.background_width/2, 14), "mode" : "build"},
        {"text" : "coconut launcher", "color" : self.gui.main.colors["dark_brown"], "position" : (360-self.gui.background_width/2, 58), "mode" : "build"},
        {"text" : "100", "color" : self.gui.main.colors["red"], "position" : (360-self.gui.background_width/2-18, 89), "mode" : "build"},
        {"text" : "0", "color" : self.gui.main.colors["dark_brown"], "position" : (360-self.gui.background_width/2+46, 89), "mode" : "build"},
        {"text" : "0", "color" : self.gui.main.colors["dark_brown"], "position" : (360-self.gui.background_width/2-18, 119), "mode" : "build"},
        {"text" : "0", "color" : self.gui.main.colors["dark_brown"], "position" : (360-self.gui.background_width/2+46, 119), "mode" : "build"},
        {"text" : "Tower", "color" : self.gui.main.colors["dark_brown"], "position" : (360-self.gui.background_width/2, 14), "mode" : "viewing_tower"},
        {"text" : "Enemy", "color" : self.gui.main.colors["dark_brown"], "position" : (360-self.gui.background_width/2, 14), "mode" : "viewing_enemy"},
        {"text" : "coconut launcher", "color" : self.gui.main.colors["dark_brown"], "position" : (360-self.gui.background_width/2, 58), "mode" : "viewing_tower"},
        {"text" : "0", "color" : self.gui.main.colors["dark_brown"], "position" : (360-self.gui.background_width/2-18, 89), "mode" : "viewing_tower"},
        {"text" : "0", "color" : self.gui.main.colors["dark_brown"], "position" : (360-self.gui.background_width/2-18, 119), "mode" : "viewing_tower"},
        {"text" : "0", "color" : self.gui.main.colors["dark_brown"], "position" : (360-self.gui.background_width/2-18, 149), "mode" : "viewing_tower"},
        {"text" : "crab", "color" : self.gui.main.colors["dark_brown"], "position" : (360-self.gui.background_width/2, 58), "mode" : "viewing_enemy"},
        {"text" : "0", "color" : self.gui.main.colors["dark_brown"], "position" : (360-self.gui.background_width/2-24, 89), "mode" : "viewing_enemy"},
        {"text" : "0", "color" : self.gui.main.colors["dark_brown"], "position" : (360-self.gui.background_width/2-24, 119), "mode" : "viewing_enemy"},
        {"text" : "Level 1", "color" : self.gui.main.colors["light_blue"], "position" : (360-self.gui.background_width/2+32, 78), "mode" : "viewing_tower"},
        {"text" : "Level 1", "color" : self.gui.main.colors["dark_blue"], "position" : (360-self.gui.background_width/2+31, 78), "mode" : "viewing_tower"},
        {"text" : "upgrade", "color" : self.gui.main.colors["light_blue"], "position" : (360-self.gui.background_width/2-34, 176), "mode" : "viewing_tower"},
        {"text" : "sell(20c)", "color" : self.gui.main.colors["yellow"], "position" : (360-self.gui.background_width/2+34, 176), "mode" : "viewing_tower"},
        {"text" : "Move by dragging \nthe steering wheel \nor pressing any \narrow keys!", "color" : self.gui.main.colors["black"], 
        "position" : (72, 164), "mode" : False},
        ]
        
    def update(self):
        self.texts[8]["text"] = self.gui.main.tower_stats[self.gui.viewing_tower]["type"].replace("_", " ")
        self.texts[9]["text"] = str(self.gui.main.tower_stats[self.gui.viewing_tower]["price"][0])
        self.texts[10]["text"] = str(self.gui.main.tower_stats[self.gui.viewing_tower]["attack"][0])
        self.texts[11]["text"] = str(self.gui.main.tower_stats[self.gui.viewing_tower]["range"][0])
        self.texts[12]["text"] = str(self.gui.main.tower_stats[self.gui.viewing_tower]["speed"][0])
        if self.gui.tower_displaying:
            self.texts[15]["text"] = self.gui.tower_displaying.type_dict["type"].replace("_", " ")
            if not self.gui.hovering_over_upgrade or self.gui.tower_displaying.level == 3:
                self.texts[16]["text"] = str(self.gui.tower_displaying.attack)
                self.texts[17]["text"] = str(self.gui.tower_displaying.range)
                self.texts[18]["text"] = str(self.gui.tower_displaying.speed)
            else:
                self.texts[16]["text"] = str(self.gui.tower_displaying.type_dict["attack"][self.gui.tower_displaying.level])
                self.texts[17]["text"] = str(self.gui.tower_displaying.type_dict["range"][self.gui.tower_displaying.level])
                self.texts[18]["text"] = str(self.gui.tower_displaying.type_dict["speed"][self.gui.tower_displaying.level])
            self.texts[22]["text"] = f"Level {self.gui.tower_displaying.level}"
            self.texts[23]["text"] = f"Level {self.gui.tower_displaying.level}"
            if self.gui.tower_displaying.level != 3:
                self.texts[24]["text"] = "upgrade(" + str(round(self.gui.tower_displaying.type_dict["price"][self.gui.tower_displaying.level])) + ")"
            self.texts[25]["text"] = "sell(" + str(round(self.gui.tower_displaying.type_dict["price"][0]*(2/3))) + ")"
        if self.gui.enemy_displaying:
            self.texts[19]["text"] = self.gui.enemy_displaying.type.replace("_", " ")
            self.texts[20]["text"] = str(self.gui.enemy_displaying.health) + "/" + str(self.gui.enemy_displaying.max_health)
            self.texts[21]["text"] = str(self.gui.enemy_displaying.speed)
        
        self.coins = self.gui.main.coins
        self.wave = self.gui.main.wave
        self.health = self.gui.main.health
        self.towers = self.gui.main.tower_amount
        if self.gui.main.tower_stats[self.gui.viewing_tower]["price"][0] > self.coins:
            self.texts[9]["color"] = self.gui.main.colors["red"]
        else:
            self.texts[9]["color"] = self.gui.main.colors["green"]
        self.texts[1]["text"] = f"Coins : {self.coins}"
        self.texts[2]["text"] = f"Wave : {self.wave}"
        self.texts[3]["text"] = f"HP : {self.health}"
        self.texts[4]["text"] = f"Towers : {self.towers}"

class Steering_Wheel:
    def __init__(self, gui):
        self.gui = gui
        self.image = load_image("gui/steering_wheel.png")
        self.norm_pos = (180, 196)
        self.position = self.norm_pos
        self.rect = self.image.get_rect(center = self.position)
        self.offset = [0, 0]
        self.being_held = False
        self.rotation = 0
        self.rotated_image = self.image
        
    def update(self, mouse_being_pressed, mouse_pos, camera_offset, dt, keyboard_movement):
        offset = (mouse_pos[0] - self.norm_pos[0], mouse_pos[1] - self.norm_pos[1])
        if keyboard_movement != [0, 0]:
            offset = (keyboard_movement[0] * 65, keyboard_movement[1] * 35)
        distance = (offset[0]**2 + offset[1]**2)**0.5
        factor = 1 / (1 + distance * 0.01)
        if (mouse_being_pressed == True and (self.rect.collidepoint(mouse_pos) or self.being_held)) or keyboard_movement != [0, 0]:
            if (offset[0] > 20 or offset[1] > 20) and self.gui.move_information_text_exists:
                self.gui.move_information_text_exists = False
                self.gui.components["texts"].texts.pop(26)
            self.being_held = True
            self.position = (self.norm_pos[0] + offset[0] * factor, self.norm_pos[1] + offset[1] * factor)
            self.move_camera(offset, distance, factor, camera_offset, dt)
            self.rotation -= offset[0] / 32 * dt
        else:
            self.position = self.norm_pos
            self.being_held = False
            self.rotation = 0
            
        self.rotated_image = pygame.transform.rotate(self.image, self.rotation)
        
    def move_camera(self, offset, distance, factor, camera_offset, dt):
        try:
            self.gui.main.camera_offset[0] -= offset[0] / distance / factor * 2 * dt
        except:
            pass
        try:
            self.gui.main.camera_offset[1] -= offset[1] / distance / factor * 2 * dt
        except:
            pass
