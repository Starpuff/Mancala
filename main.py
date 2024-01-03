import pygame
import random

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

TRANSPARENT = (0, 0, 0, 0)

FONT = pygame.font.SysFont("Arial", 30)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mancala")


class Circle:
    radius = 53
    diameter = radius * 2
    outline_thickness = 7
    hover_outline_color = "white"

    def __init__(self, x, y, number):
        self.number = number
        self.x = x
        self.y = y
        self.pebbles = 4

    def get_surface(self):
        return pygame.Surface((self.diameter, self.diameter), pygame.SRCALPHA)

    def draw(self):
        pygame.draw.circle(self.get_surface(), TRANSPARENT, (self.radius, self.radius), self.radius)

    def is_hovered_over(self, mouse_pos):
        distance_from_center = ((self.x - mouse_pos[0]) ** 2 + (self.y - mouse_pos[1]) ** 2) ** 0.5
        return distance_from_center <= self.radius

    def draw_outline_hovered(self):
        pygame.draw.circle(screen, self.hover_outline_color, (self.x, self.y), 45 +
                           self.outline_thickness, self.outline_thickness)

    def get_number(self):
        return self.number

    def add_pebble(self):
        self.pebbles += 1

    def get_nr_of_pebbles(self):
        return self.pebbles

    def remove_pebbles(self):
        self.pebbles = 0


def get_background_image():
    background_image = pygame.image.load('Images/background.png').convert()
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    return background_image


def get_board():
    board_image = pygame.image.load('Images/mancala_board_blurred.png').convert_alpha()
    board_width = board_image.get_width() * 0.75
    board_height = board_image.get_height() * 0.75
    board_image = pygame.transform.scale(board_image, (int(board_width), int(board_height)))
    return board_image, board_width, board_height


def get_flags():
    num_flag_up = pygame.image.load('Images/number-flag-up.png').convert_alpha()
    num_flag_down = pygame.image.load('Images/number-flag-down.png').convert_alpha()
    player_one_flag = pygame.image.load('Images/player-one.png').convert_alpha()
    player_two_flag = pygame.image.load('Images/player-two.png').convert_alpha()
    return num_flag_up, num_flag_down, player_one_flag, player_two_flag


def make_circles():
    y1 = 287
    y2 = y1 + 150
    circ13 = Circle(326, y1, 13) # randul 1, primul cerc
    circ12 = Circle(453, y1, 12)
    circ11 = Circle(580, y1, 11)
    circ10 = Circle(706, y1, 10)
    circ9 = Circle(833, y1, 9)
    circ8 = Circle(960, y1, 8)
    circ1 = Circle(326, y2, 1)  # randul 2, primul cerc
    circ2 = Circle(453, y2, 2)
    circ3 = Circle(580, y2, 3)
    circ4 = Circle(706, y2, 4)
    circ5 = Circle(833, y2, 5)
    circ6 = Circle(960, y2, 6)
    circ0 = Circle(192, y1 + 50, 0)  # player 1 (stanga)
    circ7 = Circle(1092, y2 - 50, 7)  # player 2 (dreapta)
    return circ0, circ1, circ2, circ3, circ4, circ5, circ6, circ7, circ8, circ9, circ10, circ11, circ12, circ13


def draw_hovered_circles(circle_list, mouse_pos, num_flag_up, num_flag_down):
    for circle in circle_list:
        if circle.is_hovered_over(mouse_pos) and circle.get_number() is not 0 and circle.get_number() is not 7:
            circle.draw_outline_hovered()
            draw_nr_of_pebbles(circle_list, mouse_pos, num_flag_up, num_flag_down)


def draw_nr_of_pebbles(circle_list, mouse_pos, num_flag_up, num_flag_down):
    for circle in circle_list:
        if circle.is_hovered_over(mouse_pos):
            nr_of_pebbles = circle.get_nr_of_pebbles()
            rendered_number = FONT.render(str(nr_of_pebbles), True, "white")
            if 7 < circle.get_number() <= 13:
                screen.blit(num_flag_up,
                            (circle.x - num_flag_up.get_width() / 2, circle.y - 1.75 * num_flag_up.get_height()))
                screen.blit(rendered_number, (circle.x - 5, circle.y - 130))
            elif 0 < circle.get_number() <= 6:
                screen.blit(num_flag_down,
                            (circle.x - num_flag_down.get_width() / 2, circle.y + 1.5 * num_flag_down.get_height() / 2))
                screen.blit(rendered_number, (circle.x - 5, circle.y + 90))


def draw_player_flags(player_one_flag, player_two_flag, player_one_points, player_two_points):
    screen.blit(player_one_flag, (16, 250))
    render_player_one_points = FONT.render(str(player_one_points), True, "white")
    screen.blit(render_player_one_points, (90, 263))
    screen.blit(player_two_flag, (SCREEN_WIDTH - player_two_flag.get_width() - 16, 420))
    render_player_two_points = FONT.render(str(player_two_points), True, "white")
    screen.blit(render_player_two_points, (SCREEN_WIDTH - 100, 433))


def get_pebble_images():
    one_pebble = pygame.image.load('Images/1-pebble-heart.png').convert_alpha()
    two_pebbles = pygame.image.load('Images/2-pebbles.png').convert_alpha()
    three_pebbles = pygame.image.load('Images/3-pebbles.png').convert_alpha()
    return one_pebble, two_pebbles, three_pebbles


def draw_pebbles(circle_list):
    pebble_img_list = get_pebble_images()
    for circle in circle_list:
        nr_of_pebbles = circle.get_nr_of_pebbles()
        if nr_of_pebbles == 1:
            screen.blit(pebble_img_list[0], (circle.x - pebble_img_list[0].get_width() / 2, circle.y
                                             - pebble_img_list[0].get_height() / 2))
        elif nr_of_pebbles == 2:
            screen.blit(pebble_img_list[1], (circle.x - pebble_img_list[1].get_width() / 2, circle.y
                                             - pebble_img_list[1].get_height() / 2))
        elif nr_of_pebbles >= 3:
            screen.blit(pebble_img_list[2], (circle.x - pebble_img_list[2].get_width() / 2, circle.y
                                             - pebble_img_list[2].get_height() / 2))


def main():
    done = False
    board_image, board_width, board_height = get_board()
    background_image = get_background_image()
    num_flag_up, num_flag_down, player_one_flag, player_two_flag = get_flags()

    make_circles()
    circle_list = make_circles()
    circle_list[0].remove_pebbles()
    circle_list[7].remove_pebbles()

    # Testing input
    circle_list[1].remove_pebbles()
    circle_list[1].add_pebble()
    circle_list[2].remove_pebbles()
    circle_list[2].add_pebble()
    circle_list[2].add_pebble()

    # Done testing

    while not done:
        screen.blit(background_image, (0, 0))
        overlay_position = (SCREEN_WIDTH // 2 - board_image.get_width() // 2,
                            SCREEN_HEIGHT // 2 - board_image.get_height() // 2)
        screen.blit(board_image, overlay_position)
        mouse_pos = pygame.mouse.get_pos()

        draw_pebbles(circle_list)
        draw_player_flags(player_one_flag, player_two_flag, circle_list[0].get_nr_of_pebbles(),
                          circle_list[7].get_nr_of_pebbles())
        draw_hovered_circles(circle_list, mouse_pos, num_flag_up, num_flag_down)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for circle in circle_list:
                    if (circle.is_hovered_over(mouse_pos) and circle.get_number() is not 0
                            and circle.get_number() is not 7):
                        current_pebbles = circle.get_nr_of_pebbles()
                        circle.remove_pebbles()
                        i = 1
                        while current_pebbles > 0:
                            circle_list[(circle.get_number() + i) % 14].add_pebble()
                            current_pebbles -= 1
                            i += 1

        pygame.display.flip()


if __name__ == '__main__':
    main()
