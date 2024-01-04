import pygame
import random

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

TRANSPARENT = (0, 0, 0, 0)

# FONT = pygame.font.SysFont("Arial", 30)
FONT = pygame.font.Font('Fonts/LEMONMILK-Medium.otf', 30)
BOLD_FONT = pygame.font.Font('Fonts/Unigeo64-Bold-trial.ttf', 30)

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

    def add_n_pebbles(self, n):
        self.pebbles += n

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


def draw_hovered_circles(circle_list, mouse_pos, num_flag_up, num_flag_down, player_turn):
    for circle in circle_list:
        if circle.is_hovered_over(mouse_pos):
            if player_turn == 1 and circle.get_number() > 7:
                circle.draw_outline_hovered()
                draw_nr_of_pebbles_flags(circle_list, mouse_pos, num_flag_up, num_flag_down)
            elif player_turn == 2 and 0 < circle.get_number() <= 6:
                circle.draw_outline_hovered()
                draw_nr_of_pebbles_flags(circle_list, mouse_pos, num_flag_up, num_flag_down)


def draw_flag_numbers(circle, nr_of_pebbles, rendered_number):
    y_addition = 90
    if 7 < circle.get_number() <= 13:
        y_addition = -130
    screen.blit(rendered_number, (circle.x - rendered_number.get_width() / 2, circle.y + y_addition))


def draw_nr_of_pebbles_flags(circle_list, mouse_pos, num_flag_up, num_flag_down):
    for circle in circle_list:
        nr_of_pebbles = circle.get_nr_of_pebbles()
        rendered_number = FONT.render(str(nr_of_pebbles), True, "white")
        if circle.is_hovered_over(mouse_pos):
            if 7 < circle.get_number() <= 13:
                screen.blit(num_flag_up, (circle.x - num_flag_up.get_width() / 2,
                                          circle.y - 1.75 * num_flag_up.get_height()))
                draw_flag_numbers(circle, nr_of_pebbles, rendered_number)
            elif 0 < circle.get_number() <= 6:
                screen.blit(num_flag_down, (circle.x - num_flag_down.get_width() / 2,
                                            circle.y + 1.5 * num_flag_down.get_height() / 2))
                draw_flag_numbers(circle, nr_of_pebbles, rendered_number)


def draw_opponent_flags(circle_list, num_flag_up, num_flag_down, player_turn):
    for circle in circle_list:
        nr_of_pebbles = circle.get_nr_of_pebbles()
        rendered_number = FONT.render(str(nr_of_pebbles), True, "white")
        if player_turn == 1 and 0 < circle.get_number() <= 6:
            screen.blit(num_flag_down,
                        (circle.x - num_flag_down.get_width() / 2, circle.y + 1.5 * num_flag_down.get_height() / 2))
            draw_flag_numbers(circle, nr_of_pebbles, rendered_number)
        elif player_turn == 2 and 7 < circle.get_number() <= 13:
            screen.blit(num_flag_up,
                        (circle.x - num_flag_up.get_width() / 2, circle.y - 1.75 * num_flag_up.get_height()))
            draw_flag_numbers(circle, nr_of_pebbles, rendered_number)


def draw_player_flags(player_one_flag, player_two_flag, player_one_points, player_two_points):
    screen.blit(player_one_flag, (16, 250))
    render_player_one_points = FONT.render(str(player_one_points), True, "white")
    if player_one_points > 9:
        screen.blit(render_player_one_points, (68, 263))
    else:
        screen.blit(render_player_one_points, (80, 263))
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


def circle_is_clicked(circle_list, mouse_pos, player_turn):
    for circle in circle_list:
        if circle.is_hovered_over(mouse_pos) and ((player_turn == 1 and 7 < circle.get_number() <= 13) or
                                                  (player_turn == 2 and 0 < circle.get_number() <= 6)):
            current_pebbles = circle.get_nr_of_pebbles()
            circle.remove_pebbles()
            i = 1
            if current_pebbles == 0:
                return player_turn
            while current_pebbles > 0:
                if player_turn == 1 and (circle.get_number() + i) % 14 == 7:
                    i += 1
                elif player_turn == 2 and (circle.get_number() + i) % 14 == 0:
                    i += 1
                last_circle = circle_list[(circle.get_number() + i) % 14]
                last_circle.add_pebble()
                current_pebbles -= 1
                i += 1
            new_player_turn = last_circle_handling(last_circle, circle_list, player_turn)
            return new_player_turn
    return 0


def last_circle_handling(last_circle, circle_list, player_turn):
    if last_circle.get_number() == 0 and player_turn == 1:
        new_player_turn = 1
    elif last_circle.get_number() == 7 and player_turn == 2:
        new_player_turn = 2
    elif last_circle.get_nr_of_pebbles() == 1:
        if player_turn == 1 and 7 < last_circle.get_number() <= 13:
            opposite_circle = circle_list[14 - last_circle.get_number()]
            circle_list[0].add_n_pebbles(opposite_circle.get_nr_of_pebbles() + 1)
            last_circle.remove_pebbles()
            opposite_circle.remove_pebbles()
            new_player_turn = 2
        elif player_turn == 2 and 0 < last_circle.get_number() <= 6:
            opposite_circle = circle_list[14 - last_circle.get_number()]
            circle_list[7].add_n_pebbles(opposite_circle.get_nr_of_pebbles() + 1)
            last_circle.remove_pebbles()
            opposite_circle.remove_pebbles()
            new_player_turn = 1
        else:
            new_player_turn = 3 - player_turn
    else:
        new_player_turn = 3 - player_turn
    return new_player_turn


def load_player_turn_images(pvp):
    if pvp:
        player_one_turn = pygame.image.load('Images/player-one-turn.png').convert_alpha()
        player_two_turn = pygame.image.load('Images/player-two-turn.png').convert_alpha()
    else:
        player_one_turn = pygame.image.load('Images/bot-turn.png').convert_alpha()
        player_two_turn = pygame.image.load('Images/your-turn.png').convert_alpha()
    return player_one_turn, player_two_turn


def load_player_turn_highlights():
    player_one_highlight = pygame.image.load('Images/player-one-highlight.png').convert_alpha()
    player_two_highlight = pygame.image.load('Images/player-two-highlight.png').convert_alpha()
    highlight_width = player_one_highlight.get_width() * 0.75
    highlight_height = player_one_highlight.get_height() * 0.75
    player_one_highlight = pygame.transform.scale(player_one_highlight, (int(highlight_width), int(highlight_height)))
    player_two_highlight = pygame.transform.scale(player_two_highlight, (int(highlight_width), int(highlight_height)))
    return player_one_highlight, player_two_highlight


def draw_player_turn(player_turn, player_turn_images, player_turn_highlights, pvp):
    draw_hint(player_turn, pvp)
    if player_turn == 1:
        screen.blit(player_turn_images[0], (SCREEN_WIDTH // 2 - player_turn_images[0].get_width() // 2, 0))
        screen.blit(player_turn_highlights[0], (SCREEN_WIDTH // 2 - player_turn_highlights[0].get_width() // 2,
                                                SCREEN_HEIGHT // 2 - player_turn_highlights[0].get_height() // 2))
    elif player_turn == 2:
        screen.blit(player_turn_images[1], (SCREEN_WIDTH // 2 - player_turn_images[1].get_width() // 2, 0))
        screen.blit(player_turn_highlights[1], (SCREEN_WIDTH // 2 - player_turn_highlights[1].get_width() // 2,
                                                SCREEN_HEIGHT // 2 - player_turn_highlights[1].get_height() // 2))


def draw_hint(player_turn, pvp):
    if player_turn == 1 and pvp is True:
        hint = "Player I : Select a circle from the top row"
    else:
        hint = "Player II : Select a circle from the bottom row"
    rendered_hint = BOLD_FONT.render(hint, True, "white")
    screen.blit(rendered_hint, (SCREEN_WIDTH // 2 - rendered_hint.get_width() // 2,
                                SCREEN_HEIGHT - rendered_hint.get_height() - 15))


def main():
    done = False
    pvp = True
    player_turn_images = load_player_turn_images(pvp)
    player_turn_highlights = load_player_turn_highlights()

    board_image, board_width, board_height = get_board()
    background_image = get_background_image()
    num_flag_up, num_flag_down, player_one_flag, player_two_flag = get_flags()

    make_circles()
    circle_list = make_circles()
    circle_list[0].remove_pebbles()
    circle_list[7].remove_pebbles()

    player_turn = random.randint(1, 2)

    # Testing
    # circle_list[10].add_n_pebbles(12)
    # circle_list[4].add_n_pebbles(12)
    # circle_list[0].add_n_pebbles(12)
    # circle_list[1].remove_pebbles()
    # circle_list[1].add_pebble()
    # circle_list[2].remove_pebbles()
    # circle_list[2].add_pebble()
    # circle_list[2].add_pebble()

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
        draw_hovered_circles(circle_list, mouse_pos, num_flag_up, num_flag_down, player_turn)
        draw_opponent_flags(circle_list, num_flag_up, num_flag_down, player_turn)

        draw_player_turn(player_turn, player_turn_images, player_turn_highlights, pvp)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                new_player_turn = circle_is_clicked(circle_list, mouse_pos, player_turn)
                if new_player_turn != 0:
                    player_turn = new_player_turn

        pygame.display.flip()


if __name__ == '__main__':
    main()
