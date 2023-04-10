import pygame
import math
from os.path import join
pygame.init()

# Static Game Variables
WIDTH, HEIGHT = 600, 600
FPS = 30
WHITE = (225, 225, 225)
BLACK = (0, 0, 0)
RED = (225, 0, 0)
BLUE = (0, 0, 225)
BUTTON_RADIUS = 25
CLICKED_DOTS = []
SET_UP_MODE = False
AI_MODE = False
TOTAL_TRIES = 0

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
    answer = None
    while not answer_found:
        global AI_MODE
        length += 1
        possibs = generator(length)
        for possib in possibs:
            if possib == tuple(CLICKED_DOTS):
                answer = possib
                answer_found = True
                AI_MODE = False
                ai_draw(possib, wait=True)
                break
            else:
                ai_draw(possib, wait=False)
    return answer


def generate_dot_set(WIN):
    dot_cors = []
    # Repeating through the 1/4s horizontally...
    for i in range(1, 4):
        cir_y = HEIGHT * (i/4)
        # Repeating through the 1/4s vertically...
        for x in range(1, 4):
            cir_x = WIDTH * (x/4)
            pygame.draw.circle(WIN, BLACK, (cir_x, cir_y), BUTTON_RADIUS)
            dot_cors.append([cir_x, cir_y])
    return dot_cors


def ai_draw(ai_answer, wait):
    WIN.fill(WHITE)

    # Setting up dots and tracking dot clicks
    dot_cors = generate_dot_set(WIN)

    connect_dots(dot_cors, ai_answer, BLUE)

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
    buttons = ["Setup_Button", "AI_Button"]
    button_prop_list = []

    for i, button in enumerate(buttons):
        props = button_prop_setter(button, (i+1))
        button_prop_list.append(props)
    return button_prop_list


def perform_button_funcs(button_status):
    """Makes the button perform its function"""
    # 0 = Set up button, 1 = AI button (because the status dictionary is set up according to global indices.)
    for button in button_status:
        if button_status.get(button) and button == 0:
            global SET_UP_MODE, CLICKED_DOTS
            if SET_UP_MODE:
                SET_UP_MODE = False
            else:
                CLICKED_DOTS = []
                SET_UP_MODE = True
            break        # Disabling the AI mode!
        elif button_status.get(button) and button == 1:
            global AI_MODE
            if not AI_MODE:
                if not SET_UP_MODE and len(CLICKED_DOTS) > 0:
                    answer = generate_the_answer()

            else:
                AI_MODE = False


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
    WIN.fill(WHITE)

    # Setting up dots and tracking dot clicks
    dot_cors = generate_dot_set(WIN)
    if SET_UP_MODE:
        clicked_dot = check_dot_click(mouse_pos, dot_cors)
        if clicked_dot != None:
            create_clicked_dots(clicked_dot)
    connect_dots(dot_cors, CLICKED_DOTS, RED)

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
        if not AI_MODE:
            draw(WIN, mouse_pos)


if __name__ == "__main__":
    main()
