import pygame

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

TRANSPARENT = (0, 0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mancala")


class Circle:
    radius = 45
    diameter = radius * 2
    outline_thickness = 5
    hover_outline_color = "white"

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_surface(self):
        return pygame.Surface((self.diameter, self.diameter), pygame.SRCALPHA)

    def draw(self):
        pygame.draw.circle(self.get_surface(), TRANSPARENT, (self.radius, self.radius), self.radius)

    def is_hovered_over(self, mouse_pos):
        return self.get_surface().get_rect(center=(self.x, self.y)).collidepoint(mouse_pos)

    def draw_outline_hovered(self):
        pygame.draw.circle(screen, self.hover_outline_color, (self.x, self.y), 45 +
                           self.outline_thickness, self.outline_thickness)


def get_background_image():
    background_image = pygame.image.load('Images/background.png').convert()
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    return background_image


def get_board():
    board_image = pygame.image.load('Images/mancala_board.png').convert_alpha()
    board_width = board_image.get_width() * 0.75
    board_height = board_image.get_height() * 0.75
    board_image = pygame.transform.scale(board_image, (int(board_width), int(board_height)))
    return board_image, board_width, board_height


def main():
    done = False
    board_image, board_width, board_height = get_board()
    background_image = get_background_image()
    circ_starting_x = 326
    circ_starting_y = 287
    circ1 = Circle(circ_starting_x, circ_starting_y)

    while not done:
        screen.blit(background_image, (0, 0))
        overlay_position = (SCREEN_WIDTH // 2 - board_image.get_width() // 2,
                            SCREEN_HEIGHT // 2 - board_image.get_height() // 2)
        screen.blit(board_image, overlay_position)
        mouse_pos = pygame.mouse.get_pos()

        if circ1.is_hovered_over(mouse_pos):
            circ1.draw_outline_hovered()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        pygame.display.flip()


if __name__ == '__main__':
    main()
