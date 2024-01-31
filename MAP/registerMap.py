import pygame
import pyscroll
import pytmx

from Entity import ManageEntity
from player import Player

class MapSwitcher:
    def __init__(self, screen, player, group):
        self.enter_house = pytmx
        self.screen = screen
        self.player = player
        self.group = group
        self.enter_house_rect = None
        self.enter_house_rect_list = []
        self.boxNumber = 0
        self.manage_entities = []
        self.box_positions = []

        self.exit_house_position = []
        self.box_contacts = []
        self.add_score = None
        self.xp = self.player.xp
        self.textCoins = pygame.font
        self.textRect = pygame.rect
        self.world = False
        self.world_name = ''

        self.number_box = 0

        self.valide = False

        self.counter = 0
        self.exists_id = []

        self.walls = []

        self.level_xp = {
            'Levels/1': 30,
            'Levels/2': 50,
            'Levels/3': 75,
            'Levels/4': 100
        }

        self.spawnPoint = {
            'Levels/1': 'spawn_enter_house',
            'Levels/2': 'spawn_enter_house2',
        }

    def switch_map(self, map_name, portalFrom, portalTo, zoom, boxNumber, nombre_calc):
        tmx_data = pytmx.util_pygame.load_pygame(f'{map_name}.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = zoom
        self.world_name = map_name

        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "Collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=nombre_calc)
        self.group.add(self.player)

        self.boxNumber = boxNumber
        self.exists_id = []
        self.manage_entities = []
        self.box_positions = []
        self.number_box = 0
        self.counter = 0
        self.add_score = None
        self.box_contacts = []  # Réinitialiser la liste des boîtes en contact
        self.exit_house_position = []

        if int(boxNumber) > 0:
            for obj in tmx_data.objects:
                if obj.name == "SpawnerBox":
                    manage_entity = ManageEntity(obj.x, obj.y - 20)
                    self.manage_entities.append(manage_entity)
                    self.group.add(manage_entity)
                    self.number_box += 1
                    self.box_positions.append([obj.x, obj.y, obj.id])
                if obj.name == "exit_house":
                    self.exit_house_position.append([obj.x, obj.y])

        if map_name == 'MAP/map':
            for obj in tmx_data.objects:
                if obj.type == portalFrom:
                    self.enter_house_rect_list.append(
                        pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        else:
            self.enter_house = tmx_data.get_object_by_name(portalFrom)
            self.enter_house_rect = pygame.Rect(self.enter_house.x, self.enter_house.y, self.enter_house.width,
                                                self.enter_house.height)

        self.spawn_player = tmx_data.get_object_by_name(portalTo)
        self.player.position[0] = self.spawn_player.x - 15
        self.player.position[1] = self.spawn_player.y - 20

        print('Nom de la map actuel', map_name)
        if map_name == 'MAP/map':
            yellow = (255, 255, 0)
            font = pygame.font.Font('ARIAL.TTF', 32)
            self.textCoins = font.render(f'Coins : {self.xp}', True, yellow)
            self.textRect = self.textCoins.get_rect()
            self.world = True
        else:
            self.world = False

        return self.walls

    def draw(self):
        self.group.draw(self.screen)
        self.group.center(self.player.rect.center)
        if self.world:
            self.screen.blit(self.textCoins, ((self.screen.get_width() / 2) - 50, 10))
            pygame.display.flip()

    # Modifier la méthode get_contact dans la classe MapSwitcher
    def get_contact(self):
        for i, manage_entity in enumerate(self.manage_entities):
            for exit_house_pos in self.exit_house_position:
                exit_house_x, exit_house_y = exit_house_pos

                # Vérifier si la boîte est sur le point de sortie (à la fois pour X et Y)
                if exit_house_x - 2 <= int(manage_entity.rect.x) <= exit_house_x + 3 \
                        and exit_house_y - 5 <= int(manage_entity.rect.y) <= exit_house_y + 5:
                    if not manage_entity.is_frozen:  # Assurez-vous que la boîte n'est pas déjà gelée
                        box_id = self.box_positions[i][2]

                        # Vérifier si l'ID de la boîte n'a pas encore été ajouté à la liste
                        if box_id not in self.exists_id:
                            self.exists_id.append(box_id)

                        manage_entity.change_sprite_sheet('Levels/BoxValide.png')
                        manage_entity.freeze()

                    break

        # Vérifier si toutes les boîtes sont valides
        if len(self.exists_id) >= self.number_box:
            self.xp += self.level_xp[self.world_name]
            print("All boxes are valid. Teleporting...")
            self.teleport_player()

    def teleport_player(self):
        self.enter_house_rect = pygame.Rect(self.enter_house.x, self.enter_house.y, self.enter_house.width,
                                            self.enter_house.height)

        if self.world_name not in self.player.get_valid_level():
            self.player.add_valid_level(self.world_name)

    def move(self):
        for sprite in self.group.sprites():
            if isinstance(sprite, Player):
                for wall in self.walls:
                    for manage_entity in self.manage_entities:
                        # Utilisez les coordonnées des ManageEntity pour la collision
                        if self.player.feet.colliderect(manage_entity.get_rect_image()):
                            self.get_contact()
                            manage_entity.set_position(manage_entity.rect.x, manage_entity.rect.y + 3)
                        elif self.player.head.colliderect(manage_entity.get_rect_image()):
                            self.get_contact()
                            manage_entity.set_position(manage_entity.rect.x, manage_entity.rect.y - 3)
                        elif self.player.right_arm.colliderect(manage_entity.get_rect_image()):
                                if manage_entity.rect.colliderect(wall):
                                    print("e")
                                else:
                                    self.get_contact()
                                    manage_entity.set_position(manage_entity.rect.x + 3, manage_entity.rect.y)
                        elif self.player.left_arm.colliderect(manage_entity.get_rect_image()):
                            self.get_contact()
                            manage_entity.set_position(manage_entity.rect.x - 3, manage_entity.rect.y)

                    # Déplacez les ManageEntity en dehors des murs après avoir géré les collisions avec le joueur

                        # Vérifiez la collision avec les murs après le déplacement


                manage_entity.update()



    def get_enter_house_rect(self):
        return self.enter_house_rect

    def are_all_boxes_valid(self):
        if len(self.exists_id) != 0:
            return len(self.exists_id) >= self.number_box

    def get_enter_house_rect_list(self):
        return self.enter_house_rect_list

    def return_spawnPoint(self):
        return self.spawnPoint[self.world_name]

    def update(self):
        self.group.update()
        if self.boxNumber > 0:
            self.move()
