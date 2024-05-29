import pygame
import pickle
import random
from os import path

pygame.init()

pygame.display.set_caption("Arakada 3")
clock = pygame.time.Clock()
fps = 60
tile_size = 40
screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen_size = (screen_width, screen_height) 
screen= pygame.display.set_mode((0,0),pygame.FULLSCREEN)

menu_principal = True
high_score = 0
level = 1
game_over = 0
score = 0
walls_pos = []

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
    ghost_1.add(ghost_group)
    ghost_2.add(ghost_group)
    world_data = []
    if path.exists(f"levels/level{level}_data"):
        pickle_read = open(f"levels/level{level}_data", "rb")

        world_data = pickle.load(pickle_read)
        world = World(world_data)

    return world


class Node:
    def __init__(self, position = None, parent = None):
        self.position = position
        self.parent = parent
        self.G = 0
        self.H = 0
        self.F = 0


class AStar(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, finish_x, finish_y, wall_pos):
        pygame.sprite.Sprite.__init__(self)
        self.start_x = start_x
        self.start_y = start_y
        self.finish_x = finish_x
        self.finish_y = finish_y
        self.open_list = []
        self.closed_list = []
        self.wall_pos = wall_pos
        self.route = []
        self.route_found = False

        print(wall_pos, "WALLLLLLLLLLL")
        print()

    def generate_children(self, parent, end_node):
        parent_pos = parent.position
        for m in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            child_pos = (parent_pos[0] + m[0], parent_pos[1] + m[1])
            if self.check_valid(child_pos):
                child = Node(child_pos, parent)
                self.H_calc(child, end_node)
                self.F_calc(child, parent)

                if self.append_to_open(child):
                    self.open_list.append(child)

    def append_to_open(self, child):
        for open_node in self.open_list:
            if child.position == open_node.position and child.F >= open_node.F:
                return False
        return True

    def H_calc(self, child, end_node):
        child.H = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)

    def F_calc(self, child, parent):
        child.F = parent.G + 10 + child.H

    def check_valid(self, move):
        grid_x, grid_y = move
        if (grid_x, grid_y) not in self.wall_pos and (grid_x, grid_y) not in self.closed_list:
            return True
        return False

    def findEnd(self, current):
        if current == (self.finish_x, self.finish_y):
            return True
        return False

    def astar_execute(self):
        # Initialize the nodes
        start_node = Node((self.start_x, self.start_y), None)
        start_node.G = start_node.H = start_node.F = 0
        end_node = Node((self.finish_x, self.finish_y), None)
        end_node.G = end_node.H = end_node.F = 0

        self.open_list.append(start_node)

        while len(self.open_list) > 0:
            current_node = self.open_list[0]
            current_index = 0

            # get the lowest "F" node
            for index, node in enumerate(self.open_list):
                if node.F < current_node.F:
                    current_node = node
                    current_index = index

            # check if we find a route
            if self.findEnd(current_node.position):
                current = current_node
                # Append path until the current node becomes none (start node has a parent of None)
                while current is not None:
                    self.route.append(current.position)
                    current = current.parent
                self.route.pop(0)
                self.route_found = True
                break

            self.generate_children(current_node, end_node)
            self.open_list.pop(current_index)
            self.closed_list.append(current_node.position)

        if self.route_found:
            try:
                self.route.insert(0, (self.finish_x, self.finish_y))
                self.route.pop(len(self.route) - 1)
                print(self.route, "rouuuuuuuuuuuuute")
                print()
                
                
                next_pos = self.route[len(self.route) - 1]
                dx = next_pos[0] - self.start_x
                dy = next_pos[1] - self.start_y
                return (dx, dy)
            except:
                return (0,0)
        else:
            return (0,0)


def execute_search_algorithm(start_node_x, start_node_y, finish_x, end_node_y, wall_pos):
    astar = AStar(start_node_x, start_node_y, finish_x, end_node_y, wall_pos)
    if start_node_x or finish_x is not None:
        return astar.astar_execute()
    else:
        draw_text('NO ROUTE FOUND!', font_bauhaus_40, (0, 0, 0), 768, 384)
        return (0, 0)




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

class Chasingghost(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites\img_ennemi1b_1.webp")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width, self.height = 40, 40
        self.direction = (0, 0)
        self.coll_down, self.coll_left, self.coll_right, self.coll_up = False, False, False, False
        self.dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        self.colls = [self.coll_up, self.coll_right, self.coll_down, self.coll_left]
        self.previous_direction = (0, 0)
        self.counter = 0

    def update(self):
        print(self.rect.y, self.rect.y // 40, "feur")
        if not self.counter >= 19:
            self.direction = self.previous_direction
            self.counter += 1
        else:
            self.direction = execute_search_algorithm(self.rect.x // 40, self.rect.y // 40, player.rect.x // 40, player.rect.y // 40, walls_pos)
            self.counter = 0

        print(self.rect.x // 40, self.rect.y // 40, "cosssss")
        print()
        print(self.direction, "directionnnnnnnn")
        print()
        # Mettre à jour la position
        self.rect.x += self.direction[0] * 2
        self.rect.y += self.direction[1] * 2

        if self.direction != (0, 0):
            self.previous_direction = self.direction




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
                    dirt = Bloc((col_count) * tile_size, (row_count) * tile_size)
                    bloc_group.add(dirt)
                    walls_pos.append((col_count, row_count))
                if tile == 9:
                    coin = Coin((col_count) * tile_size + (tile_size // 2), (row_count) * tile_size + (tile_size // 2))
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
ghost_3 = Chasingghost(screen_width // 2 - 80, screen_height - 600)
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


    pygame.display.update()

pygame.quit()