"""
############################################################
#                                                          #
#         rifkys SnakeGame Fixed V2 [20/12/2024]           #
#                                                          #
#   This game is a simple implementation of the classic    #
#   Snake game using the Pygame library. The player wins   #
#   by eating a specified number of foods.                 #
#                                                          #
#   Features:                                              #
#   - Controls: Arrow keys or W, A, S, D.                  #
#                                                          #
#   [Additional information or license details]:           #
#   - Added Restart and Exit Buttons.                      #                                                      
############################################################
"""

import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')

# Clock
clock = pygame.time.Clock()

# Snake properties
snake_pos = [[100, 50], [90, 50], [80, 50]]
snake_speed = [10, 0]
snake_size = 10

# Food properties
food_pos = [random.randrange(1, (SCREEN_WIDTH//10)) * 10, random.randrange(1, (SCREEN_HEIGHT//10)) * 10]
food_spawn = True

# Score
score = 0
win_score = 10  # Default win score

# Font
font = pygame.font.SysFont(None, 35)

# Text input variables
input_active = True
user_input = ''
input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_active

def game_over():
    print("You Lose")
    return False

def show_score():
    score_text = font.render(f'Score: {score} / {win_score}', True, BLACK)
    screen.blit(score_text, (10, 10))

def show_win():
    win_text = font.render('You Win!', True, BLACK)
    screen.blit(win_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 18))

def draw_input_box():
    txt_surface = font.render(user_input, True, BLACK)
    pygame.draw.rect(screen, color, input_box)
    pygame.draw.rect(screen, BLACK, input_box, 2, border_radius=5)
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

# Main game loop
running = True
game_won = False
keys_pressed = {'w': False, 'a': False, 's': False, 'd': False}
direction = 'RIGHT'  # Starting direction
change_to = direction
game_over_screen = False
turn_made = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if input_active:
                if event.unicode.isdigit():
                    user_input += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key == pygame.K_RETURN:
                    win_score = int(user_input)
                    input_active = False
                    user_input = ''
            else:
                if event.key == pygame.K_w:
                    change_to = 'UP'
                    turn_made = True
                if event.key == pygame.K_a:
                    change_to = 'LEFT'
                    turn_made = True
                if event.key == pygame.K_s:
                    change_to = 'DOWN'
                    turn_made = True
                if event.key == pygame.K_d:
                    change_to = 'RIGHT'
                    turn_made = True

    if input_active:
        # Draw the input box and prompt the user to enter the score
        screen.fill(WHITE)
        prompt_text = font.render("Enter the minimum score to win:", True, BLACK)
        text_rect = prompt_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 75))
        screen.blit(prompt_text, text_rect)
        draw_input_box()
    elif game_over_screen:
        # Draw game over screen
        screen.fill(WHITE)
        game_over_text = font.render("Game Over!", True, BLACK)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(game_over_text, text_rect)

        # Draw restart and exit buttons
        button_width = 150
        button_height = 50
        button_gap = 20
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        button_y = SCREEN_HEIGHT // 2 + 50
        restart_button = pygame.Rect(button_x, button_y, button_width, button_height)
        exit_button = pygame.Rect(button_x, button_y + button_height + button_gap, button_width, button_height)

        pygame.draw.rect(screen, BLACK, restart_button, border_radius=10)
        pygame.draw.rect(screen, BLACK, exit_button, border_radius=10)

        restart_text = font.render('Restart', True, WHITE)
        exit_text = font.render('Exit', True, WHITE)

        restart_text_rect = restart_text.get_rect(center=restart_button.center)
        exit_text_rect = exit_text.get_rect(center=exit_button.center)

        screen.blit(restart_text, restart_text_rect)
        screen.blit(exit_text, exit_text_rect)

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Check if the user clicked on the restart button
        if restart_button.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                # Restart the game
                game_over_screen = False
                running = True
                score = 0
                snake_pos = [[100, 50], [90, 50], [80, 50]]
                snake_speed = [10, 0]
                direction = 'RIGHT'

        # Check if the user clicked on the exit button
        if exit_button.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                # Exit the game
                running = False
    elif game_won:
        # Draw win screen
        screen.fill(WHITE)
        win_text = font.render("You Win!", True, BLACK)
        text_rect = win_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(win_text, text_rect)

        # Draw restart and exit buttons
        button_width = 150
        button_height = 50
        button_gap = 20
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        button_y = SCREEN_HEIGHT // 2 + 50
        restart_button = pygame.Rect(button_x, button_y, button_width, button_height)
        exit_button = pygame.Rect(button_x, button_y + button_height + button_gap, button_width, button_height)

        pygame.draw.rect(screen, BLACK, restart_button, border_radius=10)
        pygame.draw.rect(screen, BLACK, exit_button, border_radius=10)

        restart_text = font.render('Restart', True, WHITE)
        exit_text = font.render('Exit', True, WHITE)

        restart_text_rect = restart_text.get_rect(center=restart_button.center)
        exit_text_rect = exit_text.get_rect(center=exit_button.center)

        screen.blit(restart_text, restart_text_rect)
        screen.blit(exit_text, exit_text_rect)

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Check if the user clicked on the restart button
        if restart_button.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                # Restart the game
                game_won = False
                score = 0
                snake_pos = [[100, 50], [90, 50], [80, 50]]
                snake_speed = [10, 0]
                direction = 'RIGHT'

        # Check if the user clicked on the exit button
        if exit_button.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                # Exit the game
                running = False
    else:
        # Validate the direction change
        if change_to == 'UP' and direction!= 'DOWN':
            direction = 'UP'
            turn_made = True
        if change_to == 'LEFT' and direction!= 'RIGHT':
            direction = 'LEFT'
            turn_made = True
        if change_to == 'DOWN' and direction!= 'UP':
            direction = 'DOWN'
            turn_made = True
        if change_to == 'RIGHT' and direction!= 'LEFT':
            direction = 'RIGHT'
            turn_made = True

        # Move the snake
        if direction == 'UP':
            snake_speed = [0, -10]
        if direction == 'LEFT':
            snake_speed = [-10, 0]
        if direction == 'DOWN':
            snake_speed = [0, 10]
        if direction == 'RIGHT':
            snake_speed = [10, 0]

        snake_pos.insert(0, list(map(sum, zip(snake_pos[0], snake_speed))))

        # Check if the snake has eaten the food
        if snake_pos[0] == food_pos:
            score += 1
            food_spawn = False
        else:
            if len(snake_pos) > score + 1:
                snake_pos.pop()

        # Spawn new food
        if not food_spawn:
            food_pos = [random.randrange(1, (SCREEN_WIDTH//10)) * 10, random.randrange(1, (SCREEN_HEIGHT//10)) * 10]
            food_spawn = True

        # Check for win condition
        if score >= win_score:
            game_won = True

        # Check for collisions
        if (snake_pos[0][0] < 0 or snake_pos[0][0] >= SCREEN_WIDTH or
            snake_pos[0][1] < 0 or snake_pos[0][1] >= SCREEN_HEIGHT or
            (snake_pos[0] in snake_pos[1:])):
            game_over_screen = True

        # Draw background
        screen.fill(WHITE)

        # Draw snake
        for pos in snake_pos:
            pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], snake_size, snake_size))

        # Draw food
        pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], snake_size, snake_size))

        # Show score
        show_score()

        # Reset turn_made after a frame
        turn_made = False

    # Update the display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(15)

# Exit the game
pygame.quit()
sys.exit()
