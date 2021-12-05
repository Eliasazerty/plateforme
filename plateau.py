import pygame, sys
import images
class Selector:
    def __init__(self, screen, sprite_size, screen_size):
        self.screen = screen
        self.sprite_width, self.sprite_height = sprite_size
        self.screen_width, self.screen_height = screen_size
        self.rect = pygame.Rect(0,0, self.sprite_width, self.sprite_height)
        self.image = pygame.Surface((self.sprite_width, self.sprite_height))
        self.image.set_alpha(140)
        self.image.fill((255,255,0))
        self.vx = 0
        self.vy = 0

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
        self.rect.x += self.vx
        self.rect.y += self.vy

    def check_if_not_exceed_screen(self):
        if ((self.rect.x + self.vx) >= self.screen_width) or ((self.rect.x + self.vx) < 0):
            self.vx = 0
        if ((self.rect.y + self.vy) >= self.screen_height) or ((self.rect.y + self.vy) < 0):
            self.vy = 0


    def blit(self):
        self.screen.blit(self.image, self.rect)

class Map:
    def __init__(self, screen, sprite_width, sprite_height, name_pictures):
        self.screen = screen
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        self.name_pictures = name_pictures
        self.pictures = {}
        self.pictures_rect = {}
        self.position = {}
        self.img_path = "media/"
        self.map = []
        self.load_pictures()

    def load_pictures(self):
        for key, value in self.name_pictures.items():
            temp_img = pygame.image.load(self.img_path + value).convert_alpha()
            self.pictures[key] = pygame.transform.scale(temp_img, (self.sprite_width, self.sprite_height))
            self.pictures_rect[key] = self.pictures[key].get_rect()

    def load_map(self, filename):
        with open(filename) as file:
            for line in file:
                line = line.split("|")
                character_list = []
                for character in line:
                    if character != '\n':
                        character_list.append(character)
                self.map.append(character_list)
        self.map_size = (len(self.map), len(self.map[0]))
        self.transform_map_to_dict()

    def init_PositionDictionnary(self):
        for key in self.pictures_rect.keys():
            self.position[key] = list()

    def transform_map_to_dict(self):
        self.init_PositionDictionnary()
        for y,row in enumerate(self.map):
            for x,col in enumerate(row):
                if col != "0":
                    self.position[col].append(pygame.Rect((x*self.sprite_width,y*self.sprite_height,self.pictures_rect[col].width, self.pictures_rect[col].height)))
                    
    def draw_case(self, wall):
        pygame.draw.rect(self.screen, (255,255,255), wall, 2)

    def blit_map(self):
        for key, wall_list in self.position.items():
            if len(wall_list) != 0:
                for wall in wall_list:
                    self.screen.blit(self.pictures[key],wall)
                    self.draw_case(wall)

class Game:
    def __init__(self, screen_size, sprite_size, images):
        pygame.init()
        self.sprite_width, self.sprite_height = sprite_size
        self.screen_width, self.screen_height = screen_size[0]*self.sprite_width, screen_size[1]*self.sprite_height
        self.images = images
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.Map = Map(self.screen, self.sprite_width, self.sprite_height, self.images)
        self.Map.load_map("background.map")
        self.selector = Selector(self.screen, (self.sprite_width, self.sprite_height), (self.screen_width, self.screen_height))
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
