import time

import pygame
import pyscroll
import pytmx

from Entity import ManageEntity
from MAP.registerMap import MapSwitcher
from player import Player

pygame.init()


class Game:
    def __init__(self):
        self.enter_house_rect = None
        self.screen = pygame.display.set_mode((1080, 720))
        self.running = True
        self.map = 'world'

        tmx_data = pytmx.util_pygame.load_pygame('MAP/map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        self.player_position = tmx_data.get_object_by_name("Spawn")
        self.player = Player(self.player_position.x, self.player_position.y)
        self.xp = self.player.get_xp()
        self.walls = []
        self.id = []

        for obj in tmx_data.objects:
            if obj.type == "Collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == "enter_house":
                self.id.append(obj.name)

        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=6)
        self.group.add(self.player)

        # Définir le rectangle de collision afin d'entrer dans la maison

        self.map_switcher = MapSwitcher(self.screen, self.player, self.group)
        self.walls = self.map_switcher.switch_map('MAP/map', 'enter_house', 'Spawn', 2, 0, 6)

    def switch_map(self, map_name, portalFrom, portalTo, zoom, box, nombre_calc):
        self.walls = self.map_switcher.switch_map(map_name, portalFrom, portalTo, zoom, box, nombre_calc)

    def get_rect(self):
        return self.map_switcher.enter_house_rect()

    def update(self):
        self.level = self.player.get_valid_level()

        if self.map == 'world' and any(
                self.player.feet.colliderect(rect) for rect in self.map_switcher.get_enter_house_rect_list()):
            if self.player.feet.colliderect(self.map_switcher.get_enter_house_rect_list()[0]):
                print("Teleporting to Levels/1")
                self.switch_map('Levels/1', 'exit_house', 'spawn_first_level', 2, 1, 1)
                self.map = 'Levels/1'
                print("Player position after teleportation:", self.player.position)
            elif self.player.feet.colliderect(self.map_switcher.get_enter_house_rect_list()[1]): # and len(self.level) >= 1
                print("Teleporting to Levels/2")
                self.switch_map('Levels/2', 'exit_house', 'spawn_second_level', 2, 1, 1)
                self.map = 'Levels/2'
                print("Player position after teleportation:", self.player.position)

        if self.map_switcher.are_all_boxes_valid():
            self.switch_map('MAP/map', 'enter_house', self.map_switcher.return_spawnPoint(), 2, 0, 6)
            self.map = 'world'

        self.map_switcher.update()

        for sprite in self.group.sprites():
            if isinstance(sprite, Player):
                if sprite.feet.collidelist(self.walls) > -1:
                    sprite.move_back()
                elif sprite.head.collidelist(self.walls) > -1:
                    sprite.move_back()

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()
        if pressed[pygame.K_DOWN]:
            self.player.move_down()
        if pressed[pygame.K_LEFT]:
            self.player.move_left()
        if pressed[pygame.K_RIGHT]:
            self.player.move_right()

    def run(self):

        while self.running:
            clock = pygame.time.Clock()

            self.player.save_location()
            self.handle_input()
            self.update()
            self.map_switcher.draw()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            clock.tick(60)


game = Game()
game.run()
