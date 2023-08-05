import pygame
from pygame import mixer
import sys
import random

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Leap Frog')

road_bg = pygame.image.load('Images/road2.jpg').convert()
road_bg = pygame.transform.scale(road_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

swamp_bg = pygame.image.load('Images/bg1.png').convert()
swamp_bg = pygame.transform.scale(swamp_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

BG_ROAD_SIZE = 1080

BG_SWAMP_SIZE = 1080

current_background = 'Images/road_bg'

mixer.music.load("Images/Swamps Nature.wav")
mixer.music.play(-1)  # play non-stop

class Player(pygame.sprite.Sprite):
    frog_position = [500, 675]  # Initial position of the frog

    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.health = 100  # health bar start width
        self.lives = 1 # number of lives
        self.alive = True
        self.is_animating = False
        self.sprites_right = []
        self.sprites_left = []
        self.sprites_up = []
        self.sprites_down = []

        self.sprites_right.append(pygame.image.load('Images/frog-right1.png').convert())
        self.sprites_right.append(pygame.image.load('Images/frog-right2.png').convert())
        self.sprites_right.append(pygame.image.load('Images/frog-right3.png').convert())
        self.sprites_right.append(pygame.image.load('Images/frog-right4.png').convert())
        self.sprites_right.append(pygame.image.load('Images/frog-right5.png').convert())
        self.sprites_right.append(pygame.image.load('Images/frog-right6.png').convert())

        self.sprites_left.append(pygame.image.load('Images/frog-left1.png').convert())
        self.sprites_left.append(pygame.image.load('Images/frog-left2.png').convert())
        self.sprites_left.append(pygame.image.load('Images/frog-left3.png').convert())
        self.sprites_left.append(pygame.image.load('Images/frog-left4.png').convert())
        self.sprites_left.append(pygame.image.load('Images/frog-left5.png').convert())
        self.sprites_left.append(pygame.image.load('Images/frog-left6.png').convert())

        self.sprites_up.append(pygame.image.load('Images/frog-up1.png').convert())
        self.sprites_up.append(pygame.image.load('Images/frog-up2.png').convert())
        self.sprites_up.append(pygame.image.load('Images/frog-up3.png').convert())
        self.sprites_up.append(pygame.image.load('Images/frog-up4.png').convert())
        self.sprites_up.append(pygame.image.load('Images/frog-up5.png').convert())
        self.sprites_up.append(pygame.image.load('Images/frog-up6.png').convert())

        self.sprites_down.append(pygame.image.load('Images/frog-down1.png').convert())
        self.sprites_down.append(pygame.image.load('Images/frog-down2.png').convert())
        self.sprites_down.append(pygame.image.load('Images/frog-down3.png').convert())
        self.sprites_down.append(pygame.image.load('Images/frog-down4.png').convert())
        self.sprites_down.append(pygame.image.load('Images/frog-down5.png').convert())
        self.sprites_down.append(pygame.image.load('Images/frog-down6.png').convert())

        self.current_sprite = 0
        self.image = self.sprites_right[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.direction = "up"

        self.frog_sprites = [self.sprites_right,self.sprites_left,self.sprites_up,self.sprites_down]

        for direction_sprites in self.frog_sprites:
            for i in range(len(direction_sprites)):
                direction_sprites[i].set_colorkey((0, 0, 0))
                direction_sprites[i] = pygame.transform.scale(direction_sprites[i], (50, 50))

      

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
            self.move(0, -3)# how many steps

    def move_down(self):
        if self.rect.y < SCREEN_HEIGHT - self.rect.height:
            self.direction = "down"
            self.move(0, 3)

    def move(self, dx, dy):
        self.frog_position[0] += dx  # Update horizontal coordinate
        self.frog_position[1] += dy  # Update vertical coordinate
        self.rect.topleft = self.frog_position

    def animate(self):
        self.is_animating = True

    def health_bar(self, screen):
        health_bar_width = 100
        health_bar_height = 10
        health_bar_x = self.rect.x  # horizontal position of the health bar
        health_bar_y = self.rect.y - 30  # vertical position of the health bar

        pygame.draw.rect(screen, (255, 0, 0),
                         (health_bar_x, health_bar_y, health_bar_width, health_bar_height))  # Background bar
        pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, self.health, health_bar_height))  # Health bar

    def update(self, speed=0.1):
        if self.is_animating:
            self.current_sprite += speed
            if self.current_sprite >= len(self.sprites_right):
                self.current_sprite = 0
                self.is_animating = False

        if self.direction == "right":
            self.image = self.sprites_right[int(self.current_sprite)]
        elif self.direction == "left":
            self.image = self.sprites_left[int(self.current_sprite)]
        elif self.direction == "up":
            self.image = self.sprites_up[int(self.current_sprite)]
        elif self.direction == "down":
            self.image = self.sprites_down[int(self.current_sprite)]

        self.rect.topleft = self.frog_position

    def get_mask(self):
        return pygame.mask.from_surface(self.image)
    
    def reset_player(self):
        self.frog_position = [500, 675]  # Initial position of the frog
        self.rect.topleft = self.frog_position
        self.direction = "up"
        self.health = 100
        self.lives = 1
        self.alive = True


class Car(pygame.sprite.Sprite):
    def __init__(self, image_path, pos_x, pos_y, speed):
        super().__init__()
        self.image = pygame.image.load(image_path).convert()
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.speed = speed
        


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
    "Images/car1-right.png", "Images/car2-right.png", "Images/car3-right.png", "Images/car4-right.png", "Images/car5-right.png", "Images/car6-right.png"
]
car_images_left = [
    "Images/car1-left.png", "Images/car2-left.png", "Images/car3-left.png", "Images/car4-left.png", "Images/car5-left.png", "Images/car6-left.png"
]

# Cars 1 to 6 move from left to right
for i in range(6):
    image_path = car_images_right[i]
    pos_x = -random.randint(100, 300)  # Starting offscreen from the left
    pos_y = 40 + i * 95  # Adjust the spacing between cars
    speed = random.randint(7, 11)  # Random speed 
    car = Car(image_path, pos_x, pos_y, speed)
    car.image = pygame.image.load(image_path).convert()  # Load the image
    car.image.set_colorkey((0, 0, 0))  # Remove the black background
    car.image = pygame.transform.scale(car.image, (150, 150))  # Scale the image to the desired dimensions
    cars.add(car)

# Cars 7 to 12 move from right to left
for i in range(6):
    image_path = car_images_left[i]
    pos_x = SCREEN_WIDTH + random.randint(100, 300)  # Starting offscreen from the right
    pos_y = 40 + i * 92  # Adjust the spacing between cars
    speed = -random.randint(5, 10)  # Random  speed 
    car = Car(image_path, pos_x, pos_y, speed)
    car.image = pygame.image.load(image_path).convert()  # Load the image
    car.image.set_colorkey((0, 0, 0))  # Remove the black background
    car.image = pygame.transform.scale(car.image, (150, 150))  # Scale the image to the desired dimensions
    cars.add(car)



class New_level(pygame.sprite.Sprite): # snippet of image on top of screen taking player to second background
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load('Images/beginning level1.jpg').convert()
        self.image = pygame.transform.scale(self.image, (1090, 250))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
      
       
    def update(self):
        screen.blit(self.image, self.rect)


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
                self.rect.x = -self.rect.width  # Wrap the alligator to the left side of the screen
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
        self.speed = speed
        self.player = None  # Player attribute
        self.image = pygame.transform.scale(self.image, (150, 75))
        self.image.set_colorkey((0, 0, 0))
        self.visible = current_background == 'Images/swamp_bg'

    def set_player(self, player):
        self.player = player

    def update(self):
        if current_background == 'Images/swamp_bg':
            self.rect.x += self.speed
            if self.speed > 0 and self.rect.left > SCREEN_WIDTH:
                self.reset_position()
            elif self.speed < 0 and self.rect.right < 0:
                self.reset_position()

        # Check for collision between player and logs
        if self.player is not None:  # Check if the player is set
            player_on_log = pygame.sprite.collide_mask(self.player, self)
            if player_on_log:
                self.player.move(self.speed, 0)

    def reset_position(self):
        if self.speed > 0:
            self.rect.right = 0
        else:
            self.rect.left = SCREEN_WIDTH

    def carry_player(self, player):
        if self.speed > 0:
            player.move(self.speed, 0)
        else:
            player.move(self.speed, 0)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)
    
log1 = Log("Images/log.png", random.randint(100, 300), random.randint(300, 490), random.randint(5, 10))
log2 = Log("Images/log.png", random.randint(100, 300), random.randint(300, 490), random.randint(5, 10))
log3 = Log("Images/log.png", random.randint(100, 300), random.randint(300, 490), random.randint(5, 10))

player = Player(Player.frog_position[0], Player.frog_position[1])
log1.set_player(player)
log2.set_player(player)
log3.set_player(player)

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
           # game_over_sound.play()
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

 # Initialize objects
new_level = New_level(0, 0)
lake = Lake(-2, 255)
player = Player(Player.frog_position[0], Player.frog_position[1])
alligator = Gator(100, 500)
health_bar = Health_bar(player, screen)

  
# Create sprite groups with order of apperance 
background_sprites = pygame.sprite.LayeredUpdates()
background_sprites.add(background_sprites,cars, new_level)  # Background sprites should be drawn first

player_sprites = pygame.sprite.LayeredUpdates()
player_sprites.add(player,background_sprites)  # Player sprites should be drawn on top of background

car_sprites = pygame.sprite.LayeredUpdates()
car_sprites.add(cars)  # Cars should be drawn on top of player and background

lake_sprites = pygame.sprite.LayeredUpdates()

alligators_sprites = pygame.sprite.LayeredUpdates()
alligators_sprites.add(alligator)

logs_group = pygame.sprite.Group()
logs_second_screen = pygame.sprite.Group()
logs_group.add(log1, log2, log3)

for i in range(5):
    image_path = "Images/log.png"
    pos_x = random.randint(100, 300)
    pos_y = 300 + i * 95
    speed = random.randint(5, 10)
    log = Log(image_path, pos_x, pos_y, speed)
    log.image = pygame.image.load(image_path).convert()
    log.image.set_colorkey(0, 0)
    log.image = pygame.transform.scale(log.image, (150, 50))
    logs_second_screen.add(log)

log.set_player(player)

logs_hit_second_screen = pygame.sprite.spritecollide(player, logs_group, False, pygame.sprite.collide_mask)

for i in range(5):
    image_path = "Images/log.png"
    pos_x = random.randint(100, 300)
    pos_y = 300 + i * 95
    # Adjust the spacing between logs
    speed = random.randint(5, 10)
    # Random speed for logs

    log = Log(image_path, pos_x, pos_y, speed)
    log.image = pygame.image.load(image_path).convert()
    # Load the image
    log.image.set_colorkey(0, 0)
    # Remove the background
    log.image = pygame.transform.scale(log.image, (150, 50))
    # Scale the image to the desired dimensions

    logs_second_screen.add(log)

all_sprites = pygame.sprite.LayeredUpdates()
all_sprites.add(background_sprites, player_sprites, car_sprites, log1, log2, log3)

scroll_x = 0
scroll_y = 0

#main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if player.frog_position[1] >= BG_ROAD_SIZE:
        #REMOVE IF OK player.frog_position[1] = BG_ROAD_SIZE - 1  # Move the frog back just before the transition
        player.current_sprite = 0
        current_background = swamp_bg

    # Update the current_background based on the player's location
    if player.frog_position[1] >= BG_ROAD_SIZE:
        current_background = swamp_bg
        player.current_sprite = 0  # Move the frog back to the first sprite when transitioning
    else:
        current_background = road_bg


    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        Jump_sound = mixer.Sound("Images/jump.wav")
        Jump_sound.play()
        player.animate()
        player.move_right()
        
    elif keys[pygame.K_LEFT]:
        Jump_sound = mixer.Sound("Images/jump.wav")
        Jump_sound.play()
        player.animate()
        player.move_left()
       
    elif keys[pygame.K_UP]:
        Jump_sound = mixer.Sound("Images/jump.wav")
        Jump_sound.play()
        player.animate()
        player.move_up()
        
    elif keys[pygame.K_DOWN]:
        Jump_sound = mixer.Sound("Images/jump.wav")
        Jump_sound.play()
        player.animate()
        player.move_down()
       

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

    # Check for collision between player and logs
    if player.frog_position[0] >= BG_ROAD_SIZE:  # Check if the frog is on the second screen
        for log in logs_second_screen:
            if pygame.sprite.collide_mask(player, log):
                player.move(log.speed, 0)
  
    
      # Check for collision between player and new_level
    if player.rect.colliderect(new_level.rect):
        new_level.kill()
        lake = Lake(-2, 255)  # Create the Lake and its position x, y
        lake_sprites.add(lake)  # Add lake
        all_sprites.add(background_sprites, player_sprites, alligators_sprites)

        for car in cars.sprites():
            car.kill() # remove cars
        current_background = pygame.image.load('Images/bg1.png').convert()
        current_background = pygame.transform.scale(current_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        player.reset_player()

        alligators = []
        num_alligators = 4

        for alligator in range(num_alligators):
            alligator = Gator(200, 400)
            alligators.append(alligator)
            all_sprites.add(alligator)


    
    alligators_hit = pygame.sprite.spritecollide(player, alligators_sprites, False, pygame.sprite.collide_mask)
  
   
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

    
    screen.blit(current_background, (scroll_x, scroll_y))
   
    lake_sprites.draw(screen)

    player_sprites.draw(screen)

    all_sprites.update()
    all_sprites.draw(screen)
    health_bar.update()
    player.update()

    pygame.display.flip()
    clock.tick(60)
