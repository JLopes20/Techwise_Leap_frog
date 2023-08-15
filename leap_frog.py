import pygame
from pygame import Surface, mixer, sprite
import sys
import random
import menu

menu.main()

# Initialize pygame
pygame.init()

clock = pygame.time.Clock()

# Constants for screen/dimensions
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Leap Frog')

# Initialize pygame mixer
pygame.mixer.init()

# Set up the display
road_bg = pygame.image.load('Images/road2.jpg').convert()
road_bg = pygame.transform.scale(road_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

swamp_bg = pygame.image.load('Images/bg1.png').convert()
swamp_bg = pygame.transform.scale(swamp_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

BG_ROAD_SIZE = 1080

BG_SWAMP_SIZE = 1080

current_background = pygame.image.load('Images/road2.jpg').convert()
current_background = pygame.transform.scale(current_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Sounds
#mixer.music.load("Images/Swamps Nature.wav")
#mixer.music.load("Images/mixkit-subway-old-depart-ambience-2679.wav")
#mixer.music.play(-1)  # play non-stop

road_sound = mixer.music.load("Images/mixkit-subway-old-depart-ambience-2679.wav")
mixer.music.play()
#swamp_sound = mixer.music.load("Images/mixkit-insects-birds-and-frogs-in-the-swamp-ambience-40.wav")
#dead_sound = mixer.music.load("Images/mixkit-futuristic-electronic-engine-fail-2941.wav")

#mixer.music.play(1)  # play non-stop


class Player(pygame.sprite.Sprite):
    frog_position = [500, 675]  # Initial position of the frog

    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.health = 100  # health bar start width
        self.lives = 1  # number of lives
        self.alive = True
        self.is_animating = False
        self.directions = ["right", "left", "up", "down"]
        self.frog_sprites = {direction: [] for direction in self.directions}
        

        for direction in self.directions:
            for i in range(1, 7):
                image_path = f'Images/frog-{direction}{i}.png'
                sprite = pygame.image.load(image_path).convert()
                sprite.set_colorkey((0, 0, 0))
                sprite = pygame.transform.scale(sprite, (50, 50))
                self.frog_sprites[direction].append(sprite)

        self.current_sprite = 0
        self.image = self.frog_sprites["right"][self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.direction = "up"
        self.mask = pygame.mask.from_surface(self.image)
    def move(self, dx, dy):
        self.frog_position[0] += dx  # Update horizontal coordinate
        self.frog_position[1] += dy  # Update vertical coordinate
        self.rect.topleft = self.frog_position

    def move_right(self):
        if self.rect.x < SCREEN_WIDTH - self.rect.width:
            self.direction = "right"
            self.move(3, 0)

    def move_left(self):
        if self.rect.x > 0:
            self.direction = "left"
            self.move(-3, 0)

    def move_up(self):
        if self.rect.y > 0:
            self.direction = "up"
            self.move(0, -3)

    def move_down(self):
        if self.rect.y < SCREEN_HEIGHT - self.rect.height:
            self.direction = "down"
            self.move(0, 3)

    def animate(self):
        self.is_animating = True

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.animate()
            self.move_right()
        elif keys[pygame.K_LEFT]:
            self.animate()
            self.move_left()
        elif keys[pygame.K_UP]:
            self.animate()
            self.move_up()
        elif keys[pygame.K_DOWN]:
            self.animate()
            self.move_down()

    def health_bar(self, screen):
        health_bar_width = 100
        health_bar_height = 10
        health_bar_x = self.rect.x  # horizontal position of the health bar
        health_bar_y = self.rect.y - 30  # vertical position of the health bar

        pygame.draw.rect(screen, (255, 0, 0),
                         (health_bar_x, health_bar_y, health_bar_width, health_bar_height))  # Background bar
        pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, self.health, health_bar_height))  # Health bar

    def update(self, speed=0.1):
        self.movement()

        if self.is_animating:
            self.current_sprite += speed
            if self.current_sprite >= len(self.frog_sprites[self.direction]):
                self.current_sprite = 0
                self.is_animating = False

        self.image = self.frog_sprites[self.direction][int(self.current_sprite)]
        self.rect.topleft = self.frog_position

    def get_mask(self):
        return pygame.mask.from_surface(self.image)
    
    def reset_player(self):
#        self.frog_position = [500, 675]  # Initial position of the frog
#        self.rect.topleft = self.frog_position
        self.direction = "up"
        self.health = 100
        self.lives = 1
        self.alive = True


    def reset_pos(self):
       self.frog_position = [500, 675]  # Initial position of the frog
       self.rect.topleft = self.frog_position


class Car(pygame.sprite.Sprite):
    def __init__(self, image_path, pos_x, pos_y, speed):
        super().__init__()
        self.image = pygame.image.load(image_path).convert()
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.speed = speed
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x += self.speed
        if self.speed > 0 and self.rect.left > SCREEN_WIDTH:
            self.reset_position()
        elif self.speed < 0 and self.rect.right < 0:
            self.reset_position()

    def reset_position(self):
        if self.speed > 0:
            self.rect.right = 0
        else:
            self.rect.left = SCREEN_WIDTH
    
    def get_mask(self):
        return pygame.mask.from_surface(self.image)

# Create cars
cars = pygame.sprite.Group()
car_images_right = [
     "Images/car3-right.png", "Images/car4-right.png", "Images/car5-right.png", "Images/car6-right.png"
]
car_images_left = [
    "Images/car1-left.png", "Images/car2-left.png", "Images/car3-left.png", "Images/car4-left.png", "Images/car5-left.png", "Images/car6-left.png"
]

# Cars 1 to 6 move from left to right
for i in range(3):
    image_path = car_images_right[i]
#    pos_x = -random.randint(200, 450)  # Starting offscreen from the left
    pos_x = SCREEN_WIDTH + random.randint(100, 460)
    pos_y = 90 + i * 135  # Adjust the spacing between cars
    speed = random.randint(7, 14)  # Random speed 
    car = Car(image_path, pos_x, pos_y, speed)
    car.image = pygame.image.load(image_path).convert()  # Load the image
    car.image.set_colorkey((0, 0, 0))  # Remove the black background
    car.image = pygame.transform.scale(car.image, (145, 145))  # Scale the image to the desired dimensions
    cars.add(car)

# Cars 7 to 12 move from right to left
for i in range(4):
    image_path = car_images_left[i]
    pos_x = SCREEN_WIDTH + random.randint(120, 470)  # Starting offscreen from the right
    pos_y = 210 + i * 120  # Adjust the spacing between cars
    speed = -random.randint(9, 12)  # Random  speed 
    car = Car(image_path, pos_x, pos_y, speed)
    car.image = pygame.image.load(image_path).convert()  # Load the image
    car.image.set_colorkey((0, 0, 0))  # Remove the black background
    car.image = pygame.transform.scale(car.image, (145, 145))  # Scale the image to the desired dimensions
    cars.add(car)



class New_level(pygame.sprite.Sprite): # snippet of image on top of screen taking player to second background
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load('Images/beginning level1.jpg').convert()
        self.image = pygame.transform.scale(self.image, (1090, 260))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

       
#    def update(self):
#        screen.blit(self.image, self.rect)


class Lake(pygame.sprite.Sprite): # snippet of lake image on top of background
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load('Images/lake.png').convert()
        self.image = pygame.transform.scale(self.image, (1080, 390))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.layer = 1
      
       

    def update(self):
        screen.blit(self.image, self.rect)


class Gator(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        
        self.sprites = []
        self.is_animating = True
        self.sprites.append(pygame.image.load('Images/gator-right1.png').convert())
        self.sprites.append(pygame.image.load('Images/gator-right2.png').convert())
        self.sprites.append(pygame.image.load('Images/gator-right3.png').convert())
        self.sprites.append(pygame.image.load('Images/gator-right4.png').convert())
        self.sprites.append(pygame.image.load('Images/gator-left1.png').convert())
        self.sprites.append(pygame.image.load('Images/gator-left2.png').convert())
        self.sprites.append(pygame.image.load('Images/gator-left3.png').convert())
        self.sprites.append(pygame.image.load('Images/gator-left4.png').convert())
      
        # Set color to be removed for each loaded image
        for i in range(len(self.sprites)):
            self.sprites[i].set_colorkey((255, 255, 255))
            # Control the image size
            self.sprites[i] = pygame.transform.scale(self.sprites[i], (100, 100))
        
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

        self.speed = random.randrange(1, 4)
        self.mask = pygame.mask.from_surface(self.image)

    def animate(self):
        self.is_animating = True

    def update(self, speed=0.1):
        if self.is_animating:
            self.current_sprite += speed
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
                self.is_animating = True

            self.rect.x += self.speed
            if self.rect.right > SCREEN_WIDTH:
                self.rect.x = -self.rect.width 
                #self.rect.y = SCREEN_HEIGHT - self.rect.height  # Reset the position at the bottom of the screen
                self.rect.y = pos_y
                self.speed = random.randrange(1, 4)

            self.image = self.sprites[int(self.current_sprite)]
        else:
            self.rect.x += self.speed
            if self.rect.right > SCREEN_WIDTH:
                self.kill()

    def get_mask(self):
        return pygame.mask.from_surface(self.image)

class Log(pygame.sprite.Sprite):
    def __init__(self, image_path, pos_x, pos_y, speed):
        super().__init__()
        self.image_path = pygame.image.load(image_path).convert()
        self.image = self.image_path
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.speed = random.randrange(1,4)  
        self.player = None  # Player attribute
        self.image = pygame.transform.scale(self.image, (150, 75))
        self.image.set_colorkey((0, 0, 0))
        self.mask = pygame.mask.from_surface(self.image)

    def set_player(self, player):
        self.player = player

    def update(self):
        self.rect.x += self.speed
        if self.speed > 0 and self.rect.left > SCREEN_WIDTH:
            self.reset_position()
        elif self.speed < 0 and self.rect.right < 0:
            self.reset_position()

    def reset_position(self):
        if self.speed > 0:
            self.rect.right = 0
        else:
            self.rect.left = SCREEN_WIDTH

    def carry_player(self, player):
       player.frog_position[0] += self.speed  # Adjust the frog's position based on the log's speed
       player.rect.topleft = player.frog_position

    def get_mask(self):
        return pygame.mask.from_surface(self.image)
    
log1 = Log("Images/log.png", random.randint(100, 300), random.randint(300, 490), random.randint(5, 10))
log2 = Log("Images/log.png", random.randint(100, 300), random.randint(300, 490), random.randint(5, 10))
log3 = Log("Images/log.png", random.randint(100, 300), random.randint(300, 490), random.randint(5, 10))

#player = Player(Player.frog_position[0], Player.frog_position[1])
""" log1.set_player(player)
log2.set_player(player)
log3.set_player(player) """

class Health_bar:
    def __init__(self, player, screen):
        self.player = player
        self.screen = screen
        self.health_bar_width = 100
        self.health_bar_height = 20
        self.health_bar_x = 10  # horizontal position of the health bar
        self.health_bar_y = 10  # vertical position of the health bar



    def draw_health_bars(self):
        pygame.draw.rect(self.screen, (255, 0, 0),
                         (self.health_bar_x, self.health_bar_y, self.health_bar_width, self.health_bar_height))  # Background bar
        pygame.draw.rect(self.screen, (0, 255, 0),
                         (self.health_bar_x, self.health_bar_y, self.player.health, self.health_bar_height))  # Health bar
     
       # Player Health display
        if not self.player.alive:
            self.screen.fill((0, 0, 0))
            #game_over_sound = mixer.Sound("game over.wav")
            #game_over_sound.play()
            #game_over = pygame.image.load('game over.jpg').convert()
            #game_over_rect = game_over.get_rect()
            #game_over_rect.center = (500, 300)
            font1 = pygame.font.Font('freesansbold.ttf', 35)
            text1 = font1.render('Press SPACE to restart', True, (255, 255, 255))
            text1Rect = text1.get_rect()
            text1Rect.bottom = 550
            text1Rect.left = 350
           # self.screen.blit(game_over, game_over_rect)
            self.screen.blit(text1, text1Rect)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
               player.alive = True
               player.lives = 1
               player.health = 100
               player.frog_position = [500, 675]  # Reset the player's position
               player.rect.topleft = player.frog_position
               player.direction = "up"

       
        #Print Lives to screen
        font = pygame.font.Font('freesansbold.ttf', 30)
        text = font.render('Lives: ' + str(player.lives), True, (0,0,0))
        screen.blit(text,(650,20))


    def update(self):
        self.draw_health_bars()


class Caves(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()

        # Load the initial cave image
        initial_cave_image = pygame.image.load('Images/minicave.png').convert()
        initial_cave_image.set_colorkey((0, 0, 0)) 
        initial_cave_image = pygame.transform.scale(initial_cave_image, (410, 410))  

        self.sprites = [initial_cave_image] 
        self.num_min_caves = 3  # Number of additional cave images

        # Create more cave images based on the first one
        for _ in range(1, self.num_min_caves):
            new_cave_image = pygame.image.load('Images/minicave.png').convert()
            new_cave_image.set_colorkey((0, 0, 0))
            new_cave_image = pygame.transform.scale(new_cave_image, (410, 410))

            self.sprites.append(new_cave_image)

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.image = new_cave_image
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y


    def update(self):
        screen.blit(self.image, self.rect)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)
    


class CaveFrog(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load('Images/cave frog.png').convert()
        self.image = pygame.transform.scale(self.image, (50, 55))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.visible = False  # Initial visibility of cave frog
    
    def get_mask(self):
        return pygame.mask.from_surface(self.image)

# Create sprite groups with order of apperance 
sprites = pygame.sprite.Group() #Create Sprites Group

background_sprites = pygame.sprite.LayeredUpdates()
new_level = New_level(-10, -70)
sprites.add(background_sprites,cars, new_level)  # Background sprites should be drawn first

alligators_group = pygame.sprite.Group()

car_sprites = pygame.sprite.LayeredUpdates()
car_sprites.add(cars)  # Cars should be drawn on top of player and background

lake_sprites = pygame.sprite.LayeredUpdates()
sprites.add(lake_sprites)

#player = Player(Player.frog_position[0], Player.frog_position[1])
#sprites.add(player) #Add player last to keep on top
#all_sprites = pygame.sprite.LayeredUpdates()
#all_sprites.add(player, alligators_group, cave1,cave2,cave3)
background_sprites = pygame.sprite.LayeredUpdates()
background_sprites.add(background_sprites, cars)  # Background sprites should be drawn first

""" player_sprites = pygame.sprite.LayeredUpdates()
player_sprites.add(player)  """
#car_sprites = pygame.sprite.LayeredUpdates()
#car_sprites.add(cars)  # Cars should be drawn on top of player and background
#lake_sprites = pygame.sprite.LayeredUpdates()
#alligators_sprites = pygame.sprite.LayeredUpdates()
#alligators_sprites.add(alligator)
#all_sprites = pygame.sprite.LayeredUpdates()
#all_sprites.add(background_sprites,car_sprites,player_sprites)




 # Initialize objects
player = Player(Player.frog_position[0], Player.frog_position[1])
sprites.add(player)

lake = Lake(-2, 255)
alligator = Gator(100, 500)
health_bar = Health_bar(player, screen)

cave1 = Caves(-70,-8)
cave2 = Caves(50,-8)
cave3 = Caves(170, -8)

cave_frog1= CaveFrog(103,180)
cave_frog2 = CaveFrog(217,180)
cave_frog3= CaveFrog(345,180)


scroll_x = 0
scroll_y = 0
  

#main Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
       

    player.update()

    # Check for collision between player and cars
    for car in cars:
        if pygame.sprite.collide_mask(player, car):
            #if player.health > 0:
                player.health -= 10 # Reduce player's health by 
                if player.health == 0 and player.lives > 0:
                    player.lives -= 1
                    player.health = 100
                elif player.health == 0 and player.lives == 0:
                    player.alive = False
    
      # Check for collision between player and new_level
    if player.rect.colliderect(new_level.rect):
        player.reset_pos()
        #all_sprites.update()
        new_level.kill()
        lake = Lake(-2, 255)  # Create the Lake and its position x, y
        lake_sprites.add(lake)  # Add lake
        sprites.add(background_sprites, alligator, log1, log2, log3)
        #all_sprites.add(background_sprites, alligator, log1, log2, log3)
        sprites.add(player)
        #all_sprites.add(player)
        sprites.update()
        #all_sprites.add(player, alligators_sprites, cave1,cave2,cave3)


        for car in cars.sprites():
            car.kill() # remove cars
        current_background = pygame.image.load('Images/bg1.png').convert()
        current_background = pygame.transform.scale(current_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        alligators = []
        num_alligators = 4

        for alligator in range(num_alligators):
            alligator = Gator(200, 400)
            alligators.append(alligator)
#           sprites.add(alligator)
            #all_sprites.add(alligator)

    
    alligators_hit = pygame.sprite.spritecollide(player, alligators_group, False, pygame.sprite.collide_mask)
    player_colliding_with_alligator = False

    for gator in alligators_hit:
        if not player_colliding_with_alligator:
            player.health -= 10
            if player.health == 0 and player.lives > 0:
                player.lives -= 1
                player.health = 100
            elif player.health == 0 and player.lives == 0:
                player.alive = False
            player_colliding_with_alligator = True

    if len(alligators_hit) == 0:
        player_colliding_with_alligator = False


    # Check for collision between player and logs
    for log in log1, log2, log3:
        if pygame.sprite.collide_mask(log, player):
            log.carry_player(player)



    #check for collision between player and caves
    if pygame.sprite.collide_mask(player, cave1): 
#       sprites.add(cave_frog1)
       sprites.add(cave_frog1)
       player.reset_pos()
       cave_frog1.image.set_colorkey((0, 0, 0))  
  

    elif pygame.sprite.collide_mask(player, cave2): 
#        sprites.add(cave_frog2)
        sprites.add(cave_frog2)
        player.reset_pos()  # Reset the player's position
        cave_frog2.image.set_colorkey((0, 0, 0)) 


    elif pygame.sprite.collide_mask(player, cave3):
#       sprites.add(cave_frog3)
       sprites.add(cave_frog3)
       player.reset_pos()  # Reset the player's position
       cave_frog3.image.set_colorkey((0, 0, 0)) 


    screen.blit(current_background, (scroll_x, scroll_y))
    lake_sprites.draw(screen)
#   all_sprites.draw(screen)
    sprites.draw(screen)
    sprites.update()
#   all_sprites.update()
#   all_sprites.draw(screen)

    health_bar.update()


    pygame.display.flip()
    clock.tick(60)