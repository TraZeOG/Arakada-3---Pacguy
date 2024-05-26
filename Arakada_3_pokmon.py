import pygame
import pickle
from random import randint
from os import path

pygame.init()

pygame.display.set_caption("Arakada 3")
clock = pygame.time.Clock()
fps = 60
tile_size = 40
screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen_size = (screen_width, screen_height) 
print(screen_size)
screen= pygame.display.set_mode((0,0),pygame.FULLSCREEN)

menu_principal = True
high_score = 0
level = 1
game_over = 0
score = 0

#load de trucs--------------------------------------------------------------------------------------

#fonts----------------------------------------------------------------------------------
font_bauhaus_40 = pygame.font.SysFont("Bauhaus 93", 40)
font_bauhaus_50 = pygame.font.SysFont("Bauhaus 93", 50)
font_lilitaone_30 = pygame.font.Font("fonts/LilitaOne-Regular.ttf", 30)
font_lilitaone_50 = pygame.font.Font("fonts/LilitaOne-Regular.ttf", 50)
font_lilitaone_60 = pygame.font.Font("fonts/LilitaOne-Regular.ttf", 60)
font_lilitaone_70 = pygame.font.Font("fonts/LilitaOne-Regular.ttf", 70)
font_lilitaone_80 = pygame.font.Font("fonts/LilitaOne-Regular.ttf", 80)
font_ubuntu_30 = pygame.font.Font("fonts/Ubuntu-Regular.ttf", 30)
font_ubuntu_40 = pygame.font.Font("fonts/Ubuntu-Regular.ttf", 40)
#couleurs-------------------------------------------------------------------------------
clr_white_minus = (155,155,155)
clr_white = (225,225,225)
clr_black = (0,0,0)
clr_red = (255,0,0)
clr_green = (0,255,0)
clr_blue = (0,0,255)
clr_brown = (51,0,17)
#images---------------------------------------------------------------------------
img_bouton_restart = pygame.image.load("sprites\img_bouton_restart.webp")
img_bouton_exit = pygame.image.load("sprites/img_bouton_exit.webp")
img_bouton_back = pygame.image.load("sprites/img_bouton_back.webp")
img_bouton_menu = pygame.image.load("sprites/img_bouton_menu.webp")
img_bouton_menu_pause = pygame.image.load("sprites/img_bouton_menu_pause.webp")
img_bouton_resume_pause = pygame.image.load("sprites/img_bouton_resume_pause.webp")
img_bouton_start = pygame.image.load("sprites/img_bouton_start.webp")
img_bouton_niveaux = pygame.image.load("sprites/img_bouton_niveaux.webp")
img_cadenas = pygame.image.load("sprites/img_cadenas.webp")
img_bouton_random_mg = pygame.image.load("sprites/img_bouton_random_mg.webp")
img_bouton_create = pygame.image.load("sprites/img_bouton_create.webp")
img_bouton_skins = pygame.image.load("sprites/img_bouton_skins.webp")
img_bouton_add = pygame.image.load("sprites/img_bouton_add.webp")
img_bouton_delete = pygame.image.load("sprites/img_bouton_delete.webp")
#----------------------
img_background_menu = pygame.image.load("sprites/img_background_menu.webp")
img_background_menu = pygame.transform.scale(img_background_menu, (screen_width, screen_height))
img_background_score = pygame.image.load("sprites/img_background_score.webp")
img_background_mort = pygame.image.load("sprites/img_background_mort.webp")
img_background_pause = pygame.image.load("sprites/img_background_pause.webp")
img_background_joueur_1 = pygame.image.load("sprites/img_background_joueur_1.webp")
img_background_joueur_1 = pygame.transform.scale(img_background_joueur_1, (400, 550))
img_background_joueur_2 = pygame.image.load("sprites/img_background_joueur_2.webp")
img_background_joueur_2 = pygame.transform.scale(img_background_joueur_1, (400, 550))
#--------------------
img_waiting_screen_1 = pygame.image.load(f"sprites/img_background_waiting_screen_1.webp")
img_waiting_screen_1 = pygame.transform.scale(img_waiting_screen_1, (screen_width, screen_height))
#--------------------
img_fleche = pygame.image.load("sprites/img_fleche.webp")
img_fleche_flip = pygame.transform.flip(img_fleche, True, False)
img_coin_score = pygame.image.load("sprites\img_coin_score.webp")
img_coin_price = pygame.image.load("sprites\img_coin.webp")
img_joueur_select = pygame.image.load("sprites\img_joueur_select.webp")
#sons------------------------------------------------------------------------------
jump_msc = pygame.mixer.Sound("sounds/jump_msc.wav")
jump_msc.set_volume(0.7)
coin_msc = pygame.mixer.Sound("sounds/coin_msc.mp3")
coin_msc.set_volume(1)
game_over_msc = pygame.mixer.Sound("sounds/game_over_msc.mp3")
game_over_msc.set_volume(1)




def draw_grid():
    for ligne in range(28):
        pygame.draw.line(screen, (255,255,255), (0, tile_size*ligne), (screen_width,tile_size*ligne))
        pygame.draw.line(screen, (255,255,255), (tile_size*ligne, 0), (tile_size*ligne, screen_height))

def draw_text(texte, font, couleur, x, y):
    img = font.render(texte, True, couleur)
    screen.blit(img, (x, y))


pickle_in = open(f'data/data_main', 'rb')
datas = pickle.load(pickle_in)
#factory settings::: ---------------------------
#datas = 0

def save():
    pickle_out = open('data/data_main', 'wb')
    datas = high_score
    pickle.dump(datas, pickle_out)
    pickle_out.close()
    pygame.time.delay(180)


class Bloc(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        if path.exists(f"sprites/img_dirt.webp"):
            img = pygame.image.load(f"sprites/img_dirt.webp")
        else:
            img = pygame.image.load(f"sprites/img_dirt_1.webp")
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Ghost(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites\img_ennemi1a_1.webp")
        self.image = pygame.transform.scale(self.image, (40,40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width, self.height = 40, 40
        self.direction = (0,1)
        self.coll_down, self.coll_left, self.coll_right, self.coll_up = False, False, False, False

    def update(self):
        colls = [self.coll_up, self.coll_right, self.coll_down, self.coll_left]
        dirs = [(0,-1), (1,0), (0,1), (-1,0)]
        nb_colls = 0
        for bloc in bloc_group:

            if bloc.rect.colliderect(self.rect.x, self.rect.bottom + 15, self.width, self.height):
                self.coll_down = True
            if bloc.rect.colliderect(self.rect.right + 15, self.rect.y, self.width, self.height):
                self.coll_right = True
            if bloc.rect.colliderect(self.rect.x, self.rect.top - 15, self.width, self.height):
                self.coll_up = True
            if bloc.rect.colliderect(self.rect.left - 15, self.rect.y, self.width, self.height):
                self.coll_left = True
                print(bloc.rect)
                print(self.rect.x)
    
            if bloc.rect.colliderect(self.rect.x, self.rect.y + self.direction[1], self.width, self.height):
                self.direction = (0, 0)
            if bloc.rect.colliderect(self.rect.x + self.direction[0], self.rect.y, self.width, self.height):
                self.direction = (0, 0)

            if self.rect.x < 560:
                self.rect.x = 1280
            if self.rect.x > 1280:
                self.rect.x = 560

        for coll in colls:
            if coll:
                nb_colls += 1

        print(nb_colls)
        print(colls)
        if nb_colls <= 2 or (nb_colls == 2 and self.direction == (0,0)):
            index = randint(1, 4 - nb_colls)
            if not colls[index - 1]:
                self.direction = dirs[index - 1]
            else:
                self.direction = dirs[index]
    
            nb_colls = 0

        print(self.direction)
        self.rect.x += self.direction[0] * 2
        self.rect.y += self.direction[1] * 2

class Bouton():

    def __init__(self, x, y, width, height, image):
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self, type):
        if type == 1:
            reset_click = False
            mouse_cos = pygame.mouse.get_pos()
            screen.blit(self.image, self.rect)
            if self.rect.collidepoint(mouse_cos):
                if pygame.mouse.get_pressed()[0] == 1:
                    self.clicked = True
                if pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
                    reset_click = True
                    self.clicked = False
            return reset_click
        elif type == 2:
            reset_click = False
            mouse_cos = pygame.mouse.get_pos()
            screen.blit(self.image, self.rect)
            if self.rect.collidepoint(mouse_cos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    reset_click = True
                if pygame.mouse.get_pressed()[0] == 0:
                    self.clicked = False
            return reset_click

bloc_group = pygame.sprite.Group()

class Coin(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("sprites\img_coin.webp")
        self.image = pygame.transform.scale(img, (15, 15))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

coin_group = pygame.sprite.Group()

class World():
    def __init__(self, data):
        self.tile_list = []

        row_count = 3
        for row in data:
            col_count = 14
            for tile in row:
                if tile == 1:
                    dirt = Bloc(col_count * tile_size, row_count * tile_size)
                    bloc_group.add(dirt)
                if tile == 9:
                    coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    coin_group.add(coin)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

if path.exists(f"levels/level{level}_data"):
    pickle_read = open(f"levels/level{level}_data", "rb")
    world_data = pickle.load(pickle_read)
    world = World(world_data)












class Joueur():
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, game_over):
        if game_over == 0:
            speed = 4
            key = pygame.key.get_pressed()

            coll_down = False
            coll_left= False
            coll_right = False
            coll_up = False
            for bloc in bloc_group:
                if bloc.rect.colliderect(self.rect.x, self.rect.y + self.dy, self.width, self.height):
                    self.dy = 0
                if bloc.rect.colliderect(self.rect.x + self.dx, self.rect.y, self.width, self.height):
                    self.dx= 0

                if bloc.rect.colliderect(self.rect.x, self.rect.bottom + 15, self.width, self.height):
                    coll_down = True
                if bloc.rect.colliderect(self.rect.right + 15, self.rect.y, self.width, self.height):
                    coll_right = True
                if bloc.rect.colliderect(self.rect.x, self.rect.top - 15, self.width, self.height):
                    coll_up = True
                if bloc.rect.colliderect(self.rect.left - 15, self.rect.y, self.width, self.height):
                    coll_left = True

            if key[pygame.K_LEFT] and not coll_left:
                self.dx = - 1 * speed
                self.dy = 0
            if key[pygame.K_RIGHT] and not coll_right:
                self.dx = speed
                self.dy = 0
            if key[pygame.K_UP] and not coll_up:
                self.dy = - 1 * speed
                self.dx = 0
            if key[pygame.K_DOWN] and not coll_down:
                self.dy = speed
                self.dx = 0

            self.rect.x += self.dx
            self.rect.y += self.dy  

        screen.blit(self.image, self.rect)

        return game_over
    
    
    def reset(self, x, y):

        self.image = pygame.image.load(f"sprites\img_joueur_1_0.webp")
        self.image = pygame.transform.scale(self.image, (39,39))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.dx = 0
        self.dy = 0

player = Joueur(screen_width // 2, screen_height - 200)



bouton_exit = Bouton(screen_width - 105, 15, 90, 50, img_bouton_exit)
bouton_resume_pause = Bouton(screen_width // 2 - 350, screen_height // 2 - 40, 312, 142, img_bouton_resume_pause)
bouton_menu_pause = Bouton(screen_width // 2 + 50, screen_height // 2 - 40, 312, 142, img_bouton_menu_pause)
bouton_start = Bouton(screen_width // 2 + 95, screen_height // 2 - 45, 260, 100, img_bouton_start)

ghost_1 = Ghost(screen_width // 2 - 100, screen_height // 2 + 100)

ghost_group = pygame.sprite.Group()

ghost_1.add(ghost_group)

run=True
while run==True:

    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            save()
            run = False

    clock.tick(fps)
    key = pygame.key.get_pressed()

    if menu_principal == True:
        screen.fill((100,255,100))
        draw_text('Arakada 3', font_lilitaone_50, clr_black, screen_width // 2 - 415, screen_height // 2 - 160)   

        if bouton_start.draw(1):
            menu_principal = False 

    else:

        world.draw()

        if game_over == 0:
            screen.fill((50,50,255))
            bloc_group.draw(screen)
            coin_group.draw(screen)
            ghost_group.draw(screen)

            game_over = player.update(game_over)
            ghost_group.update()

            if pygame.sprite.spritecollide(player, coin_group, True):
                coin_msc.play()
                score += 1

            if key[pygame.K_ESCAPE]:
                menu_pause = True

            screen.blit(img_background_score, (50,50))
            screen.blit(img_coin_score, (327,85))
            draw_text("helo", font_bauhaus_50, clr_black, 90, 85)
            draw_text('x ' + str(score), font_bauhaus_50, clr_black, 370, 85)

        #draw_grid()

    pygame.display.update()


pygame.quit()