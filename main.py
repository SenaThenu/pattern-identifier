import pygame
from os.path import join
pygame.init()

# Static Game Variables
WIDTH, HEIGHT = 600, 600
FPS = 30
WHITE = (225, 225, 225)
BLACK = (0, 0, 0)
BUTTON_RADIUS = 25

# Display Setup
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pattern Identifier")


def generate_dot_set(win):
    # Repeating through the 1/4s horizontally...
    for i in range(1, 4):
        cir_y = HEIGHT * (i/4)
        # Repeating through the 1/4s vertically...
        for x in range(1, 4):
            cir_x = WIDTH * (x/4)
            pygame.draw.circle(win, BLACK, (cir_x, cir_y), BUTTON_RADIUS)


def check_click(buttons, mouse_pos, func="pressing"):
    for button in buttons:
        button_x, button_y, button_width, button_height = button
        if mouse_pos[0] > button_x and mouse_pos[0] < (button_x+button_width):
            if mouse_pos[1] > button_y and mouse_pos[1] < (button_y+button_height):
                print("Button was clicked!")
            else:
                pass


def draw(win):
    win.fill(WHITE)
    generate_dot_set(win)

    # The Setup Button
    set_up_button = pygame.image.load(join('assets', 'Setup_Button.png'))
    set_up_x, set_up_y = WIDTH-set_up_button.get_width(), HEIGHT - \
        set_up_button.get_height()
    win.blit(set_up_button, (set_up_x, set_up_y))

    buttons = [[set_up_x, set_up_y, set_up_button.get_width(),
                set_up_button.get_height()]]
    check_click(buttons, pygame.mouse.get_pos())
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw(win)


if __name__ == "__main__":
    main()
