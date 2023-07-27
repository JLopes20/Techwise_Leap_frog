import pygame
from pygame import mixer
import sys
import random

pygame.init()
clock = pygame.time.Clock()

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Leap Frog')

road_bg = pygame.image.load('road2.jpg').convert()
road_bg = pygame.transform.scale(road_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

swamp_bg = pygame.image.load('bg.jpg').convert()
swamp_bg = pygame.transform.scale(swamp_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

BG_ROAD_SIZE = 1080

BG_SWAMP_SIZE = 1080

level = 1

level2 = 2

#mixer.music.load("Swamps Nature.wav")
#mixer.music.play(0)  # play non-stop -1 is continuous play



class Player(pygame.sprite.Sprite):
    frog_position = [500, 675]  # Initial position of the frog

    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.health = 250  # health bar start width
        self.lives = 3 # number of lives
        self.alive = True
       
        self.is_animating = False
        self.sprites_right = []
        self.sprites_left = []
        self.sprites_up = []
        self.sprites_down = []

        self.sprites_right.append(pygame.image.load('frog-right1.png').convert())
        self.sprites_right.append(pygame.image.load('frog-right2.png').convert())
        self.sprites_right.append(pygame.image.load("frog-right3.png").convert())
        self.sprites_right.append(pygame.image.load('frog-right4.png').convert())
        self.sprites_right.append(pygame.image.load('frog-right5.png').convert())
        self.sprites_right.append(pygame.image.load('frog-right6.png').convert())

        self.sprites_left.append(pygame.image.load('frog-left1.png').convert())
        self.sprites_left.append(pygame.image.load('frog-left2.png').convert())
        self.sprites_left.append(pygame.image.load('frog-left3.png').convert())
        self.sprites_left.append(pygame.image.load('frog-left4.png').convert())
        self.sprites_left.append(pygame.image.load('frog-left5.png').convert())
        self.sprites_left.append(pygame.image.load('frog-left6.png').convert())

        self.sprites_up.append(pygame.image.load('frog-up1.png').convert())
        self.sprites_up.append(pygame.image.load('frog-up2.png').convert())
        self.sprites_up.append(pygame.image.load('frog-up3.png').convert())
        self.sprites_up.append(pygame.image.load('frog-up4.png').convert())
        self.sprites_up.append(pygame.image.load('frog-up5.png').convert())
        self.sprites_up.append(pygame.image.load('frog-up6.png').convert())

        self.sprites_down.append(pygame.image.load('frog-down1.png').convert())
        self.sprites_down.append(pygame.image.load('frog-down2.png').convert())
        self.sprites_down.append(pygame.image.load('frog-down3.png').convert())
        self.sprites_down.append(pygame.image.load('frog-down4.png').convert())
        self.sprites_down.append(pygame.image.load('frog-down5.png').convert())
        self.sprites_down.append(pygame.image.load('frog-down6.png').convert())

        self.current_sprite = 0
        self.image = self.sprites_right[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.direction = "right"

        # Set color to be removed for each loaded image
        for i in range(len(self.sprites_right)):
            self.sprites_right[i].set_colorkey((0, 0, 0))
            # Control the image size
            self.sprites_right[i] = pygame.transform.scale(self.sprites_right[i], (70, 40))

        for i in range(len(self.sprites_left)):
            self.sprites_left[i].set_colorkey((0, 0, 0))
            # Control the image size
            self.sprites_left[i] = pygame.transform.scale(self.sprites_left[i], (70, 40))

        for i in range(len(self.sprites_up)):
            self.sprites_up[i].set_colorkey((0, 0, 0))
            # Control the image size
            self.sprites_up[i] = pygame.transform.scale(self.sprites_up[i], (70, 40))

        for i in range(len(self.sprites_down)):
            self.sprites_down[i].set_colorkey((0, 0, 0))
            # Control the image size
            self.sprites_down[i] = pygame.transform.scale(self.sprites_down[i], (70, 40))# frog size

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


# Create cars
cars = pygame.sprite.Group()
car_images_right = [
    "car1-right.png", "car2-right.png", "car3-right.png", "car4-right.png", "car5-right.png", "car6-right.png"
]
car_images_left = [
    "car1-left.png", "car2-left.png", "car3-left.png", "car4-left.png", "car5-left.png", "car6-left.png"
]

# Cars 1 to 6 move from left to right
for i in range(6):
    image_path = car_images_right[i]
    pos_x = -random.randint(100, 300)  # Starting offscreen from the left
    pos_y = 40 + i * 80  # Adjust the spacing between cars
    speed = random.randint(3, 7)  # Random speed between 3 and 7
    car = Car(image_path, pos_x, pos_y, speed)
    car.image = pygame.image.load(image_path).convert()  # Load the image
    car.image.set_colorkey((0, 0, 0))  # Remove the black background
    car.image = pygame.transform.scale(car.image, (150, 150))  # Scale the image to the desired dimensions
    cars.add(car)

# Cars 7 to 12 move from right to left
for i in range(6):
    image_path = car_images_left[i]
    pos_x = SCREEN_WIDTH + random.randint(100, 300)  # Starting offscreen from the right
    pos_y = 40 + i * 80  # Adjust the spacing between cars
    speed = -random.randint(3, 7)  # Random negative speed between -3 and -7
    car = Car(image_path, pos_x, pos_y, speed)
    car.image = pygame.image.load(image_path).convert()  # Load the image
    car.image.set_colorkey((0, 0, 0))  # Remove the black background
    car.image = pygame.transform.scale(car.image, (150, 150))  # Scale the image to the desired dimensions
    cars.add(car)


class New_level(pygame.sprite.Sprite): # snippet of image on top of screen taking player to second background
    def __init__(self, pos_x, pos_y, speed):
        super().__init__()
        self.image = pygame.image.load('beginning level1.jpg').convert()
        self.image = pygame.transform.scale(self.image, (1090, 230))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.speed = speed

    def update(self):
        screen.blit(self.image, self.rect)



class Health_bar:
    def __init__(self, player, screen):
        self.player = player
        self.screen = screen
        self.health_bar_width = 250
        self.health_bar_height = 20
        self.health_bar_x = 10  # horizontal position of the health bar
        self.health_bar_y = 10  # vertical position of the health bar

    def draw_health_bars(self):
        pygame.draw.rect(self.screen, (255, 0, 0),
                         (self.health_bar_x, self.health_bar_y, self.health_bar_width, self.health_bar_height))  # Background bar
        pygame.draw.rect(self.screen, (0, 255, 0),
                         (self.health_bar_x, self.health_bar_y, self.player.health, self.health_bar_height))  # Health bar
     
        # Player Health display
      
   
        if self.player.alive == False:
            self.screen.fill((0, 0, 0))
          
            game_over_sound = mixer.Sound("game over.wav")
            
            game_over_sound.play()
          
            game_over = pygame.image.load('game over.jpg').convert()
           
            game_over_rect = game_over.get_rect()
            game_over_rect.center = (500, 300)

            font1 = pygame.font.Font('freesansbold.ttf', 35)

            text1 = font1.render('Press R to restart', True, (255, 255, 255))

            text1Rect = text1.get_rect()
            text1Rect.bottom = 550
            text1Rect.left = 350

            self.screen.blit(game_over, game_over_rect)
            self.screen.blit(text1, text1Rect)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self.player.alive = True
                self.player.lives = 5
                self.player.health = 250

       
        #Print Lives to screen
        font = pygame.font.Font('freesansbold.ttf', 30)
        text = font.render('Lives: ' + str(player.lives), True, (0,0,0))
        screen.blit(text,(650,20))


    def update(self):
        self.draw_health_bars()

# print image to screen
new_level = New_level(0, 0, 0)

player = Player(Player.frog_position[0], Player.frog_position[1])

# print Health_bar
health_bar = Health_bar(player, screen)

all_sprites = pygame.sprite.Group()
all_sprites.add(player, cars, new_level)

scroll_x = 0
scroll_y = 0
current_background = road_bg

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        Jump_sound = mixer.Sound("jump.wav")
        Jump_sound.play()
        player.animate()
        player.move_right()
        
    elif keys[pygame.K_LEFT]:
        Jump_sound = mixer.Sound("jump.wav")
        Jump_sound.play()
        player.animate()
        player.move_left()
       
    elif keys[pygame.K_UP]:
        Jump_sound = mixer.Sound("jump.wav")
        Jump_sound.play()
        player.animate()
        player.move_up()
        
    elif keys[pygame.K_DOWN]:
        Jump_sound = mixer.Sound("jump.wav")
        Jump_sound.play()
        player.animate()
        player.move_down()
       

    if player.frog_position[0] >= BG_ROAD_SIZE:
       current_background = swamp_bg

    screen.blit(current_background, (scroll_x, scroll_y))




    # Check for collision between player and cars
    for car in cars:
        if player.rect.colliderect(car.rect):
            if player.health > 0:
                player.health -= 1  # Reduce player's health by 1
                if player.health == 0 and player.lives > 0:
                    player.lives -= 1
                    player.health = 250
                elif player.health == 0 and player.lives == 0:
                     player.alive = False

    
      # Check for collision between player and new_level
    if player.rect.colliderect(new_level.rect):
        new_level.kill()
       
        for car in cars.sprites():
            car.kill() # remove cars
        current_background = pygame.image.load('bg.jpg').convert()
        current_background = pygame.transform.scale(current_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        #player.frog_position = 700
        #player.rect = player.frog_position
  

    all_sprites.update()
    all_sprites.draw(screen)
    health_bar.update()
    player.update()

    pygame.display.flip()
    clock.tick(60)
