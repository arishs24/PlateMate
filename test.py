import pygame
import sys
import sqlite3
from pygame.locals import *

pygame.init()

# Initialize SQLite database
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE meals (id INTEGER PRIMARY KEY, provider TEXT, meal TEXT, dietary_restriction TEXT, time TEXT)
''')
conn.commit()

# Colors and Fonts
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
font = pygame.font.SysFont("Arial", 30)

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Feed & Earn")

# User roles
roles = ["Food Provider", "Homeless Person"]
current_role = None

# Input boxes
input_box_meal = pygame.Rect(200, 150, 400, 50)
input_box_diet = pygame.Rect(200, 250, 400, 50)
input_box_time = pygame.Rect(200, 350, 400, 50)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
input_boxes = [input_box_meal, input_box_diet, input_box_time]
active_boxes = [False, False, False]
text_inputs = ["", "", ""]

# Button
submit_button = pygame.Rect(300, 450, 200, 50)

def draw_text_centered(text, rect, color=BLACK):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def display_role_selection():
    screen.fill(WHITE)
    y_pos = 100
    for role in roles:
        role_button = pygame.Rect((screen_width / 2 - 200 / 2, y_pos), (200, 50))
        pygame.draw.rect(screen, BLUE, role_button)
        draw_text_centered(role, role_button)
        y_pos += 100
    pygame.display.flip()

def display_meal_posting_form():
    screen.fill(WHITE)
    screen.blit(font.render("Meal", True, BLACK), (100, 160))
    screen.blit(font.render("Dietary Restriction", True, BLACK), (100, 260))
    screen.blit(font.render("Available Time", True, BLACK), (100, 360))
    for i, box in enumerate(input_boxes):
        color = color_active if active_boxes[i] else color_inactive
        pygame.draw.rect(screen, color, box)
        txt_surface = font.render(text_inputs[i], True, BLACK)
        screen.blit(txt_surface, (box.x + 5, box.y + 5))
        pygame.draw.rect(screen, BLACK, box, 2)
    pygame.draw.rect(screen, RED, submit_button)
    draw_text_centered("Submit", submit_button)
    pygame.display.flip()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_role is None:
                # Role selection
                if pygame.Rect((screen_width / 2 - 200 / 2, 100), (200, 50)).collidepoint(event.pos):
                    current_role = "Food Provider"
                elif pygame.Rect((screen_width / 2 - 200 / 2, 200), (200, 50)).collidepoint(event.pos):
                    current_role = "Homeless Person"
            else:
                # Meal posting
                for i, box in enumerate(input_boxes):
                    active_boxes[i] = box.collidepoint(event.pos)
                if submit_button.collidepoint(event.pos) and current_role == "Food Provider":
                    provider = "Test Provider"
                    meal = text_inputs[0]
                    dietary_restriction = text_inputs[1]
                    time = text_inputs[2]
                    cursor.execute('''
                        INSERT INTO meals (provider, meal, dietary_restriction, time)
                        VALUES (?, ?, ?, ?)''', (provider, meal, dietary_restriction, time))
                    conn.commit()
                    print(f"Inserted meal: {meal}")
                    text_inputs = ["", "", ""]

        elif event.type == pygame.KEYDOWN:
            for i, active in enumerate(active_boxes):
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        text_inputs[i] = text_inputs[i][:-1]
                    else:
                        text_inputs[i] += event.unicode

    # Display
    if current_role is None:
        display_role_selection()
    else:
        display_meal_posting_form()

pygame.quit()
sys.exit()
