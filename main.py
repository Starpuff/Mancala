import pygame

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

TRANSPARENT = (0, 0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mancala")


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


def draw_holes():
    circle_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
    pygame.draw.circle(circle_surface, TRANSPARENT, (50, 50), 50)
    return circle_surface


def main():
    done = False
    hover = False
    hover_outline_color = "white"
    outline_thickness = 5
    board_image, board_width, board_height = get_board()
    background_image = get_background_image()
    circle_surface = draw_holes()

    while not done:
        screen.blit(background_image, (0, 0))
        overlay_position = (SCREEN_WIDTH // 2 - board_image.get_width() // 2,
                            SCREEN_HEIGHT // 2 - board_image.get_height() // 2)
        screen.blit(board_image, overlay_position)
        mouse_pos = pygame.mouse.get_pos()

        if circle_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)).collidepoint(mouse_pos):
            hovered = True
        else:
            hovered = False

        if hovered:
            pygame.draw.circle(screen, hover_outline_color, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 50 +
                               outline_thickness, outline_thickness)
        else:
            screen.blit(circle_surface, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        pygame.display.flip()


if __name__ == '__main__':
    main()
