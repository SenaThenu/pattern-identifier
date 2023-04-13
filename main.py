import pygame
import math
import ctypes
from os.path import join
pygame.init()

# Static Game Variables
WIDTH, HEIGHT = 600, 600
FPS = 30
WHITE = (174, 253, 202)
BLACK = (0, 0, 0)
MANU_COLOUR = (9, 189, 57)    # Color used to connect the user's dots
AI_COLOUR = (2, 121, 212)     # Color used to connect AI connected dots color
BUTTON_RADIUS = 25
CLICKED_DOTS = []
PREV_DOTS = []

SET_UP_MODE = False
AI_MODE = False

BG = pygame.image.load(join("assets", "bg.png"))

# Display Setup
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pattern Identifier")

# The purpose of this is generating all possible outcomes of the pattern for a given length. <start>


def select_non_repetitive(possibs, sample):
    different_values = len(set(sample))
    if different_values == len(sample):
        possibs.append(tuple(sample))


def generator(length):
    sample = [1 for i in range(length)]
    possibs = []
    all_nine = False
    while not all_nine:
        for i in range(length):
            next_index = i+1
            rest_values = sample[next_index:]
            if next_index == length:
                sample[i] += 1
                select_non_repetitive(possibs, sample)
            elif len(set(rest_values)) == 1 and rest_values[0] == 9:
                for x in range(len(sample)):
                    if x >= next_index:
                        sample[x] = 1
                sample[i] += 1
                select_non_repetitive(possibs, sample)
            else:
                pass

        # All nine validator
        if len(set(sample)) == 1 and sample[0] == 9:
            all_nine = True
    return possibs
# <end>


def generate_the_answer():
    """This generates the correct pattern number sequence and returns it!"""
    length = 0
    answer_found = False
    while not answer_found:
        global AI_MODE
        length += 1
        possibs = generator(length)
        for possib in possibs:
            if possib == tuple(CLICKED_DOTS):
                answer_found = True
                AI_MODE = False
                ai_draw(possib, wait=True)
                break
            else:
                ai_draw(possib, wait=False)


def generate_dot_set(WIN):
    dot_cors = []
    # Repeating through the 1/4s horizontally...
    for i in range(1, 4):
        cir_y = HEIGHT * (i/4)
        # Repeating through the 1/4s vertically...
        for x in range(1, 4):
            cir_x = WIDTH * (x/4)
            pygame.draw.circle(WIN, WHITE, (cir_x, cir_y), BUTTON_RADIUS)
            dot_cors.append([cir_x, cir_y])
    return dot_cors


def ai_draw(ai_answer, wait):
    WIN.blit(BG, (0, 0))

    # Setting up dots and tracking dot clicks
    dot_cors = generate_dot_set(WIN)

    connect_dots(dot_cors, ai_answer, AI_COLOUR)

    pygame.display.update()
    if wait:
        pygame.time.delay(1000)


def check_dot_click(mouse_pos, dot_cors):
    if mouse_pos != None:
        for i, cor in enumerate(dot_cors):
            hyp = math.sqrt(int(((cor[0]-mouse_pos[0]) ** 2) +
                                ((cor[1]-mouse_pos[1]) ** 2)))
            if hyp <= BUTTON_RADIUS:
                return i+1


def create_clicked_dots(pressed):
    if int(pressed) not in CLICKED_DOTS:
        CLICKED_DOTS.append(int(pressed))


# n means the position of the button from the left...
def button_prop_setter(button_name, n, button_width=144, button_gap=10):
    """This sets up the properties for a specific button, given its position from left. Afterwards, it blits it on to the screen."""
    button_width += button_gap
    but_img = pygame.image.load(
        join("assets", "Buttons", f"{button_name}.png"))
    but_x, but_y = WIDTH-(n * button_width), HEIGHT-but_img.get_height()
    WIN.blit(but_img, ((but_x), but_y))
    return [but_x, but_y, but_img.get_width(), but_img.get_height()]


def set_up_buttons():
    """This is where the buttons are mended and a list of button properties is returned!"""

    # This is the list for buttons containing global indexes. (Used in performing button funcs)
    if SET_UP_MODE:
        buttons = ["Done", "Cancel"]
    else:
        buttons = ["Setup_Button", "AI_Button"]
    button_prop_list = []

    for i, button in enumerate(buttons):
        props = button_prop_setter(button, (i+1))
        button_prop_list.append(props)
    return button_prop_list


def perform_button_funcs(button_status):
    """Makes the button perform its function"""

    for button in button_status:
        global SET_UP_MODE, CLICKED_DOTS, PREV_DOTS
        if not SET_UP_MODE:
            # 0 = Set up button, 1 = AI button (because the status dictionary is set up according to global indices.)
            if button_status.get(button) and button == 0:
                SET_UP_MODE = True
                PREV_DOTS = CLICKED_DOTS
                CLICKED_DOTS = []
            elif button_status.get(button) and button == 1:
                global AI_MODE
                if not AI_MODE:
                    if len(CLICKED_DOTS) > 0:
                        generate_the_answer()
                    else:
                        ctypes.windll.user32.MessageBoxW(
                            0, 'Set a pattern before running the identifier!', 'No Pattern Error', 48)
        else:
            # 0 = Done, 1 = Cancel
            if button_status.get(button) and button == 0:
                SET_UP_MODE = False
            elif button_status.get(button) and button == 1:
                CLICKED_DOTS = PREV_DOTS
                SET_UP_MODE = False


def check_button_click(button_props, mouse_pos):
    """Checks whether a particular button is clicked or not and if clicked, performs what it does."""
    button_status = {}
    if mouse_pos != None:
        for i, button in enumerate(button_props):
            button_x, button_y, button_width, button_height = button
            if mouse_pos[0] > button_x and mouse_pos[0] < (button_x+button_width):
                if mouse_pos[1] > button_y and mouse_pos[1] < (button_y+button_height):
                    button_status[i] = True
                else:
                    pass
    perform_button_funcs(button_status)


def connect_dots(dot_cors, dot_sequence, color):
    """This connects the clicked dots with lines"""
    for i, dot in enumerate(dot_sequence):
        if (i+1) != len(dot_sequence):
            nxt_dot_cor_index = dot_sequence[i+1] - 1
            pygame.draw.line(
                WIN, color, dot_cors[(dot-1)], dot_cors[nxt_dot_cor_index], 10)


def draw(WIN, mouse_pos):
    WIN.blit(BG, (0, 0))

    # Setting up dots and tracking dot clicks
    dot_cors = generate_dot_set(WIN)
    if SET_UP_MODE:
        global PREV_DOTS
        clicked_dot = check_dot_click(mouse_pos, dot_cors)
        if clicked_dot != None:
            create_clicked_dots(clicked_dot)
    connect_dots(dot_cors, CLICKED_DOTS, MANU_COLOUR)

    # Setting up buttons and tracking button clicks
    button_props = set_up_buttons()
    check_button_click(button_props, mouse_pos)
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        mouse_pos = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
        draw(WIN, mouse_pos)


if __name__ == "__main__":
    main()
