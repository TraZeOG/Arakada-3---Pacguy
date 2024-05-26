import pygame
import pickle
import random
import heapq
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
img_bouton_start = pygame.image.load("sprites/img_bouton_start.webp")
img_bouton_add = pygame.image.load("sprites/img_bouton_add.webp")
img_bouton_delete = pygame.image.load("sprites/img_bouton_delete.webp")
img_bouton_menu = pygame.image.load("sprites/img_bouton_menu.webp")
#--------------------
img_fleche = pygame.image.load("sprites/img_fleche.webp")
img_fleche_flip = pygame.transform.flip(img_fleche, True, False)
img_coin_score = pygame.image.load("sprites\img_coin_score.webp")
img_coin_price = pygame.image.load("sprites\img_coin.webp")
img_background_score = pygame.image.load("sprites/img_background_score.webp")
#sons------------------------------------------------------------------------------
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
    text_width, text_height = font.size(texte)
    screen.blit(img, (x - text_width // 2, y - text_height // 2))


pickle_in = open(f'data/data_main', 'rb')
datas = pickle.load(pickle_in)
#factory settings::: ---------------------------
#datas = 0

def new_grid(grid):
    return [[0 if cell != 1 else cell for cell in row] for row in grid]

def save():
    pickle_out = open('data/data_main', 'wb')
    datas = high_score
    pickle.dump(datas, pickle_out)
    pickle_out.close()
    pygame.time.delay(180)

def reset_level(level):
    global world_data
    player.reset(screen_width // 2, screen_height - 200)
    ghost_group.empty()
    coin_group.empty()
    bloc_group.empty()
    ghost_1 = Ghost(screen_width // 2 - 80, screen_height - 600)
    ghost_2 = Ghost(screen_width // 2, screen_height - 600)
    ghost_3 = ChasingGhost(screen_width // 2 - 80, screen_height - 680, grid)
    ghost_1.add(ghost_group)
    ghost_2.add(ghost_group)
    ghost_3.add(ghost_group)
    world_data = []
    if path.exists(f"levels/level{level}_data"):
        pickle_read = open(f"levels/level{level}_data", "rb")

        world_data = pickle.load(pickle_read)
        world = World(world_data)

    return world




class AStar:
    def __init__(self, grid):
        self.grid = grid
        self.width = len(grid[0])
        self.height = len(grid)
        self.directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, node):
        neighbors = []
        for d in self.directions:
            neighbor = (node[0] + d[0], node[1] + d[1])
            if 0 <= neighbor[0] < self.width and 0 <= neighbor[1] < self.height and self.grid[neighbor[1]][neighbor[0]] == 0:
                neighbors.append(neighbor)
        return neighbors

    def find_path(self, start, goal):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            for neighbor in self.get_neighbors(current):
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return []






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
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width, self.height = 40, 40
        self.direction = (0, 0)
        self.previous_direction = (0, 0)
        self.coll_down, self.coll_left, self.coll_right, self.coll_up = False, False, False, False
        self.dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        self.colls = [self.coll_up, self.coll_right, self.coll_down, self.coll_left]

    def update(self):
        self.coll_up, self.coll_right, self.coll_down, self.coll_left = False, False, False, False

        # Vérification des collisions
        for bloc in bloc_group:
            if bloc.rect.colliderect(pygame.Rect(self.rect.x, self.rect.y - 2, self.width, self.height)):
                self.coll_up = True
            if bloc.rect.colliderect(pygame.Rect(self.rect.x + 2, self.rect.y, self.width, self.height)):
                self.coll_right = True
            if bloc.rect.colliderect(pygame.Rect(self.rect.x, self.rect.y + 2, self.width, self.height)):
                self.coll_down = True
            if bloc.rect.colliderect(pygame.Rect(self.rect.x - 2, self.rect.y, self.width, self.height)):
                self.coll_left = True

            if bloc.rect.colliderect(pygame.Rect(self.rect.x, self.rect.y + self.direction[1], self.width, self.height)):
                self.direction = (0, 0)
            if bloc.rect.colliderect(pygame.Rect(self.rect.x + self.direction[0], self.rect.y, self.width, self.height)):
                self.direction = (0, 0)

            if self.rect.x < 560:
                self.rect.x = 1280
            if self.rect.x > 1280:
                self.rect.x = 560

        # Mise à jour des directions possibles
        self.dirs_temp = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        self.colls = [self.coll_up, self.coll_right, self.coll_down, self.coll_left]

        nb_colls = sum(self.colls)

        # Filtrer les directions possibles en excluant la direction opposée à la précédente
        self.dirs_temp = [d for d, coll in zip(self.dirs, self.colls) if not coll and d != (-self.previous_direction[0], -self.previous_direction[1])]

        if nb_colls <= 1 or (nb_colls == 2 and self.direction == (0, 0)): 
            if self.dirs_temp:
                index = random.randint(0, len(self.dirs_temp) - 1)
                self.direction = self.dirs_temp[index]

        if nb_colls == 3 and self.direction == (0, 0):
            if self.coll_left:
                self.direction = (1, 0)
            else:
                self.direction = (-1, 0)

        # Mettre à jour la position
        self.rect.x += self.direction[0] * 2
        self.rect.y += self.direction[1] * 2

        # Mettre à jour la direction précédente
        if self.direction != (0, 0):
            self.previous_direction = self.direction


class ChasingGhost(pygame.sprite.Sprite):
    def __init__(self, x, y, grid):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites\img_ennemi1b_1.webp")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width, self.height = 40, 40
        self.direction = (0, 0)
        self.previous_direction = (0, 0)
        self.coll_down, self.coll_left, self.coll_right, self.coll_up = False, False, False, False
        self.dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        self.colls = [self.coll_up, self.coll_right, self.coll_down, self.coll_left]
        self.grid = grid
        self.path = []
        self.astar = AStar(grid)
        self.target_pos = None

    def update(self):
        ghost_pos = (self.rect.x // 40, self.rect.y // 40)
        player_pos = (player.rect.x // 40, player.rect.y // 40)

        if not self.path or ghost_pos == self.target_pos:
            self.path = self.astar.find_path(ghost_pos, player_pos)
            self.target_pos = player_pos

        if self.path:
            next_tile = self.path[0]
            next_x, next_y = next_tile[0] * 40, next_tile[1] * 40

            if abs(self.rect.x - next_x) <= 2 and abs(self.rect.y - next_y) <= 2:
                self.path.pop(0)

            dx, dy = 0, 0
            if self.rect.x < next_x:
                dx = 2
            elif self.rect.x > next_x:
                dx = -2
            if self.rect.y < next_y:
                dy = 2
            elif self.rect.y > next_y:
                dy = -2

            # Vérifier les collisions avant de déplacer
            if not self.check_collision(bloc_group, dx, dy):
                self.rect.x += dx
                self.rect.y += dy

    def check_collision(self, bloc_group, dx, dy):
        new_rect = self.rect.copy()
        new_rect.x += dx
        new_rect.y += dy

        for bloc in bloc_group:
            if new_rect.colliderect(bloc.rect):
                return True
        return False

    def update_collisions(self, bloc_group):
        self.coll_up, self.coll_right, self.coll_down, self.coll_left = False, False, False, False

        for bloc in bloc_group:
            if bloc.rect.colliderect(pygame.Rect(self.rect.x, self.rect.y - 2, self.width, self.height)):
                self.coll_up = True
            if bloc.rect.colliderect(pygame.Rect(self.rect.x + 2, self.rect.y, self.width, self.height)):
                self.coll_right = True
            if bloc.rect.colliderect(pygame.Rect(self.rect.x, self.rect.y + 2, self.width, self.height)):
                self.coll_down = True
            if bloc.rect.colliderect(pygame.Rect(self.rect.x - 2, self.rect.y, self.width, self.height)):
                self.coll_left = True




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

grid = new_grid(world_data)










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

            if self.rect.x < 560:
                self.rect.x = 1280
            if self.rect.x > 1280:
                self.rect.x = 560

            self.rect.x += self.dx
            self.rect.y += self.dy  

        screen.blit(self.image, self.rect)

        if pygame.sprite.spritecollide(self, ghost_group, False):
            game_over= -1

        return game_over
    
    
    def reset(self, x, y):

        self.image = pygame.image.load(f"sprites\img_joueur.webp")
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
bouton_start = Bouton(screen_width // 2 - 125, screen_height // 2, 260, 100, img_bouton_start)
bouton_restart = Bouton(screen_width // 2 - 125, screen_height // 2 - 45, 250, 100, img_bouton_restart)
bouton_menu = Bouton(screen_width // 2 - 125, screen_height // 2 + 95, 250, 100, img_bouton_menu)


ghost_group = pygame.sprite.Group()
chasingghost_group = pygame.sprite.Group()
ghost_1 = Ghost(screen_width // 2 - 80, screen_height - 600)
ghost_2 = Ghost(screen_width // 2, screen_height - 600)
ghost_3 = ChasingGhost(screen_width // 2 - 80, screen_height - 680, grid)
ghost_1.add(ghost_group)
ghost_2.add(ghost_group)
ghost_3.add(ghost_group)

run=True
while run==True:

    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            save()
            run = False

    clock.tick(fps)
    key = pygame.key.get_pressed()

    if menu_principal == True:

        screen.fill((120,100,100))
        draw_text('Arakada 3', font_lilitaone_50, clr_black, screen_width // 2, screen_height // 2 - 160)   

        if bouton_start.draw(1):
            menu_principal = False 
        if bouton_exit.draw(1):
            run = False

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

        if game_over == -1:
            if bouton_restart.draw(1) or key[pygame.K_RETURN]:
                pygame.time.delay(30)
                world_data = []
                world = reset_level(level)
                game_over = 0
            if bouton_menu.draw(1):
                pygame.time.delay(45)
                menu_principal = True
                game_over = 0
                world = reset_level(level)
                level = 1

        if bouton_exit.draw(1):
            run = False

        #draw_grid()

    pygame.display.update()


pygame.quit()