import pygame

pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mancala")

background_image = pygame.image.load('Images/background.png').convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

board_image = pygame.image.load('Images/mancala_board.png').convert_alpha()
board_width = board_image.get_width() * 0.75
board_height = board_image.get_height() * 0.75
board_image = pygame.transform.scale(board_image, (int(board_width), int(board_height)))
    
done = False

while not done:
    screen.blit(background_image, (0, 0))

    overlay_position = (SCREEN_WIDTH // 2 - board_image.get_width() // 2,
                        SCREEN_HEIGHT // 2 - board_image.get_height() // 2)
    screen.blit(board_image, overlay_position)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    pygame.display.flip()
