import pygame, sys
import images

class sprite:
    def __init__(self, rect, image, move_distance):
        self.rect = rect
        self.image = image
        self.move_distance = move_distance

class Selector:
    def __init__(self, screen, sprite_size, screen_size, sprites_map_rect):
        self.screen = screen
        self.sprite_width, self.sprite_height = sprite_size
        self.screen_width, self.screen_height = screen_size
        self.rect = pygame.Rect(0,0, self.sprite_width, self.sprite_height)
        self.image = pygame.Surface((self.sprite_width, self.sprite_height))
        self.image.set_alpha(140)
        self.image.fill((255,255,0))
        self.vx = 0
        self.vy = 0
        self.sprites_rect = sprites_map_rect

    def move(self):
        self.vx = 0
        self.vy = 0
        pygame.event.pump()
        event = pygame.key.get_pressed()
        if event[pygame.K_RIGHT]:
            self.vx = self.sprite_width
        if event[pygame.K_LEFT]:
            self.vx = -self.sprite_width
        if event[pygame.K_UP]:
            self.vy = -self.sprite_height
        if event[pygame.K_DOWN]:
            self.vy = self.sprite_height

        self.check_if_not_exceed_screen()
        if self.collide_with_sprite():
            self.image.fill((255,255,255))
        else:
            self.image.fill((255,255,0))

        self.rect.x += self.vx
        self.rect.y += self.vy

    def check_if_not_exceed_screen(self):
        if ((self.rect.x + self.vx) >= self.screen_width) or ((self.rect.x + self.vx) < 0):
            self.vx = 0
        if ((self.rect.y + self.vy) >= self.screen_height) or ((self.rect.y + self.vy) < 0):
            self.vy = 0

    def collide_with_sprite(self):
        for type_sprite in self.sprites_rect:
            for name_sprite, sprite_list in type_sprite.items():
                if len(sprite_list) != 0:
                    for sprite in sprite_list:
                        if self.rect.colliderect(sprite):
                            return True
        return False

    def blit(self):
        self.screen.blit(self.image, self.rect)

class Map:
    def __init__(self, screen, sprite_width, sprite_height, name_pictures, filenames):
        self.screen = screen
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        self.name_pictures = name_pictures
        self.img_path = "media/"
        self.maps = []
        self.pictures = {}
        self.maps_rect = []
        self.sprites_map = []
        self.sprites_map_index = "undefined"
        self.sprites_map_rect = []

        for index,filename in enumerate(filenames):
            if filename == "sprites.map":
                self.sprites_map.append(map)
                self.sprites_map_index = index
            map = self.load_map(filename)
            self.maps.append(map)
        self.load_pictures()
        self.create_rect()
        print(self.maps_rect)
        self.maps_rect.remove(self.sprites_map_rect)
        print(self.maps_rect)

    def load_map(self, filename):
        map_data = []
        map_size = []
        map = []
        with open(filename) as file:
            for line in file:
                line = line.split("|")
                character_list = []
                for character in line:
                    if character != '\n':
                        character_list.append(character)
                map_data.append(character_list)
        map_size = (len(map_data), len(map_data[0]))
        return map_data

    def load_pictures(self):
        for key, value in self.name_pictures.items():
            temp_img = pygame.image.load(self.img_path + value).convert_alpha()
            self.pictures[key] = pygame.transform.scale(temp_img, (self.sprite_width, self.sprite_height))

    def init_rectDictionnary(self):
        self.rect_dic = {}
        for key in self.pictures.keys():
            self.rect_dic[key] = list()

    def create_rect(self):
        for index, map in enumerate(self.maps):
            self.init_rectDictionnary()
            for y,row in enumerate(map):
                for x, character in enumerate(row):
                    if character != '0':
                        self.rect_dic[character].append(pygame.Rect(x*self.sprite_width, y*self.sprite_height, self.sprite_width, self.sprite_height))
            self.maps_rect.append(self.rect_dic)
            if index == self.sprites_map_index:
                self.sprites_map_rect.append(self.rect_dic)

    def blit_map(self):
        for map_rect in self.maps_rect:
            for key, wall_list in map_rect.items():
                if len(wall_list) != 0:
                    for wall in wall_list:
                        self.screen.blit(self.pictures[key],wall)

class Game:
    def __init__(self, screen_size, sprite_size, images):
        pygame.init()
        self.sprite_width, self.sprite_height = sprite_size
        self.screen_width, self.screen_height = screen_size[0]*self.sprite_width, screen_size[1]*self.sprite_height
        self.images = images
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        maps = ["background.map", "sprites.map"]
        self.Map = Map(self.screen, self.sprite_width, self.sprite_height, self.images, maps)
        self.selector = Selector(self.screen, (self.sprite_width, self.sprite_height), (self.screen_width, self.screen_height), self.Map.sprites_map_rect)
        self.clock = pygame.time.Clock()

    def draw(self):
        self.Map.blit_map()
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

jeu = Game((18,10), (64,64), images.img)
jeu.loop()
