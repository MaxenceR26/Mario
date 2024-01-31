import pygame

class ManageEntity(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.entity = 'Levels/Box.png'
        self.sprite_sheet = pygame.image.load(f'{self.entity}')
        self.image = self.get_image(0, 0)

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.position = pygame.Vector2(x, y)
        self.frozen_position = pygame.Vector2(x, y)  # Nouvelle propriété pour stocker la position gelée
        self.is_frozen = False

        self.old_position = self.position.copy()

    def get_image(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image

    def change_sprite_sheet(self, filenames):
        self.entity = filenames
        self.sprite_sheet = pygame.image.load(f'{self.entity}')
        self.image = self.get_image(0, 0)

    def set_position(self, x, y):
        self.position.x = x
        self.position.y = y
        self.rect.topleft = self.position

    def get_rect_image(self):
        return self.rect

    def move_back(self):
        self.position = self.old_position

    def update(self):
        if not self.is_frozen:
            self.rect.topleft = self.position
        else:
            # Si gelé, utilisez la position gelée
            self.rect.topleft = self.frozen_position

    def freeze(self):
        self.is_frozen = True
        # Stockez la position gelée lors de la congélation
        self.frozen_position = self.position.copy()

    def unfreeze(self):
        self.is_frozen = False
