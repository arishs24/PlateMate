import pygame
import sys

# Initialize Pygame
pygame.init()

# Load the images
first_screen_image = pygame.image.load("image.png")
second_screen_image = pygame.image.load("image2.png")
third_screen_image = pygame.image.load("image3.png")
fourth_screen_image = pygame.image.load("image4.png")
fifth_screen_image = pygame.image.load("image5.png")
sixth_screen_image = pygame.image.load("image6.png")

# Set up the display
screen = pygame.display.set_mode((first_screen_image.get_width(), first_screen_image.get_height()))
pygame.display.set_caption("PlateMate App")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# Fonts
font = pygame.font.SysFont("Arial", 25)
small_font = pygame.font.SysFont("Arial", 20)

# Back button
back_button_rect = pygame.Rect(10, 10, 80, 40)
back_button_surface = pygame.Surface((80, 40))
back_button_surface.fill(GRAY)
pygame.draw.rect(back_button_surface, BLACK, pygame.Rect(0, 0, 80, 40), 2)
back_button_text = small_font.render("Back", True, BLACK)
back_button_surface.blit(back_button_text, (10, 10))

# Buttons for second screen
looking_to_cook_button_rect = pygame.Rect((screen.get_width() // 2) - 150, 450, 300, 50)
looking_to_eat_button_rect = pygame.Rect((screen.get_width() // 2) - 150, 510, 300, 50)

# Buttons for third screen
email_input_rect = pygame.Rect((screen.get_width() // 2) - 150, 379, 300, 40)
sign_up_with_email_button_rect = pygame.Rect((screen.get_width() // 2) - 150, 400, 300, 50)
google_button_rect = pygame.Rect((screen.get_width() // 2) - 150, 520, 300, 50)

# Upload ID button
upload_id_button_rect = pygame.Rect((screen.get_width() // 2) - 150, 393, 382, 50)

email_text = ""
email_input_active = False
input_color_inactive = pygame.Color("lightskyblue3")
input_color_active = pygame.Color("dodgerblue2")
input_color = input_color_inactive


def display_image(image, show_back_button=False):
    screen.blit(image, (0, 0))
    if show_back_button:
        screen.blit(back_button_surface, back_button_rect)


def popup_text(text):
    # Popup with "Signing in with Google"
    popup_surface = pygame.Surface((400, 100))
    popup_surface.fill(WHITE)
    text_surface = small_font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(200, 50))
    popup_surface.blit(text_surface, text_rect)
    screen.blit(popup_surface, (screen.get_width() // 2 - 200, screen.get_height() // 2 - 50))
    pygame.display.update()
    pygame.time.wait(2000)  # Pause for 2 seconds


def main():
    global email_text, email_input_active, input_color

    screen_number = 1  # 1 for the first screen, 2 for the second screen, 3 for the third screen, 4 for the fourth screen, 5 for the fifth screen, 6 for the sixth screen
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                print(f"Mouse clicked at: ({x}, {y})")

                # Handle clicking on input box
                if screen_number == 3:
                    if email_input_rect.collidepoint(event.pos):
                        email_input_active = not email_input_active
                    else:
                        email_input_active = False
                    input_color = input_color_active if email_input_active else input_color_inactive

                # Handle back button
                if back_button_rect.collidepoint(event.pos):
                    screen_number = screen_number - 1 if screen_number > 1 else 1
                else:
                    # Handle other clicks to go to the next screen
                    screen_number = min(screen_number + 1, 6)

                # Special handling for the third and fourth screens
                if screen_number == 3:  # On the third screen
                    if sign_up_with_email_button_rect.collidepoint(event.pos):
                        screen_number = 4
                    elif google_button_rect.collidepoint(event.pos):
                        popup_text("Signing in with Google...")
                        screen_number = 4
                elif screen_number == 4:  # On the fourth screen
                    if upload_id_button_rect.collidepoint(event.pos):
                        screen_number = 5

            elif event.type == pygame.KEYDOWN:
                if screen_number == 3 and email_input_active:
                    if event.key == pygame.K_BACKSPACE:
                        email_text = email_text[:-1]
                    else:
                        email_text += event.unicode

        # Display the appropriate screen
        if screen_number == 1:
            display_image(first_screen_image)
        elif screen_number == 2:
            display_image(second_screen_image, show_back_button=True)
        elif screen_number == 3:
            display_image(third_screen_image, show_back_button=True)
            # Render the email input box
            pygame.draw.rect(screen, input_color, email_input_rect, 2)
            text_surface = small_font.render(email_text, True, BLACK)
            screen.blit(text_surface, (email_input_rect.x + 5, email_input_rect.y + 5))
            email_input_rect.w = max(300, text_surface.get_width() + 10)
        elif screen_number == 4:
            display_image(fourth_screen_image, show_back_button=True)
        elif screen_number == 5:
            display_image(fifth_screen_image, show_back_button=True)
        elif screen_number == 6:
            display_image(sixth_screen_image, show_back_button=True)

        pygame.display.update()


if __name__ == "__main__":
    main()
