import pygame
import math
from os.path import join
pygame.init()

# Static Game Variables
WIDTH, HEIGHT = 600, 600
FPS = 30
WHITE = (225, 225, 225)
BLACK = (0, 0, 0)
BUTTON_RADIUS = 25
CLICKED_DOTS = []
SET_UP_MODE = False
TRYING_MODE = False
TOTAL_TRIES = 0

# Display Setup
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pattern Identifier")


def generate_the_answer():
    # Run only if SET_UP_MODE is False and len(CLICKED DOTS) > 0
    pass


def generate_dot_set(win):
    dot_cors = []
    # Repeating through the 1/4s horizontally...
    for i in range(1, 4):
        cir_y = HEIGHT * (i/4)
        # Repeating through the 1/4s vertically...
        for x in range(1, 4):
            cir_x = WIDTH * (x/4)
            pygame.draw.circle(win, BLACK, (cir_x, cir_y), BUTTON_RADIUS)
            dot_cors.append([cir_x, cir_y])
    return dot_cors


def check_dot_click(mouse_pos, dot_cors):
    if mouse_pos != None:
        for i, cor in enumerate(dot_cors):
            hyp = math.sqrt(int(((cor[0]-mouse_pos[0]) ** 2) +
                                ((cor[1]-mouse_pos[1]) ** 2)))
            if hyp <= BUTTON_RADIUS:
                return i+1


def create_clicked_dots(pressed):
    CLICKED_DOTS.append(int(pressed))


def set_up_buttons():
    # Setting up the set-up button which lets the user to enter a new pattern
    set_up_button = pygame.image.load(join('assets', 'Setup_Button.png'))
    set_up_x, set_up_y = WIDTH-set_up_button.get_width(), HEIGHT - \
        set_up_button.get_height()
    win.blit(set_up_button, (set_up_x, set_up_y))

    button_props = [[set_up_x, set_up_y, set_up_button.get_width(),
                     set_up_button.get_height()]]
    # Here, button_props's index is used as the index keyword of the button_status dictionary
    return button_props


def perform_button_funcs(button_status):
    # button = 0; set-up-button
    for button in button_status:
        if button_status.get(button) and button == 0:
            global SET_UP_MODE, CLICKED_DOTS
            if SET_UP_MODE:
                SET_UP_MODE = False
            else:
                CLICKED_DOTS = []
                SET_UP_MODE = True


def check_button_click(button_props, mouse_pos):
    button_status = {

    }
    if mouse_pos != None:
        for i, button in enumerate(button_props):
            button_x, button_y, button_width, button_height = button
            if mouse_pos[0] > button_x and mouse_pos[0] < (button_x+button_width):
                if mouse_pos[1] > button_y and mouse_pos[1] < (button_y+button_height):
                    button_status[i] = True
                else:
                    pass
    perform_button_funcs(button_status)


def draw(win, mouse_pos):
    win.fill(WHITE)

    # Setting up dots and tracking dot clicks
    dot_cors = generate_dot_set(win)
    if SET_UP_MODE:
        clicked_dot = check_dot_click(mouse_pos, dot_cors)
        if clicked_dot != None:
            create_clicked_dots(clicked_dot)

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
        draw(win, mouse_pos)


if __name__ == "__main__":
    main()
