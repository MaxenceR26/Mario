import random

import pygame

pygame.init()


class Player(pygame.sprite.Sprite):
    def __init__(self, x: object, y: object):
        super().__init__()
        self.sprite_sheet = pygame.image.load('players.png')
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.images = {
            'RIGHT-0': self.get_image(0, 64),
            'RIGHT-1': self.get_image(32, 64),
            'RIGHT-2': self.get_image(64, 64),
            'RIGHT-3': self.get_image(96, 64),
            'LEFT-0': self.get_image(0, 32),
            'LEFT-1': self.get_image(32, 32),
            'LEFT-2': self.get_image(64, 32),
            'LEFT-3': self.get_image(96, 32),
            'UP-0': self.get_image(0, 96),
            'UP-1': self.get_image(32, 96),
            'UP-2': self.get_image(64, 96),
            'UP-3': self.get_image(96, 96),
            'DOWN-0': self.get_image(0, 0),
            'DOWN-1': self.get_image(32, 0),
            'DOWN-2': self.get_image(64, 0),
            'DOWN-3': self.get_image(96, 0),

        }

        self.feet = pygame.Rect(0, 0, self.rect.width * 0.8, 12)
        self.head = pygame.Rect(0, 0, self.rect.width * 0.5, 1)
        self.right_arm = pygame.Rect(0, 0, self.rect.width * 0.5, self.rect.height * 0.8)
        self.left_arm = pygame.Rect(0, 0, self.rect.width * 0.5, self.rect.height * 0.8)
        self.old_position = self.position.copy()
        self.speed = 2
        self.clock = pygame.time.Clock()
        self.direction_cooldown = 100
        self.xp = 0
        self.valid_level = []

    def save_location(self): self.old_position = self.position.copy()

    def add_valid_level(self, level): self.valid_level.append(level)

    def get_valid_level(self): return self.valid_level

    def move_right(self):
        self.position[0] += self.speed
        key = random.randint(0, 3)
        self.image = self.images[f'RIGHT-{key}']
        self.image.set_colorkey([0, 0, 0])

    def move_left(self):
        self.position[0] -= self.speed
        key = random.randint(0, 3)
        self.image = self.images[f'LEFT-{key}']
        self.image.set_colorkey([0, 0, 0])

    def move_down(self):
        self.position[1] += self.speed
        key = random.randint(0, 3)
        self.image = self.images[f'DOWN-{key}']
        self.image.set_colorkey([0, 0, 0])

    def move_up(self):
        self.position[1] -= self.speed
        key = random.randint(0, 3)
        self.image = self.images[f'UP-{key}']
        self.image.set_colorkey([0, 0, 0])

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        self.head.midtop = self.rect.midtop
        self.right_arm.topright = self.rect.topright
        self.left_arm.topleft = self.rect.topleft

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        self.head.midtop = self.rect.midtop
        self.right_arm.topright = self.rect.topright
        self.left_arm.topleft = self.rect.topleft

    def get_image(self, x, y):
        image = pygame.Surface([24, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 24, 32))
        return image

    def get_xp(self):
        return self.xp

    def get_rect_image(self):
        return self.rect.x
