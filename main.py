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
            self.sprite = pygame.image.load('source/menu/purple_ninja.png')
        elif ch_type == "green_ninja":
            self.sprite = pygame.image.load('source/menu/green_ninja.png')
        elif ch_type == "skeleton_knife":
            self.sprite = pygame.image.load('source/...').convert()
        elif ch_type == "skeleton_spear":
            self.sprite = pygame.image.load('source/...').convert()
        self.rect = pygame.Rect(coords[0], coords[1], self.sprite.get_width(), self.sprite.get_height())
        self.speed = [1, 4]     # [walk speed, run speed]

    def set_speed(self, speed):
        self.speed = speed

    def move(self, direction, mode=0):
        self.rect.x += direction * self.speed[mode]


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
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h
    width = int(((screen_width + screen_height) / 2 + abs(screen_width - screen_height) / 2))
    k = width / 600
    if screen_width < screen_height:
        k = width / 400
    width = 600 * k
    height = 400 * k
    win_size = (int(600 * k), int(400 * k))
    display = pygame.Surface((600, 400))

    dif_x = int((screen_width - width) / 2)
    dif_y = int((screen_height - height) / 2)

    background = pygame.image.load('source/menu/background.jpg')
    light_background = pygame.image.load('source/menu/light_background.jpg')
    display.blit(background, (0, 0))
    positions = [
        (103, 321),
        (424, 118),
        (486, 321),
    ]
    pos = randint(0, 2)
    purple_ninja = GameCharacter(positions[pos], "purple_ninja")
    green_ninja = GameCharacter(positions[pos - 1], "green_ninja")
    del pos, screen_width, screen_height
    ############################################################################
    button_start_image = pygame.image.load('source/menu/startbtn.png')
    button_start = pygame.Rect(247, 100, button_start_image.get_width(), button_start_image.get_height())
    button_load_image = pygame.image.load('source/menu/loadbtn.png')
    button_load = pygame.Rect(382, 177, button_load_image.get_width(), button_load_image.get_height())
    button_settings_image = pygame.image.load('source/menu/settingsbtn.png')
    button_settings = pygame.Rect(113, 228, button_settings_image.get_width(), button_settings_image.get_height())
    button_exit_image = pygame.image.load('source/menu/exitbtn.png')
    button_exit = pygame.Rect(256, 338, button_exit_image.get_width(), button_exit_image.get_height())
    chain_image = pygame.image.load('source/menu/chain.png')
    chain = pygame.Rect(343, 136, chain_image.get_width(), chain_image.get_height())
    chain_down_image = pygame.image.load('source/menu/chaindown.png')
    chain_down = pygame.Rect(333, 137, chain_down_image.get_width(), chain_down_image.get_height())
    images = [button_start_image, button_load_image, button_settings_image, button_exit_image, chain_image,
              chain_down_image]
    objects = [button_start, button_load, button_settings, button_exit, chain, chain_down]
    moving = 0
    running = True
    while running:
        display.blit(background, (0, 0))
        for image, obj in zip(images, objects):
            display.blit(image, obj)
        display.blit(purple_ninja.sprite, purple_ninja.rect)
        display.blit(green_ninja.sprite, green_ninja.rect)
        green_ninja.move(moving)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == K_RIGHT:
                    moving = 1
                if event.key == K_LEFT:
                    moving = -1
            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    moving = 0
                if event.key == K_LEFT:
                    moving = 0
        surf = pygame.transform.scale(display, win_size)
        screen.blit(surf, (dif_x, dif_y))
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
