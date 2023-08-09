import pygame
from pygame import mixer
import subprocess #allows you to run other Python scripts. Needed to link to game when you click start button.
pygame.init()
pygame.mixer.init()

#Mp3 file
mp3_file = "sounds/background.mp3"
pygame.mixer.music.load(mp3_file)

#play the music
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.5)

#stop the music 
def stop_Music(): 
    pygame.mixer.music.stop()


screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Menu Screen")

# Define colors
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

#Background sound
mixer.music.load('sounds/Music4.mp3')
mixer.music.play()

# Function to draw the menu with the buttons
def draw_menu():
    #screen.fill(GREEN)  # Fill the screen with green color
    # change to correct path for font
    font = pygame.font.Font('fonts/Lilita_One.ttf', 36)
    text = font.render("Frogger", True, BLACK)  # Black text
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, 200))

    # Draw the start button
    start_button_width, start_button_height = 200, 50
    start_button_x = screen_width // 2 - start_button_width // 2
    start_button_y = 300
    pygame.draw.rect(screen, BLACK, (start_button_x, start_button_y, start_button_width, start_button_height))
    start_text = font.render("Start", True, GREEN)
    screen.blit(start_text, (start_button_x + start_button_width // 2 - start_text.get_width() // 2, start_button_y + start_button_height // 2 - start_text.get_height() // 2))

    # Draw the quit button
    quit_button_width, quit_button_height = 200, 50
    quit_button_x = screen_width // 2 - quit_button_width // 2
    quit_button_y = 400
    pygame.draw.rect(screen, BLACK, (quit_button_x, quit_button_y, quit_button_width, quit_button_height))
    quit_text = font.render("Quit", True, GREEN)
    screen.blit(quit_text, (quit_button_x + quit_button_width // 2 - quit_text.get_width() // 2, quit_button_y + quit_button_height // 2 - quit_text.get_height() // 2))

    pygame.display.flip()  # Update the display

# Function to draw the gameplay screen
def draw_gameplay_screen():
    screen.fill(BLACK)  # Fill the screen with black color
    pygame.display.flip()  # Update the display

# Function to handle button click events
def handle_button_click(mouse_pos):
    start_button_x, start_button_y, start_button_width, start_button_height = screen_width // 2 - 100, 300, 200, 50
    quit_button_x, quit_button_y, quit_button_width, quit_button_height = screen_width // 2 - 100, 400, 200, 50

    if start_button_x <= mouse_pos[0] <= start_button_x + start_button_width and start_button_y <= mouse_pos[1] <= start_button_y + start_button_height:
        click_Sound = mixer.Sound('sounds/click.wav')
        click_Sound.play()
        stop_Music()

        subprocess.Popen(["python3", "car moving1.py"])

        # switch to the gameplay screen
        run_gameplay_screen()
    elif quit_button_x <= mouse_pos[0] <= quit_button_x + quit_button_width and quit_button_y <= mouse_pos[1] <= quit_button_y + quit_button_height:
        pygame.quit()
        quit()

# Function to run the gameplay screen
def run_gameplay_screen():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        draw_gameplay_screen()

        pygame.display.flip()  # Update the display
    return running

def background_image():
    
    # Load the background image
    background_image = pygame.image.load('Images/menu-background2.jpg') 

    # Get the size of the background image
    image_width, image_height = background_image.get_size()

    # Calculate the scaling factors to fit the window size
    scale_width = screen_width / image_width
    scale_height = screen_height / image_height
    scale_factor = min(scale_width, scale_height)

    # Scale the background image to fit the window
    scaled_width = int(image_width * scale_factor)
    scaled_height = int(image_height * scale_factor)
    background_image = pygame.transform.scale(background_image, (scaled_width, scaled_height))

    # Calculate the position to center the image
    center_x = screen_width // 2 - scaled_width // 2
    center_y = screen_height // 2 - scaled_height // 2

    # Resize the background image to fit the screen
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    # Blit the background image on the screen
    screen.blit(background_image, (0, 0))

    pygame.display.flip()  # Update the display

def main():
    running = True
    background_image()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    handle_button_click(pygame.mouse.get_pos())
        draw_menu() #Puts background and text together

        pygame.display.flip()  # Update the display

    pygame.quit()

    

if __name__ == "__main__":
    main()

