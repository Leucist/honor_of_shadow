import pygame
import sys
import json
from random import randint
from pygame.locals import *

pygame.init()

pygame.display.set_caption('Тень Чести')
pygame.mixer.pre_init(44100, -16, 2, 512)

clock = pygame.time.Clock()
# info = pygame.display.Info()
# screen_width, screen_height = info.current_w, info.current_h
# window_width, window_height = screen_width - 10, screen_height - 50
# window = pygame.display.set_mode((window_width,window_height))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
global display_width


class GameCharacter:
    def __init__(self, coords, ch_type):
        self.animation_database = {}
        self.animation_frames = {}
        self.hit_list = []
        self.mode = 'idle'
        self.anim_frame = 0
        self.moving = [0, 0]
        self.flip = False
        self.name = ch_type
        self.sprite = pygame.image.load('source/animations/' + self.name + '/idle/idle_0.png').convert_alpha()
        with open("character_settings.json", "r", encoding="UTF-8") as settings_file:
            data = json.loads(settings_file.read())
            self.hp = data[self.name][0]
            self.weapon_damage = data[self.name][1]
            self.weapon_cd = data[self.name][2]  # weapon cool down
            self.speed = data[self.name][3]  # [walk speed, run speed]
            self.speed['idle'] = 0
            animset = data[self.name][4]
            for mode in animset:
                self.load_animation(mode, animset[mode])
        self.rect = pygame.Rect(coords[0], coords[1], self.sprite.get_width(), self.sprite.get_height())

    def move(self, collidable_objects):
        self.rect.x += self.moving[0] * self.speed[self.mode]
        self.check_collision(collidable_objects)
        if self.rect.x <= 0:
            self.rect.x = 0
            self.mode = 'idle'
        right_border = display_width - self.sprite.get_width()
        if self.rect.x >= right_border:
            self.rect.x = right_border
            self.mode = 'idle'
        for obj in self.hit_list:
            if self.moving[0] > 0:
                self.rect.right = obj.left
                self.mode = 'idle'
            elif self.moving[0] < 0:
                self.rect.left = obj.right
                self.mode = 'idle'
        self.rect.y += self.moving[1] * self.speed[self.mode]
        self.check_collision(collidable_objects)
        for obj in self.hit_list:
            if self.moving[1] > 0:
                self.rect.bottom = obj.top
                self.mode = 'idle'
            elif self.moving[1] < 0:
                self.rect.top = obj.bottom
                self.mode = 'idle'
            # self.speed[1] = 0


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

    def change_frame(self):
        if self.anim_frame >= len(self.animation_database[self.mode]):
            self.anim_frame = 0
        self.sprite = self.animation_frames[self.animation_database[self.mode][self.anim_frame]]

    def check_collision(self, collidable_objects):
        self.hit_list = []
        for obj in collidable_objects:
            # if obj == self.rect:
            #     continue
            if self.rect.colliderect(obj):
                self.hit_list.append(obj)


def start():
    # display = pygame.Surface((600, 400))
    # background, game_objects, game_characters = draw_level(0)
    # update(background, game_objects, game_characters, display)
    main_menu()


def main_menu():
    global display_width
    display_width = 600
    with open("settings.json", "r", encoding="UTF-8") as settings_file:
        settings = json.loads(settings_file.read())
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

    background = pygame.image.load('source/menu/background.jpg').convert()
    light_background = pygame.image.load('source/menu/light_background.jpg').convert()
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
    game_objects = [button_start, button_load, button_settings, button_exit, chain, chain_down]
    collidable_objects = [button_start, button_load, button_settings, button_exit]
    collidable_objects.append(pygame.Rect(0, 379, 600, 1))      # floor
    collidable_objects.append(pygame.Rect(220, 337, 165, 43))   # stairs
    characters = [purple_ninja, green_ninja]
    LIGHT_DISTANCE = [50, 50, 50, 51, 51, 51, 49, 49, 49] * 4
    green_ninja.anim_frame = 0
    purple_ninja.anim_frame = 0
    running = True

    pygame.mixer.music.load("source/audio/menu_backgound_music.wav")
    pygame.mixer.music.set_volume(settings['volume']['background_music'])
    pygame.mixer.music.play(-1)

    while running:
        display.blit(background, (0, 0))

        light = []
        # Probably gonna remake it in order it will be easier to treat torches as single objects
        purple_torch = [purple_ninja.rect.x + 6 + 44 * purple_ninja.flip, purple_ninja.rect.y + 12]
        green_torch = [green_ninja.rect.x + 6 + 44 * green_ninja.flip, green_ninja.rect.y + 12]
        for i in range(-LIGHT_DISTANCE[purple_ninja.anim_frame], LIGHT_DISTANCE[purple_ninja.anim_frame] + 1):
            x_ch = ((LIGHT_DISTANCE[purple_ninja.anim_frame] - i) * (
                    LIGHT_DISTANCE[purple_ninja.anim_frame] + i)) ** 0.5
            w_ch = x_ch * 2
            light.append(pygame.Rect(purple_torch[0] - x_ch, purple_torch[1] + i,
                                     w_ch, 1))
            light.append(pygame.Rect(green_torch[0] - x_ch, green_torch[1] + i,
                                     w_ch, 1))
            # FOR OPTIMISATION SHOULD USE INCREASING THE HEIGHT OF THE RECT AND ADDING "i += n"
        for rect in light:
            display.blit(light_background, rect, rect)

        for image, obj in zip(images, game_objects):
            display.blit(image, obj)

        for character in characters:
            if character.moving[0] != 0:
                character.move(collidable_objects)
            character.change_frame()
            character.anim_frame += 1
            display.blit(pygame.transform.flip(character.sprite, character.flip, False), character.rect)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == K_RIGHT:
                    green_ninja.flip = False
                    green_ninja.moving[0] = 1
                    green_ninja.anim_frame = 0
                    green_ninja.mode = 'walk'
                if event.key == K_LEFT:
                    green_ninja.flip = True
                    green_ninja.moving[0] = -1
                    green_ninja.anim_frame = 0
                    green_ninja.mode = 'walk'
            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    green_ninja.moving[0] = 0
                    green_ninja.anim_frame = 0
                    green_ninja.mode = 'idle'
                if event.key == K_LEFT:
                    green_ninja.moving[0] = 0
                    green_ninja.anim_frame = 0
                    green_ninja.mode = 'idle'
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
