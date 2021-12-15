import pygame, sys
import images, sprites_specificity
import random
from hashlib import sha256 as hashlib_sha256
from os import path as os_path

class tank:
    def __init__(self, screen, image, rect, specificity, name):
        self.screen = screen
        self.image = image
        self.rect = rect
        self.FireDistance, self.MovementDistance = specificity
        self.name = name

    def blit(self):
        self.screen.blit(self.image, self.rect)

    def informations(self):
        print(f"tank: {self.name} = {self.image}, {self.rect}, can shot to {self.FireDistance} and move to {self.MovementDistance}")

class sprites:
    def __init__(self, screen, sprite_width, sprite_height, name_pictures, filenames, tanks_specificity, selector):
        self.Map = Map(screen, sprite_width, sprite_height, name_pictures, filenames)
        self.screen = screen
        self.tanks_specificity = tanks_specificity
        self.selector = selector
        self.sprite_list = []
        for dic in self.Map.maps_rect:
            for key,value_list in dic.items():
                for rect in value_list:
                    self.sprite_list.append(tank(self.screen, self.Map.pictures[key], rect, self.tanks_specificity[key], key))
        self.update_sprite_list()

    def update_sprite_list(self):
        self.selector.update_sprite_list(self.sprite_list)

    def blit(self):
        for tank in self.sprite_list:
            tank.blit()

class Selector:
    def __init__(self, screen, sprite_size, screen_size):
        self.YELLOW = (255,255,0)
        self.WHITE = (255,255,255)
        self.GREEN = (0,255,0)
        self.RED = (255,0,0)

        self.screen = screen
        self.sprite_width, self.sprite_height = sprite_size
        self.screen_width, self.screen_height = screen_size

        self.rect = pygame.Rect(0,0, self.sprite_width, self.sprite_height)
        self.image = pygame.Surface((self.sprite_width, self.sprite_height))
        self.image.set_alpha(140)
        self.image.fill(self.YELLOW)

        self.selected_image = pygame.Surface((self.sprite_width, self.sprite_height))
        self.selected_image.set_alpha(140)
        self.selected_image.fill(self.GREEN)

        self.sprite_list = []
        self.SpriteMovementCaseList = []
        self.VisitedSpriteMovementList = []
        self.VisitedSpriteMovementList_rect = []
        self.HoveredSprite = None
        self.SelectedSprite = None
        self.vx = 0
        self.vy = 0

    def move(self):
        self.vx, self.vy = 0,0
        pygame.event.pump()
        event = pygame.key.get_pressed()
        self.vx = (event[pygame.K_RIGHT]-event[pygame.K_LEFT])*self.sprite_width
        self.vy = (event[pygame.K_DOWN]-event[pygame.K_UP])*self.sprite_height

        self.check_if_not_exceed_screen()
        if self.collide_with_sprite():
            self.image.set_alpha(200)
            self.image.fill(self.WHITE)
        else:
            self.image.set_alpha(140)
            self.image.fill(self.YELLOW)

        self.check_if_sprite_select()
        self.rect.x += self.vx
        self.rect.y += self.vy

    def check_if_not_exceed_screen(self):
        if ((self.rect.x + self.vx) >= self.screen_width) or ((self.rect.x + self.vx) < 0):
            self.vx = 0
        if ((self.rect.y + self.vy) >= self.screen_height) or ((self.rect.y + self.vy) < 0):
            self.vy = 0

    def update_sprite_list(self, list):
        self.sprite_list = list

    def check_if_sprite_select(self):
        pygame.event.pump()
        event = pygame.key.get_pressed()
        if event[pygame.K_RETURN]:
            self.change_SelectedSprite()
            self.VisitedSpriteMovementList.clear()
            self.VisitedSpriteMovementList_rect.clear()

        if self.SelectedSprite != None:
            self.blit_spriteMovement_arrea() # aie aie aie la fôte d'ortaugraf !
            self.collide_with_spriteMovementCase()
            self.draw_selector_case()

    def change_SelectedSprite(self): # si un sprite est survolé (self.HoveredSprite), il devient selectionné (self.SelectedSprite), sinon rien
        if self.HoveredSprite != None and self.SelectedSprite == None:
            self.SelectedSprite = self.HoveredSprite
        else:
            self.SelectedSprite = None

    def collide_with_sprite(self):
        for sprite in self.sprite_list:
            if self.rect.colliderect(sprite):
                self.HoveredSprite = sprite
                return True
        self.HoveredSprite = None
        return False

    def collide_with_spriteMovementCase(self):
        for sprite in self.SpriteMovementCaseList:
            if self.rect.colliderect(sprite):
                self.image.set_alpha(200)
                self.image.fill(self.RED)
                if sprite not in self.VisitedSpriteMovementList:
                    self.VisitedSpriteMovementList.append(sprite)
                    self.VisitedSpriteMovementList_rect.append(self.rect)
                    #print(self.VisitedSpriteMovementList_rect)

    def get_movement_on_sprite_arrea(self):
        pass

    def blit(self):
        self.screen.blit(self.image, self.rect)

    def blit_spriteMovement_arrea(self):
        self.SpriteMovementCaseList.clear()
        for i in range(self.SelectedSprite.MovementDistance):
            new_posx1 = pygame.Rect(self.SelectedSprite.rect.x + i*self.sprite_width, self.SelectedSprite.rect.y, self.sprite_width, self.sprite_height)
            new_posx2 = pygame.Rect(self.SelectedSprite.rect.x - i*self.sprite_width, self.SelectedSprite.rect.y, self.sprite_width, self.sprite_height)

            new_posy1 = pygame.Rect(self.SelectedSprite.rect.x, self.SelectedSprite.rect.y + i*self.sprite_height, self.sprite_width, self.sprite_height)
            new_posy2 = pygame.Rect(self.SelectedSprite.rect.x, self.SelectedSprite.rect.y - i*self.sprite_height, self.sprite_width, self.sprite_height)

            self.screen.blit(self.selected_image, new_posx1)
            self.screen.blit(self.selected_image, new_posx2)
            self.screen.blit(self.selected_image, new_posy1)
            self.screen.blit(self.selected_image, new_posy2)

            self.SpriteMovementCaseList.append(new_posx1)
            self.SpriteMovementCaseList.append(new_posx2)
            self.SpriteMovementCaseList.append(new_posy1)
            self.SpriteMovementCaseList.append(new_posy2)

    def draw_selector_case(self):
        thickness = 5
        for case in self.VisitedSpriteMovementList:
            pygame.draw.line(self.screen, self.WHITE, case.center, (case.centerx, case.centery), thickness)

class Map: # comment differencier les maps qui "changent" des autres? -> on le fait pas :)
    def __init__(self, screen, sprite_width, sprite_height, name_pictures, filenames):
        self.screen = screen
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        self.name_pictures = name_pictures
        self.img_path = "media/"
        self.maps = []
        self.pictures = {}
        self.maps_rect = []

        self.map_hash = ''
        for filename in filenames: # permet d'afficher plusieurs maps (pour avoir des backgrounds par exemple)
            map = self.load_map(filename)
            self.maps.append(map)
            self.map_hash += self.hash_file(filename)
        self.load_pictures()
        self.create_rect()
        self.base_map_image = self.create_map_image()

    def hash_file(self, filename):
        file = filename # Location of the file (can be set a different way)
        BLOCK_SIZE = 65536 # The size of each read from the file

        file_hash = hashlib_sha256() # Create the hash object, can use something other than `.sha256()` if you wish
        with open(file, 'rb') as f: # Open the file to read it's bytes
            fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
            while len(fb) > 0: # While there is still data being read from the file
                file_hash.update(fb) # Update the hash
                fb = f.read(BLOCK_SIZE) # Read the next block from the file

        #print (file_hash.hexdigest()) # Get the hexadecimal digest of the hash
        return (file_hash.hexdigest())

    def load_map(self, filename):
        map_data = []
        with open(filename) as file:
            for line in file:
                line = line.split("|")
                character_list = []
                for character in line:
                    if character != '\n':
                        character_list.append(character)
                map_data.append(character_list)
        self.map_size = (len(map_data[0]), len(map_data))
        return map_data

    def load_pictures(self): # permet de charger les images dans le dic self.pictures à partir des correspondances contenues dans images.py
        for key, value in self.name_pictures.items():
            temp_img = pygame.image.load(self.img_path + value).convert_alpha()
            self.pictures[key] = pygame.transform.scale(temp_img, (self.sprite_width, self.sprite_height))

    def init_rectDictionnary(self):
        self.rect_dic = {}
        for key in self.pictures.keys():
            self.rect_dic[key] = list()

    def create_rect(self): # permet de créer un dic avec correspondance d'une liste de position de cette image: {'img1': [liste de positions], 'img2': [liste de position2]}
        for index, map in enumerate(self.maps):
            self.init_rectDictionnary()
            for y,row in enumerate(map):
                for x, character in enumerate(row):
                    if character != '0':
                        self.rect_dic[character].append(pygame.Rect(x*self.sprite_width, y*self.sprite_height, self.sprite_width, self.sprite_height))
            self.maps_rect.append(self.rect_dic)

    def blit_map(self):
        self.screen.blit(self.base_map_image, (0,0))
        """
        for map_rect in self.maps_rect:
            for key, wall_list in map_rect.items():
                if len(wall_list) != 0:
                    for wall in wall_list:
                        self.screen.blit(self.pictures[key],wall)
        """
    
    def create_map_image(self): # creates an image of all the maps contained in self.maps if thei image of the map is not existing. Else, it loads the map who already exists
        if not os_path.isfile(f"{self.img_path}{self.map_hash}.png"):
            default_image = pygame.Surface((self.sprite_width, self.sprite_height))
            default_image.fill((0,0,255)) 
            map_image = pygame.Surface((self.map_size[0]*self.sprite_width, self.map_size[1]*self.sprite_height))
            for map in self.maps:
                for y, map_elements in enumerate(map):
                    for x, element in enumerate(map_elements):
                        if element != '0':
                            map_image.blit(self.pictures[element], (x*self.sprite_width, y*self.sprite_height))
                        else:
                            map_image.blit(default_image, (x*self.sprite_width, y*self.sprite_height))
            pygame.image.save(map_image, f"{self.img_path}{self.map_hash}.png")
            print(f"[+] saved new image called [{self.img_path}{self.map_hash}.png]")
            return map_image
        else:
            map_image = pygame.image.load(f"{self.img_path}{self.map_hash}.png").convert()
            map_image.set_colorkey((0,0,255))
            print(f"[=] opened file \"{self.img_path}{self.map_hash}.png\"")
            return map_image

class Game:
    def __init__(self, screen_size, sprite_size, plateforms_images,sprite_images, tanks_specificity):
        pygame.init()
        self.sprite_width, self.sprite_height = sprite_size
        self.screen_width, self.screen_height = screen_size[0]*self.sprite_width, screen_size[1]*self.sprite_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        plateforms_maps = ["background.map"]
        sprites_map = ["sprites.map"]
        self.Map = Map(self.screen, self.sprite_width, self.sprite_height, plateforms_images, plateforms_maps)
        self.selector = Selector(self.screen, (self.sprite_width, self.sprite_height), (self.screen_width, self.screen_height))
        self.sprites = sprites(self.screen, self.sprite_width, self.sprite_height, sprite_images, sprites_map, tanks_specificity, self.selector)
        self.clock = pygame.time.Clock()

    def draw(self):
        self.Map.blit_map()
        self.sprites.blit()
        self.selector.move()
        self.selector.blit()

    def loop(self):
        while True:
            self.clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            self.draw()
            pygame.display.flip()

jeu = Game((18,10), (64,64), images.plateforms, images.sprites, sprites_specificity.tanks)
jeu.loop()
