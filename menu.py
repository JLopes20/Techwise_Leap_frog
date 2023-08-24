import pygame
from pygame import mixer
pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("sounds/birds.mp3")
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.5)


screen_width = 1080
screen_height = 720

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Menu Screen")

# Define colors
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Stop music function
def stop_Music():
    pygame.mixer.music.stop()


# Function to draw the menu with the buttons
def draw_menu():
    font = pygame.font.Font('fonts/Lilita_One.ttf', 36)
    text = font.render("Leap Frog", True, BLACK)  # Black text
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

    # Draw the credits button
    credits_button_width, credits_button_height = 200, 50
    credits_button_x = screen_width // 2 - credits_button_width // 2
    credits_button_y = 500
    pygame.draw.rect(screen, BLACK, (credits_button_x, credits_button_y, credits_button_width, credits_button_height))
    credits_text = font.render("Credits", True, GREEN)
    screen.blit(credits_text, (credits_button_x + credits_button_width // 2 - credits_text.get_width() // 2, credits_button_y + credits_button_height // 2 - credits_text.get_height() // 2))


    pygame.display.flip()  # Update the display

# Function to draw the gameplay screen
def draw_gameplay_screen():
    screen.fill(BLACK)  # Fill the screen with black color
    pygame.display.flip()  # Update the display


# Function to handle button click events
def handle_button_click(mouse_pos):
    start_button_x = screen_width // 2 - 100
    start_button_y = 300
    start_button_width = 200
    start_button_height = 50

    quit_button_x = screen_width // 2 - 100
    quit_button_y = 400
    quit_button_width = 200
    quit_button_height = 50

    credits_button_x = screen_width // 2 - 100
    credits_button_y = 400
    credits_button_width = 200
    credits_button_height = 50

    is_mouse_over_start_button_x = start_button_x <= mouse_pos[0] <= start_button_x + start_button_width
    is_mouse_over_start_button_y = start_button_y <= mouse_pos[1] <= start_button_y + start_button_height

    if is_mouse_over_start_button_x and is_mouse_over_start_button_y:
        click_Sound = mixer.Sound('sounds/click.wav')
        click_Sound.play()
        stop_Music()

        # START GAME HERE
        return 1

    is_mouse_over_quit_button_x = quit_button_x <= mouse_pos[0] <= quit_button_x + quit_button_width
    is_mouse_over_quit_button_y = quit_button_y <= mouse_pos[1] <= quit_button_y + quit_button_height

    if is_mouse_over_quit_button_x and is_mouse_over_quit_button_y:
        pygame.quit()
        quit()

    # Check if the mouse is over the credits button
    is_mouse_over_credits_button_x = credits_button_x <= mouse_pos[0] <= credits_button_x + credits_button_width
    is_mouse_over_credits_button_y = credits_button_y <= mouse_pos[1] <= credits_button_y + credits_button_height

    if is_mouse_over_credits_button_x and is_mouse_over_credits_button_y:
        click_Sound = mixer.Sound('sounds/click.wav')
        click_Sound.play()
        
        # DISPLAY CREDITS HERE
        print("Credits button clicked")

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
                    user_choice = handle_button_click(pygame.mouse.get_pos())
                    if(user_choice == 1):
                        # User has pressed Start, start game
                        return
        draw_menu() #Puts background and text together

        pygame.display.flip()  # Update the display

    pygame.quit()


if __name__ == "__main__":
    main()