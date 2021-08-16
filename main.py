import pygame
import sys
from random import randint
from pygame.locals import *

pygame.init()

pygame.display.set_caption('Тень Чести')

clock = pygame.time.Clock()
# info = pygame.display.Info()
# screen_width, screen_height = info.current_w, info.current_h
# window_width, window_height = screen_width - 10, screen_height - 50
# window = pygame.display.set_mode((window_width,window_height))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


class GameCharacter:
    def __init__(self, coords, ch_type):
        if ch_type == "ninja":
            self.sprite = pygame.image.load('source/MC_r_r.png').convert()
            self.katana = Armour(10, .6)
            self.knife = Armour(20, None)
        elif ch_type == "purple_ninja":
            self.sprite = pygame.image.load('source/menu/purple_ninja.png').convert()
        elif ch_type == "green_ninja":
            self.sprite = pygame.image.load('source/menu/green_ninja.png').convert()
        elif ch_type == "skeleton_knife":
            self.sprite = pygame.image.load('source/...').convert()
        elif ch_type == "skeleton_spear":
            self.sprite = pygame.image.load('source/...').convert()
        self.rect = pygame.Rect(coords[0], coords[1], self.sprite.get_width(), self.sprite.get_height())
        self.speed = 10

    def set_speed(self, speed):
        self.speed = speed

    # def move(self, direction):


class Armour:
    def __init__(self, damage, cd):
        self.damage = damage
        self.cd = cd

    def hit(self):
        pass


def start():
    # display = pygame.Surface((600, 400))
    # background, game_objects, game_characters = draw_level(0)
    # update(background, game_objects, game_characters, display)
    main_menu()


def main_menu():
    display = pygame.Surface((600, 400))
    background = pygame.image.load('source/menu/background.jpg').convert()
    display.blit(background, (0, 0))
    positions = [
        (103, 379),
        (424, 176),
        (498, 379),
    ]
    pos = randint(0, 2)
    purple_ninja = GameCharacter(positions[pos], "purple_ninja")
    green_ninja = GameCharacter(positions[pos - 1], "green_ninja")
    del pos
    button_start_image = pygame.image.load('source/menu/startbtn.jpg').convert()
    button_start = pygame.Rect(247, 135, button_start_image.get_width(), button_start_image.get_height())
    button_load_image = pygame.image.load('source/menu/loadbtn.jpg').convert()
    button_load = pygame.Rect(382, 214, button_load_image.get_width(), button_load_image.get_height())
    button_settings_image = pygame.image.load('source/menu/settingsbtn.jpg').convert()
    button_settings = pygame.Rect(247, 146, button_settings_image.get_width(), button_settings_image.get_height())
    button_exit_image = pygame.image.load('source/menu/exitbtn.jpg').convert()
    button_exit = pygame.Rect(247, 146, button_exit_image.get_width(), button_exit_image.get_height())
    chain_image = pygame.image.load('source/menu/chain.jpg').convert()
    chain = pygame.Rect(247, 146, chain_image.get_width(), chain_image.get_height())
    chain_down_image = pygame.image.load('source/menu/chaindown.jpg').convert()
    chain_down = pygame.Rect(247, 146, chain_down_image.get_width(), chain_down_image.get_height())
    images = [button_start_image, button_load_image, button_settings_image, button_exit_image, chain_image,
              chain_down_image, purple_ninja.sprite, green_ninja.sprite]
    objects = [button_start, button_load, button_settings, button_exit, chain, chain_down, purple_ninja, green_ninja]
    for image, obj in zip(images, objects):
        display.blit(image, obj)
    pygame.display.update()
    clock.tick(60)


def update(background, game_objects, game_characters, display):
    running = True
    display.blit(background, (0, 0))
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        pygame.display.update()
        clock.tick(60)


def draw_level(level):
    if level == 0:
        background = pygame.image.load('source/menu/background.jpg').convert()  # 600x400
        # button_start, button_load, button_settings, button_exit, chain, chain_down, ninja1, ninja2
        game_objects = [
            pygame.image.load('source/menu/startbtn.jpg').convert(),
            pygame.image.load('source/menu/loadbtn.jpg').convert(),
            pygame.image.load('source/menu/settingsbtn.jpg').convert(),
            pygame.image.load('source/menu/exitbtn.jpg').convert(),
            pygame.image.load('source/menu/chain.jpg').convert(),
            pygame.image.load('source/menu/chaindown.jpg').convert()
        ]
        game_characters = [
            GameCharacter((100, 100), "purple_ninja"),
            GameCharacter((100, 100), "green_ninja"),
        ]
    else:
        background = pygame.image.load('source/lvl' + str(level) + '/background.jpg').convert()
        game_objects = []
        game_characters = []
        # for image in folder (if consist ninja or skeleton — character, else — simple game object. But mb'll change)
    return background, game_objects, game_characters


if __name__ == '__main__':
    start()
    pygame.quit()
    sys.exit()
