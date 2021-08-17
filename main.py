import pygame
import sys
import json
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
global anim_frame


class GameCharacter:
    def __init__(self, coords, ch_type):
        self.animation_database = {}
        self.animation_frames = {}
        self.name = ch_type
        self.sprite = pygame.image.load('source/animations/' + self.name + '/idle/idle_0.png').convert_alpha()
        with open("character_settings.json", "r", encoding="UTF-8") as settings_file:
            data = json.loads(settings_file.read())
            self.hp = data[self.name][0]
            self.weapon_damage = data[self.name][1]
            self.weapon_cd = data[self.name][2]  # weapon cool down
            self.speed = data[self.name][3]  # [walk speed, run speed]
            animset = data[self.name][4]
            for mode in animset:
                self.load_animation(mode, animset[mode])
        self.rect = pygame.Rect(coords[0], coords[1], self.sprite.get_width(), self.sprite.get_height())

    def move(self, direction, mode=0):
        self.rect.x += direction * self.speed[mode]

    def load_animation(self, mode, frame_durations):
        animation_frame_data = []
        n = 0
        for frame in frame_durations:
            animation_frame_id = mode + '_' + str(n)
            img_loc = 'source/animations/' + self.name + '/' + mode + '/' + animation_frame_id + '.png'
            # animations/ninja/idle/idle_0.png
            animation_image = pygame.image.load(img_loc).convert_alpha()
            self.animation_frames[animation_frame_id] = animation_image.copy()
            for i in range(frame):
                animation_frame_data.append(animation_frame_id)
            n += 1
        self.animation_database[mode] = animation_frame_data

    def change_frame(self, mode):
        global anim_frame
        if anim_frame >= len(self.animation_database[mode]):
            anim_frame = 0
        self.sprite = self.animation_frames[self.animation_database[mode][anim_frame]]


def change_mode(mode, new_mode):
    if mode != new_mode:
        global anim_frame
        anim_frame = 0
    return mode


def start():
    # display = pygame.Surface((600, 400))
    # background, game_objects, game_characters = draw_level(0)
    # update(background, game_objects, game_characters, display)
    main_menu()


def main_menu():
    global anim_frame
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
    button_start_image = pygame.image.load('source/menu/startbtn.png').convert_alpha()
    button_start = pygame.Rect(247, 100, button_start_image.get_width(), button_start_image.get_height())
    button_load_image = pygame.image.load('source/menu/loadbtn.png').convert_alpha()
    button_load = pygame.Rect(382, 177, button_load_image.get_width(), button_load_image.get_height())
    button_settings_image = pygame.image.load('source/menu/settingsbtn.png').convert_alpha()
    button_settings = pygame.Rect(113, 228, button_settings_image.get_width(), button_settings_image.get_height())
    button_exit_image = pygame.image.load('source/menu/exitbtn.png').convert_alpha()
    button_exit = pygame.Rect(256, 338, button_exit_image.get_width(), button_exit_image.get_height())
    chain_image = pygame.image.load('source/menu/chain.png').convert_alpha()
    chain = pygame.Rect(343, 136, chain_image.get_width(), chain_image.get_height())
    chain_down_image = pygame.image.load('source/menu/chaindown.png').convert_alpha()
    chain_down = pygame.Rect(333, 137, chain_down_image.get_width(), chain_down_image.get_height())
    images = [button_start_image, button_load_image, button_settings_image, button_exit_image, chain_image,
              chain_down_image]
    objects = [button_start, button_load, button_settings, button_exit, chain, chain_down]
    moving, anim_frame = 0, 0
    mode = 'idle'
    running = True
    while running:
        display.blit(background, (0, 0))
        for image, obj in zip(images, objects):
            display.blit(image, obj)
        if moving != 0:
            # change_mode(mode, 'walk')
            # green_ninja.change_frame('walk')
            green_ninja.move(moving)
        green_ninja.change_frame(mode)
        anim_frame += 1

        display.blit(purple_ninja.sprite, purple_ninja.rect)
        display.blit(green_ninja.sprite, green_ninja.rect)

        # light = []
        # # Probably gonna remake it in order it will be easier to treat torches as single objects
        # purple_torch = [purple_ninja.rect.x + 3, purple_ninja.rect.y + 12]
        # green_torch = [green_ninja.rect.x + 3, green_ninja.rect.y + 12]
        # LIGHT_DISTANCE = 100
        # for i in range(LIGHT_DISTANCE):
        #     light.append(pygame.Rect(purple_torch[0] - LIGHT_DISTANCE / 2 - i, purple_torch[1] - LIGHT_DISTANCE / 2 + i,
        #                              LIGHT_DISTANCE + i, 1))
        #     # light.append(pygame.Rect(green_torch[0] - LIGHT_DISTANCE / 2 - i, green_torch[1] - LIGHT_DISTANCE / 2 + i,
        #     #                          LIGHT_DISTANCE + i, 1))
        # for rect in light:
        #     display.blit(light_background, rect)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == K_RIGHT:
                    moving = 1
                    anim_frame = 0
                    mode = 'walk'
                if event.key == K_LEFT:
                    moving = -1
                    anim_frame = 0
                    mode = 'walk'
            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    moving = 0
                    anim_frame = 0
                    mode = 'idle'
                if event.key == K_LEFT:
                    moving = 0
                    anim_frame = 0
                    mode = 'idle'
        surf = pygame.transform.scale(display, win_size)
        screen.blit(surf, (dif_x, dif_y))
        pygame.display.update()
        clock.tick(60)


# def load_animation(path,frame_durations):
#     global animation_frames
#     animation_name = path.split('/')[-1]
#     animation_frame_data = []
#     n = 0
#     for frame in frame_durations:
#         animation_frame_id = animation_name + '_' + str(n)
#         img_loc = path + '/' + animation_frame_id + '.png'
#         # player_animations/idle/idle_0.png
#         animation_image = pygame.image.load(img_loc).convert()
#         animation_image.set_colorkey((255,255,255))
#         animation_frames[animation_frame_id] = animation_image.copy()
#         for i in range(frame):
#             animation_frame_data.append(animation_frame_id)
#         n += 1
#     return animation_frame_data


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
