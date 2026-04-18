import pygame
from Scripts.utilities import load_image, process_font
from Scripts.tower import Tower

class GUI:
	def __init__(self, main):
		self.main = main
		self.gui_mode = "stats"
		self.background_pos = ()
		self.background_width = 150
		self.showing_blueprint = False
		self.viewing_tower = 0
		self.images = {
		"driftwood_icon" : load_image("gui/driftwood_icon.png"),
		"doubloon" : load_image("gui/doubloon.png"),
		"wave" : load_image("gui/wave.png"),
		"health" : load_image("gui/health.png"),
		"towers_icon" : load_image("gui/towers_icon.png"),
		"panel_icon1" : load_image("gui/panel_icon1.png"),
		"sabre_button_up_left" : load_image("gui/sabre_button_up.png"),
		"sabre_button_up_right" : pygame.transform.flip(load_image("gui/sabre_button_up.png"), True, False),
		"sabre_button_down_left" : load_image("gui/sabre_button_down.png"),
		"sabre_button_down_right" : pygame.transform.flip(load_image("gui/sabre_button_down.png"), True, False),
		"build_button_up" : load_image("gui/build_button_up.png"),
		"build_button_down" : load_image("gui/build_button_down.png"),
		"coconut_launcher_blueprint_green" : load_image("towers/coconut_launcher/blueprint_green.png"),
		"startwave_button_up" : load_image("gui/startwave_button_up.png"),
		"startwave_button_down" : load_image("gui/startwave_button_down.png"),
		}
		self.blueprints = {
		}
		self.components = {"background" : Background(), "buttons" : Buttons(self), "icons" : Icons(self), "texts" : Texts(self), "steering_wheel" : Steering_Wheel(self)}
	
	def render(self, screen):
		screen.blit(self.components["background"].image, self.components["background"].position)
		for icon in self.components["icons"].icons:
			if not icon["mode"] or icon["mode"] == self.gui_mode:
				if icon["rect"].midtop == (360 / 2, 240 / 2 - 14) and self.showing_blueprint:   # position -> midtop location of blueprints
					screen.blit(icon["image"], icon["rect"])
				elif icon["rect"].midtop != (360 / 2, 240 / 2 - 14):
					screen.blit(icon["image"], icon["rect"])
		
		self.components["texts"].update()
		for text in self.components["texts"].texts:
			if text["mode"] == self.gui_mode:
				if text["color"] != (123, 123, 123):
					process_font(text["text"], text["color"], text["position"], self.main.screen)	
					
		for button in self.components["buttons"].buttons:
			if not button["mode"] or button["mode"] == self.gui_mode:
				if button["being_pressed"] == False:
					screen.blit(button["image_up"], button["rect"])
				else:
					screen.blit(button["image_down"], button["rect"])
					
		for text in self.components["texts"].texts:
			if text["mode"] == self.gui_mode:
				if text["color"] == (123, 123, 123):
					process_font(text["text"], text["color"], text["position"], self.main.screen)	
		screen.blit(self.components["steering_wheel"].rotated_image, 
		self.components["steering_wheel"].rotated_image.get_rect(center = self.components["steering_wheel"].position))

class Background:
	def __init__(self):
		self.image = load_image("gui/background.png")
		self.position = (210, 0)
		GUI.background_pos = self.position
	
class Buttons:
	def __init__(self, gui):
		self.gui = gui
		self.buttons = [
		dict(zip(["image_up", "image_down", "rect", "mode", "being_pressed"], self.get_button_rect("sabre_button_up_right", (360-self.gui.background_width+100, 37), "stats"))),
		dict(zip(["image_up", "image_down", "rect", "mode", "being_pressed"], self.get_button_rect("sabre_button_up_left", (360-self.gui.background_width+36, 1), "build"))),
		dict(zip(["image_up", "image_down", "rect", "mode", "being_pressed"], self.get_button_rect("build_button_up", (360-self.gui.background_width+75, 56), "build"))),
		dict(zip(["image_up", "image_down", "rect", "mode", "being_pressed"], self.get_button_rect("startwave_button_up", (26, 2), False))),
		]
		
	def get_button_rect(self, img, pos, mode):
		img_up = self.gui.images[img]
		img_down = self.gui.images[img.replace("_up", "_down")]
		return(img_up, img_down, img_up.get_rect(midtop = pos), mode, False)
		
	def check_collisions(self, mouse_being_pressed, mouse_pos):
		for button in self.buttons:
			if mouse_being_pressed:
				if button["rect"].collidepoint(mouse_pos):
					button["being_pressed"] = True
				else:
					button["being_pressed"] = False
			else:
				if button["rect"].collidepoint(mouse_pos):
					if button["being_pressed"] == True:
						button["being_pressed"] = False
						if button["image_up"] == self.gui.images["sabre_button_up_right"]:
							self.gui.gui_mode = "build"
						if button["image_up"] == self.gui.images["sabre_button_up_left"] and button["mode"] == "build":
							self.gui.gui_mode = "stats"
						if button["image_up"] == self.gui.images["startwave_button_up"] and button["mode"] == False:
							self.gui.main.wave_started = True
						if button["image_up"] == self.gui.images["build_button_up"] and self.gui.gui_mode == "build":
							if self.gui.showing_blueprint == False:
								self.gui.showing_blueprint = True
							else:
								self.gui.main.add_tower("coconut_launcher", (360 / 2 - self.gui.main.camera_offset[0], 240 / 2 - self.gui.main.camera_offset[1]))
								self.gui.showing_blueprint = False
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
		dict(zip(["image", "rect", "mode"], self.get_icon_rect("coconut_launcher_blueprint_green", (360 / 2, 240 / 2 - 14), "build"))),
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
		{"text" : "Stats", "color" : self.gui.main.colors["gray"], "position" : (360-self.gui.background_width+16, 7), "mode" : "build"},
		{"text" : "Build", "color" : self.gui.main.colors["dark_brown"], "position" : (360-self.gui.background_width/2, 14), "mode" : "build"},
		]
		
	def update(self):
		self.coins = self.gui.main.coins
		self.wave = self.gui.main.wave
		self.health = self.gui.main.health
		self.towers = self.gui.main.tower_amount
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
		
	def update(self, mouse_being_pressed, mouse_pos, camera_offset):
		offset = (mouse_pos[0] - self.norm_pos[0], mouse_pos[1] - self.norm_pos[1])
		distance = (offset[0]**2 + offset[1]**2)**0.5
		factor = 1 / (1 + distance * 0.01)
		if mouse_being_pressed == True and (self.rect.collidepoint(mouse_pos) or self.being_held):
			self.being_held = True
			self.position = (self.norm_pos[0] + offset[0] * factor, self.norm_pos[1] + offset[1] * factor)
			self.move_camera(offset, distance, factor, camera_offset)
			self.rotation -= offset[0] / 32
		else:
			self.position = self.norm_pos
			self.being_held = False
			self.rotation = 0
			
		self.rotated_image = pygame.transform.rotate(self.image, self.rotation)
		
	def move_camera(self, offset, distance, factor, camera_offset):
		try:
			self.gui.main.camera_offset[0] -= offset[0] / distance / factor * 2
		except:
			pass
		try:
			self.gui.main.camera_offset[1] -= offset[1] / distance / factor * 2
		except:
			pass
