# IMPORTS
# ------------------------------------------------------------------------
import pygame
import random
from Projects.Games.Tetris import sprites
from Projects.Games.Tetris import functions
#from . import sprites
#from . import functions
from functools import partial
from math import floor

pygame.init()
pygame.display.set_caption("Tetris")
gameIcon = pygame.image.load('Icon.png')
pygame.display.set_icon(gameIcon)

# AUDIO
# --------------------------------------------------------------------------
song = pygame.mixer.music.load('pymusic.mp3')
pygame.mixer.music.play(-1)

# GLOBAL VARIABLES
# --------------------------------------------------------------------------
screen_width = 620
screen_height = 701

x_grid_cords = [5, 48, 91, 134, 177, 220, 263, 306, 349, 392]
y_grid_cords = [-253, -210, -167, -124, -81, -38, 5, 48, 91, 134, 177, 220, 263, 306, 349, 392, 435, 478, 521, 564, 607, 650]

x_limits_dict_dict = {
    1: functions.L_x_limits_dict,
    2: functions.K_x_limits_dict,
    3: functions.S_x_limits_dict,
    4: functions.O_x_limits_dict,
    5: functions.Z_x_limits_dict,
    6: functions.I_x_limits_dict
}

movement_dict_dict = {
    1: functions.L_dict,
    2: functions.K_dict,
    3: functions.S_dict,
    4: functions.O_dict,
    5: functions.Z_dict,
    6: functions.I_dict
}

# BEGINNING INITIALIZATIONS
# -------------------------------------------------------------------------
sprite_status = "Dead"
sprite_nr = 0
x, y = 0, 0
vel = 1
delta_vel = 0
rotation = 0
color = (0, 0, 0)
movement_dict = functions.L_dict
x_limits_dict = functions.L_x_limits_dict
delay_r = 0
delay_l = 0
delay_rot = 0
delay_dropped = 0
delay_swap = 0
click1_delay = 0
click2_delay = 0
y_limit_array = [650, 650, 650, 650, 650, 650, 650, 650, 650, 650]
color_array = [[(0, 0, 0)] * 22 for _ in range(10)]
coord_array = [[(0, 0)] * 22 for _ in range(10)]
space_click = False
score = [0]
# Swap vars
block_bank = (0, 0)
block_bank_color = (0, 0, 0)
first_swap = True
first_game = True
# Rendering labels and images

score_text = pygame.font.SysFont("smallfonts", 50)
score_update = pygame.font.SysFont("smallfonts", 60)
instructions_text = pygame.font.SysFont("smallfonts", 30)


# RUNNING WINDOW
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
main_window = pygame.display.set_mode((screen_width, screen_height))

background = pygame.image.load('Tetris_bg.jpg').convert_alpha()


run = True
while run:
    pygame.time.delay(5)
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 448 <= mouse[0] <= 610 and 580 <= mouse[1] <= 680:
                functions.pause(main_window)

    main_window.fill((255, 255, 255))

    main_window.blit(background, (5, 5))

    pygame.draw.rect(main_window, (192, 192, 192), (443, 5, 172, 691))

    # Score Text

    text = score_text.render('Итог: ', True, (0, 0, 0))
    score_t = score_update.render(f'{score[0]}', True, (0, 0, 0))

    pygame.draw.rect(main_window, (0, 0, 0), (448, 50, 162, 60))
    pygame.draw.rect(main_window, (192, 192, 192), (452, 54, 154, 52))
    main_window.blit(text, (448, 10))
    main_window.blit(score_t, (456, 63))

    # Bank

    b_text = score_text.render("Банк:", True, (0, 0, 0))
    pygame.draw.rect(main_window, (0, 0, 0), (448, 170, 162, 220))
    pygame.draw.rect(main_window, (192, 192, 192), (452, 174, 154, 212))
    main_window.blit(b_text, (448, 130))

    # Instructions

    instructions_header = score_text.render("Кнопки:", True, (0, 0, 0))

    rotate_text = instructions_text.render("R - перевернуть", True, (0, 0, 0,))
    swap_text = instructions_text.render("S - подменить", True, (0, 0, 0,))
    move_text = instructions_text.render("< > - ходить", True, (0, 0, 0,))
    accelerate_text = instructions_text.render("_ - бегать", True, (0, 0, 0))

    main_window.blit(instructions_header, (448, 410))
    main_window.blit(rotate_text, (452, 450))
    main_window.blit(swap_text, (452, 475))
    main_window.blit(move_text, (452, 500))
    main_window.blit(accelerate_text, (452, 525))

    if first_game:
        run = functions.game_over(main_window, first_game)
        first_game = False

    if sprite_status == "Dead":
        # Defining parameters
        sprite_nr = random.randint(1, 6)
        y = -170
        rotation = random.randint(0, 3)
        color = (random.randint(20, 255), random.randint(20, 255), random.randint(20, 255))
        delay_dropped = 100

        x_limits_dict = x_limits_dict_dict[sprite_nr]
        movement_dict = movement_dict_dict[sprite_nr]

        x = x_grid_cords[random.randint(x_limits_dict[rotation][0], x_limits_dict[rotation][1])]
        sprite_status = "Falling"

    function_dict = {
        1: partial(sprites.L_block, main_window, x, y, color, rotation),
        2: partial(sprites.K_block, main_window, x, y, color, rotation),
        3: partial(sprites.S_block, main_window, x, y, color, rotation),
        4: partial(sprites.O_block, main_window, x, y, color, rotation),
        5: partial(sprites.Z_block, main_window, x, y, color, rotation),
        6: partial(sprites.I_block, main_window, x, y, color, rotation)
    }

    if not(functions.is_ok(x, y + vel, movement_dict[rotation], coord_array, x_grid_cords, y_grid_cords, sprite_status)):
        vel = 1

    if functions.is_ok(x, y, movement_dict[rotation], coord_array, x_grid_cords, y_grid_cords, sprite_status):
        sprite_status = "Falling"
        delay_dropped = 100
        y += vel
        vel = 1 + delta_vel

    function_dict[sprite_nr]()

    if not (functions.is_ok(x, y, movement_dict[rotation], coord_array, x_grid_cords, y_grid_cords, sprite_status)):

        if sprite_status == "Falling":
            sprite_status = "Dropped"

        if delay_dropped == 0:
            sprite_status = "Dead"
        else:
            delay_dropped -= 1

        # Setting color of block
        # -------------------------------------
        if sprite_status == "Dead":

            if y < 5:
                run = False

            if run is True:
                x_cord = x_grid_cords.index(x)
                y_cord = y_grid_cords.index(y)
                color_array[x_cord][y_cord] = color
                functions.set_array(x_cord, y_cord, color, color_array, movement_dict[rotation])
                functions.update_array(x, y, movement_dict[rotation], y_limit_array, x_grid_cords)
                functions.coordinate_array(coord_array, color_array, x_grid_cords, y_grid_cords)

    # CONTROLS
    # --------------

    keys = pygame.key.get_pressed()

    key_right_condition1 = keys[pygame.K_RIGHT] and x < x_grid_cords[x_limits_dict[rotation][1]] and delay_r == 0
    key_right_condition2 = functions.is_ok(x + 43, y, movement_dict[rotation], coord_array, x_grid_cords, y_grid_cords, sprite_status)
    key_right_condition3 = keys[pygame.K_RIGHT] and (sprite_status == "Dropped") and functions.is_ok_x(x + 43, y, movement_dict[rotation], coord_array, x_grid_cords, y_grid_cords, sprite_status) and delay_r == 0

    if key_right_condition1 and key_right_condition2 or key_right_condition3:
        x += 43
        delay_r = 20

    key_left_condition1 = keys[pygame.K_LEFT] and delay_l == 0 and (functions.is_ok(x - 43, y, movement_dict[rotation], coord_array, x_grid_cords, y_grid_cords, sprite_status))
    key_left_condition2 = keys[pygame.K_LEFT] and (sprite_status == "Dropped") and functions.is_ok_x(x - 43, y, movement_dict[rotation], coord_array, x_grid_cords, y_grid_cords, sprite_status) and delay_l == 0

    if key_left_condition1 or key_left_condition2:
        x -= 43
        delay_l = 20

    if keys[pygame.K_r] and delay_rot == 0 and functions.is_ok(x, y, movement_dict[(rotation+1) % 4], coord_array, x_grid_cords, y_grid_cords, sprite_status):
        rotation += 1
        rotation %= 4
        delay_rot = 35
    if keys[pygame.K_SPACE]:
        vel = 10

    if keys[pygame.K_s] and delay_swap == 0 and (sprite_status == "Falling"):
        if first_swap is True:
            block_bank = (sprite_nr, rotation)
            block_bank_color = color
            first_swap = False
            sprite_status = "Dead"

        else:
            if functions.is_ok(x, y, movement_dict_dict[block_bank[0]][block_bank[1]], coord_array, x_grid_cords, y_grid_cords, sprite_status) and \
                    functions.is_ok_x(x, y, movement_dict_dict[block_bank[0]][block_bank[1]], coord_array, x_grid_cords, y_grid_cords, sprite_status):
                block_temp = block_bank
                color_temp = block_bank_color

                block_bank = (sprite_nr, rotation)
                block_bank_color = color

                sprite_nr, rotation = block_temp
                color = color_temp

                x_limits_dict = x_limits_dict_dict[sprite_nr]
                movement_dict = movement_dict_dict[sprite_nr]

        delay_swap = 35

    if not first_swap:
        functions.bank_update(main_window, movement_dict_dict[block_bank[0]], block_bank_color, block_bank[0])

    if delay_l > 0:
        delay_l -= 1
    if delay_r > 0:
        delay_r -= 1
    if delay_rot > 0:
        delay_rot -= 1
    if delay_swap > 0:
        delay_swap -= 1

    # Pause Button

    pygame.draw.rect(main_window, (139, 0, 0), (448, 580, 162, 100))
    pygame.draw.rect(main_window, (255, 255, 153), (489, 590, 30, 80))
    pygame.draw.rect(main_window, (255, 255, 153), (539, 590, 30, 80))

    if 448 <= mouse[0] <= 610 and 580 <= mouse[1] <= 680:
        pygame.draw.rect(main_window, (110, 0, 0), (448, 580, 162, 100))
        pygame.draw.rect(main_window, (255, 255, 102), (489, 590, 30, 80))
        pygame.draw.rect(main_window, (255, 255, 102), (539, 590, 30, 80))

    # Difficulty Increase
    if delta_vel < 7:
        delta_vel = floor(score[0]/20)



# DELETING FULL ROWS
# --------------------------

    color_array = functions.delete_full_rows(color_array, score, 1)
    functions.coordinate_array(coord_array, color_array, x_grid_cords, y_grid_cords)

# DISPLAYING DEAD BLOCKS
# -------------------------------------------------------------
    for i, row in enumerate(color_array):
        for j, column in enumerate(row):
            if column != (0, 0, 0):
                sprites.building_block(main_window, x_grid_cords[i], y_grid_cords[j], color_array[i][j])

    if not run:
        run = functions.game_over(main_window, first_game)
        if run is True:
            color_array = [[(0, 0, 0)] * 22 for _ in range(10)]
            coord_array = [[(0, 0)] * 22 for _ in range(10)]
            score[0] = 0
            first_swap = True

    pygame.display.update()

pygame.quit()
