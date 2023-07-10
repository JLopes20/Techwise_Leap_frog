import pygame
import sys
import random
import math

class Player(pygame.sprite.Sprite):
    frog_position = [100, 400]  # Initial position of the frog

    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites_right = []
        self.sprites_left = []
        self.is_animating = False

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

     

        self.current_sprite = 0
        self.image = self.sprites_right[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.direction = 0

        self.rect.topleft = Player.frog_position

# Set color to be removed for each loaded image
        for i in range(len(self.sprites_right)):
            self.sprites_right[i].set_colorkey((0, 0, 0, 0))
    # Control the image size
            self.sprites_right[i] = pygame.transform.scale(self.sprites_right[i], (100, 100))

        for i in range(len(self.sprites_left)):
            self.sprites_left[i].set_colorkey((0, 0, 0, 0))
    # Control the image size
            self.sprites_left[i] = pygame.transform.scale(self.sprites_left[i], (100, 100))



       
    
    def move(self, dx, dy):
        self.frog_position[0] += dx  # Update x-coordinate
        self.frog_position[1] += dy  # Update y-coordinate
        self.rect.topleft = self.frog_position
    
    def turn_left(self):
        if self.frog_position[0] > 0:
         self.direction = -90
         self.frog_position[0] -= 10  # Move left by 10 units
        else:
        # Frog is at the left edge, cannot turn left
         pass
    
    def turn_right(self):
        if self.direction != 90:  # Frog is not currently facing right
            self.direction = 90  # Set direction to face right
            self.frog_position[0] += self.rect.width  # Move right 
        # Frog is already facing right, no action needed
        pass



    def animate(self):
        self.is_animating = True
    
    def update(self, speed=0.2):
        if self.is_animating:
            self.current_sprite += speed
        if self.current_sprite >= len(self.sprites_right):
            self.current_sprite = 0
            self.is_animating = False

        if self.direction >= 0:
             self.image = self.sprites_right[int(self.current_sprite)]
        else:
            self.image = self.sprites_left[int(self.current_sprite)]

        self.rect.topleft = self.frog_position

class Snake(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        self.is_animating = True
        self.sprites.append(pygame.image.load('Snake-right0.png').convert_alpha())
        self.sprites.append(pygame.image.load('Snake-right1.png').convert_alpha())
        self.sprites.append(pygame.image.load('Snake-right2.png').convert_alpha())
        self.sprites.append(pygame.image.load('Snake-right3.png').convert_alpha())
        self.sprites.append(pygame.image.load('Snake-right4.png').convert_alpha())
        self.sprites.append(pygame.image.load('Snake-right5.png').convert_alpha())
        self.sprites.append(pygame.image.load('Snake-left0.png').convert_alpha())
        self.sprites.append(pygame.image.load('Snake-left1.png').convert_alpha())
        self.sprites.append(pygame.image.load('Snake-left2.png').convert_alpha())
        self.sprites.append(pygame.image.load('Snake-left3.png').convert_alpha())
        self.sprites.append(pygame.image.load('Snake-left4.png').convert_alpha())
        self.sprites.append(pygame.image.load('Snake-left5.png').convert_alpha())
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
       
        self.speed = random.randrange(1, 8)

    def animate(self):
        self.is_animating = True

    def update(self, speed=0.1):
        if self.is_animating:
            self.current_sprite += speed
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
                self.is_animating = True

             

                self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
                self.rect.y = random.randrange(10, SCREEN_HEIGHT - self.rect.height)
                self.speed = random.randrange(1, 8)

            self.image = self.sprites[int(self.current_sprite)]
        else:
            self.rect.x += self.speed
            if self.rect.right > SCREEN_WIDTH:
                self.kill()  # Remove the snake if it reaches the right edge of the screen

class Gator(pygame.sprite.Sprite):
    gator_position = [70, 300]  # Initial position of the gator
    def __init__(self, pos_x, pos_y):
        super().__init__()
        
        self.sprites = []
        self.is_animating = True
        self.sprites.append(pygame.image.load('gator-right1.png').convert())
        self.sprites.append(pygame.image.load('gator-right2.png').convert())
        self.sprites.append(pygame.image.load('gator-right3.png').convert())
        self.sprites.append(pygame.image.load('gator-right4.png').convert())
        self.sprites.append(pygame.image.load('gator-left1.png').convert())
        self.sprites.append(pygame.image.load('gator-left2.png').convert())
        self.sprites.append(pygame.image.load('gator-left3.png').convert())
        self.sprites.append(pygame.image.load('gator-left4.png').convert())
      
       
# Set color to be removed for each loaded image
        for i in range(len(self.sprites)):
            self.sprites[i].set_colorkey((255, 255, 255))
            # Control the image size
            self.sprites[i] = pygame.transform.scale(self.sprites[i], (100, 100))
      

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
       
        self.speed = random.randrange(1, 8)
       

    def move(self, dx, dy):
       
        Gator.gator_position[0] += dx
        Gator.gator_position[1] += dy
        self.rect.topleft = Gator.gator_position

    def animate(self):
            self.is_animating = True


    def update(self, speed=0.1):
        if self.is_animating:
            self.current_sprite += speed
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
                self.is_animating = True

             

                self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
                self.rect.y = random.randrange(10, SCREEN_HEIGHT - self.rect.height)
                self.speed = random.randrange(1, 8)

            self.image = self.sprites[int(self.current_sprite)]
        else:
            self.rect.x += self.speed
            if self.rect.right > SCREEN_WIDTH:
                self.kill()  


pygame.init()
clock = pygame.time.Clock()

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Froggers')

background = pygame.image.load('bg.jpg').convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

all_sprites = pygame.sprite.Group()
player = Player(Player.frog_position[0], Player.frog_position[1])
snake = Snake(90, 200)
Alligator= Gator(90,100)

snake_timer = 0


all_sprites.add(player,snake,Alligator)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.turn_right()
                player.animate()
                player.move(10, 0)  # Move the frog 10 steps to the right
            if event.key == pygame.K_LEFT:
                
                player.turn_left()
                player.move(-10, 0)
                player.animate()

    
    screen.blit(background, (0, 0))

    all_sprites.update()

    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)
