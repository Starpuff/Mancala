import pygame
import random

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

TRANSPARENT = (0, 0, 0, 0)

# FONT = pygame.font.SysFont("Arial", 30)
FONT = pygame.font.Font('Fonts/LEMONMILK-Medium.otf', 30)
MEDIUM_FONT = pygame.font.Font('Fonts/LEMONMILK-Regular.otf', 30)
BOLD_FONT = pygame.font.Font('Fonts/Unigeo64-Bold-trial.ttf', 30)
WINNER_FONT = pygame.font.Font('Fonts/Unigeo64-Bold-trial.ttf', 60)
TITLE_FONT = pygame.font.Font('Fonts/CameraObscuraDEMO.otf', 160)

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
    circ13 = Circle(326, y1, 13)  # randul 1, primul cerc
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


def is_final_state(circle_list):
    pebbles_row_1 = 0
    pebbles_row_2 = 0
    for circle in circle_list:
        if circle.get_nr_of_pebbles() != 0:
            if 0 < circle.get_number() <= 6:
                pebbles_row_2 += 1
            elif 7 < circle.get_number() <= 13:
                pebbles_row_1 += 1
    if pebbles_row_1 == 0:
        return 1
    elif pebbles_row_2 == 0:
        return 2
    return 0


def distribute_last_pebbles(circle_list, final_state):
    if final_state == 1:
        for circle in circle_list:
            if 0 < circle.get_number() <= 6:
                circle_list[7].add_n_pebbles(circle.get_nr_of_pebbles())
                circle.remove_pebbles()
    elif final_state == 2:
        for circle in circle_list:
            if 7 < circle.get_number() <= 13:
                circle_list[0].add_n_pebbles(circle.get_nr_of_pebbles())
                circle.remove_pebbles()


def draw_winner(player_one_points, player_two_points, pvp):
    if player_one_points > player_two_points and pvp:
        winner = "Player I wins!"
    elif player_one_points < player_two_points and pvp:
        winner = "Player II wins!"
    elif player_one_points > player_two_points and not pvp:
        winner = "Bot wins!"
    elif player_one_points < player_two_points and not pvp:
        winner = "You win!"
    else:
        winner = "It's a tie!"

    if pvp:
        player_one_text = "Player I" + " : " + str(player_one_points) + " points"
        player_two_text = "Player II" + " : " + str(player_two_points) + " points"
    else:
        player_one_text = "Bot" + " : " + str(player_one_points)
        player_two_text = "You" + " : " + str(player_two_points)

    # coat_color = (0, 0, 0, 15)
    # pygame.draw.rect(screen, coat_color, (0, 0, SCREEN_WIDTH-100, SCREEN_HEIGHT-100))

    winner_banner = pygame.image.load('Images/winner-banner.png').convert_alpha()
    banner_width = winner_banner.get_width() * 0.75
    banner_height = winner_banner.get_height() * 0.75
    winner_banner = pygame.transform.scale(winner_banner, (int(banner_width), int(banner_height)))

    screen.blit(winner_banner, (SCREEN_WIDTH // 2 - winner_banner.get_width() // 2,
                                SCREEN_HEIGHT // 2 - winner_banner.get_height() // 2))

    rendered_winner = WINNER_FONT.render(winner, True, "white")
    rendered_player_one_text = MEDIUM_FONT.render(player_one_text, True, "white")
    rendered_player_two_text = MEDIUM_FONT.render(player_two_text, True, "white")
    screen.blit(rendered_winner, (SCREEN_WIDTH // 2 - rendered_winner.get_width() // 2,
                                  SCREEN_HEIGHT // 2 - rendered_winner.get_height() // 2 - 30))
    screen.blit(rendered_player_one_text, (SCREEN_WIDTH // 2 - rendered_player_one_text.get_width() // 2,
                                           SCREEN_HEIGHT // 2 - rendered_player_one_text.get_height() // 2 + 70))
    screen.blit(rendered_player_two_text, (SCREEN_WIDTH // 2 - rendered_player_two_text.get_width() // 2,
                                           SCREEN_HEIGHT // 2 - rendered_player_two_text.get_height() // 2 + 100))


def draw_title():
    title = "MANCALA"
    rendered_title = TITLE_FONT.render(title, True, "white")
    rendered_title_black = TITLE_FONT.render(title, True, "black")

    screen.blit(rendered_title_black, (SCREEN_WIDTH // 2 - rendered_title.get_width() // 2 - 5,
                                       SCREEN_HEIGHT // 2 - rendered_title.get_height() // 2 - 105))
    screen.blit(rendered_title_black, (SCREEN_WIDTH // 2 - rendered_title.get_width() // 2 + 5,
                                       SCREEN_HEIGHT // 2 - rendered_title.get_height() // 2 - 95))
    screen.blit(rendered_title, (SCREEN_WIDTH // 2 - rendered_title.get_width() // 2,
                                 SCREEN_HEIGHT // 2 - rendered_title.get_height() // 2 - 100))


def draw_menu_buttons(button_width, button_height, mouse_pos):
    pygame.draw.rect(screen, "black", (SCREEN_WIDTH // 2 - button_width - 55, SCREEN_HEIGHT // 2 + 70,
                                       button_width, button_height))
    pygame.draw.rect(screen, "black", (SCREEN_WIDTH // 2 - button_width - 45, SCREEN_HEIGHT // 2 + 80,
                                       button_width, button_height))
    pygame.draw.rect(screen, "white", (SCREEN_WIDTH // 2 - button_width - 50, SCREEN_HEIGHT // 2 + 75,
                                       button_width, button_height))

    pygame.draw.rect(screen, "black", (SCREEN_WIDTH // 2 + 45, SCREEN_HEIGHT // 2 + 70,
                                       button_width, button_height))
    pygame.draw.rect(screen, "black", (SCREEN_WIDTH // 2 + 55, SCREEN_HEIGHT // 2 + 80,
                                       button_width, button_height))
    pygame.draw.rect(screen, "white", (SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2 + 75,
                                       button_width, button_height))

    pvp_button_text = "PvP"
    pvp_button_text_rendered = FONT.render(pvp_button_text, True, "black")
    pvp_button_text_rendered_white = FONT.render(pvp_button_text, True, "white")
    pve_button_text = "PvE"
    pve_button_text_rendered = FONT.render(pve_button_text, True, "black")
    pve_button_text_rendered_white = FONT.render(pve_button_text, True, "white")

    button_text_color = (227, 80, 7)

    screen.blit(pvp_button_text_rendered, (SCREEN_WIDTH // 2 - button_width // 2 - 50 -
                                           pvp_button_text_rendered.get_width() // 2, SCREEN_HEIGHT // 2 +
                                           80))
    screen.blit(pve_button_text_rendered, (SCREEN_WIDTH // 2 + button_width // 2 + 50 -
                                           pve_button_text_rendered.get_width() // 2, SCREEN_HEIGHT // 2 +
                                           80))

    if ((mouse_pos[0] > SCREEN_WIDTH // 2 - button_width - 50) and (mouse_pos[0] < SCREEN_WIDTH // 2 - 50) and
            (mouse_pos[1] > SCREEN_HEIGHT // 2 + 75) and (mouse_pos[1] < SCREEN_HEIGHT // 2 + 75 + button_height)):
        pygame.draw.rect(screen, button_text_color, (SCREEN_WIDTH // 2 - button_width - 50, SCREEN_HEIGHT // 2 + 75,
                                                     button_width, button_height))
        screen.blit(pvp_button_text_rendered_white, (SCREEN_WIDTH // 2 - button_width // 2 - 50 -
                                                     pvp_button_text_rendered.get_width() // 2, SCREEN_HEIGHT // 2
                                                     + 80))
    elif ((mouse_pos[0] > SCREEN_WIDTH // 2 + 50) and (mouse_pos[0] < SCREEN_WIDTH // 2 + button_width + 50) and
          (mouse_pos[1] > SCREEN_HEIGHT // 2 + 75) and (mouse_pos[1] < SCREEN_HEIGHT // 2 + 75 + button_height)):
        pygame.draw.rect(screen, button_text_color, (SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2 + 75,
                                                     button_width, button_height))
        screen.blit(pve_button_text_rendered_white, (SCREEN_WIDTH // 2 + button_width // 2 + 50 -
                                                     pve_button_text_rendered.get_width() // 2, SCREEN_HEIGHT // 2
                                                     + 80))


def check_pvp(button_width, button_height, mouse_pos):
    if ((mouse_pos[0] > SCREEN_WIDTH // 2 - button_width - 50) and (mouse_pos[0] < SCREEN_WIDTH // 2 - 50) and
            (mouse_pos[1] > SCREEN_HEIGHT // 2 + 75) and (mouse_pos[1] < SCREEN_HEIGHT // 2 + 75 + button_height)):
        return True
    return False


def check_pve(button_width, button_height, mouse_pos):
    if ((mouse_pos[0] > SCREEN_WIDTH // 2 + 50) and (mouse_pos[0] < SCREEN_WIDTH // 2 + button_width + 50) and
            (mouse_pos[1] > SCREEN_HEIGHT // 2 + 75) and (mouse_pos[1] < SCREEN_HEIGHT // 2 + 75 + button_height)):
        return True
    return False


def menu_button_pressed(pvp, pve, button_width, button_height):
    pressed_color = (82, 207, 209)
    if pvp:
        pygame.draw.rect(screen, pressed_color, (SCREEN_WIDTH // 2 - button_width - 50, SCREEN_HEIGHT // 2 + 75,
                                                 button_width, button_height))
        pvp_button_text = "PvP"
        pvp_button_text_rendered = FONT.render(pvp_button_text, True, "black")
        screen.blit(pvp_button_text_rendered, (SCREEN_WIDTH // 2 - button_width // 2 - 50 -
                                               pvp_button_text_rendered.get_width() // 2, SCREEN_HEIGHT // 2 +
                                               80))
    elif pve:
        pygame.draw.rect(screen, pressed_color, (SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2 + 75,
                                                 button_width, button_height))
        pve_button_text = "PvE"
        pve_button_text_rendered = FONT.render(pve_button_text, True, "black")
        screen.blit(pve_button_text_rendered, (SCREEN_WIDTH // 2 + button_width // 2 + 50 -
                                               pve_button_text_rendered.get_width() // 2, SCREEN_HEIGHT // 2 +
                                               80))


def draw_menu_screen(menu_screen, background_image):
    while menu_screen:
        screen.blit(background_image, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        button_width = 150
        button_height = 50
        quit_b_x1, quit_b_y1, quit_button_width, quit_button_height = draw_quit_button()

        draw_title()
        draw_menu_buttons(button_width, button_height, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pvp = check_pvp(button_width, button_height, mouse_pos)
                pve = check_pve(button_width, button_height, mouse_pos)
                if pvp or pve:
                    menu_button_pressed(pvp, pve, button_width, button_height)
                if pvp:
                    return True
                elif pve:
                    return False
                if ((mouse_pos[0] > quit_b_x1) and (mouse_pos[0] < quit_b_x1 + quit_button_width) and
                        (mouse_pos[1] > quit_b_y1) and (mouse_pos[1] < quit_b_y1 + quit_button_height)):
                    pygame.quit()

        pygame.display.flip()


def draw_quit_button():
    mouse_pos = pygame.mouse.get_pos()
    button_width = 150
    button_height = 50
    button_text = "QUIT"
    button_hover_color = (227, 80, 7)

    button_text_rendered = FONT.render(button_text, True, "black")
    button_text_rendered_white = FONT.render(button_text, True, "white")

    quit_b_x1 = SCREEN_WIDTH // 2 - button_width // 2
    quit_b_y1 = SCREEN_HEIGHT // 2 + 235

    pygame.draw.rect(screen, "black", (quit_b_x1 - 5, quit_b_y1 - 5, button_width, button_height))
    pygame.draw.rect(screen, "black", (quit_b_x1 + 5, quit_b_y1 + 5, button_width, button_height))
    pygame.draw.rect(screen, "white", (quit_b_x1, quit_b_y1, button_width, button_height))
    screen.blit(button_text_rendered, (SCREEN_WIDTH // 2 - button_text_rendered.get_width() // 2,
                                       SCREEN_HEIGHT // 2 + 240))

    if ((mouse_pos[0] > quit_b_x1) and (mouse_pos[0] < quit_b_x1 + button_width) and
            (mouse_pos[1] > quit_b_y1) and (mouse_pos[1] < quit_b_y1 + button_height)):
        pygame.draw.rect(screen, button_hover_color, (quit_b_x1, quit_b_y1,
                                                      button_width, button_height))
        screen.blit(button_text_rendered_white, (SCREEN_WIDTH // 2 - button_text_rendered.get_width() // 2,
                                                 SCREEN_HEIGHT // 2 + 240))

    return quit_b_x1, quit_b_y1, button_width, button_height


def draw_back_to_menu_button():
    mouse_pos = pygame.mouse.get_pos()
    button_width = 300
    button_height = 50
    button_text = "Back to menu"
    button_hover_color = (227, 80, 7)
    button_text_rendered = FONT.render(button_text, True, "black")
    button_text_rendered_white = FONT.render(button_text, True, "white")

    pygame.draw.rect(screen, "black", (SCREEN_WIDTH // 2 - button_width // 2 - 5, SCREEN_HEIGHT // 2 + 175,
                                       button_width, button_height))
    pygame.draw.rect(screen, "black", (SCREEN_WIDTH // 2 - button_width // 2 + 5, SCREEN_HEIGHT // 2 + 185,
                                       button_width, button_height))
    pygame.draw.rect(screen, "white", (SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + 180,
                                       button_width, button_height))
    screen.blit(button_text_rendered, (SCREEN_WIDTH // 2 - button_text_rendered.get_width() // 2 + 5,
                                       SCREEN_HEIGHT // 2 + 185))

    if ((mouse_pos[0] > SCREEN_WIDTH // 2 - button_width // 2) and
            (mouse_pos[0] < SCREEN_WIDTH // 2 + button_width // 2) and
            (mouse_pos[1] > SCREEN_HEIGHT // 2 + 180) and (mouse_pos[1] < SCREEN_HEIGHT // 2 + 180 + button_height)):
        pygame.draw.rect(screen, button_hover_color, (SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + 180,
                                                      button_width, button_height))
        screen.blit(button_text_rendered_white, (SCREEN_WIDTH // 2 - button_text_rendered.get_width() // 2 + 5,
                                                 SCREEN_HEIGHT // 2 + 185))


def draw_winner_screen(winner_screen, background_image, circle_list, pvp):
    while winner_screen:
        screen.blit(background_image, (0, 0))
        draw_winner(circle_list[0].get_nr_of_pebbles(), circle_list[7].get_nr_of_pebbles(), pvp)

        draw_back_to_menu_button()
        quit_b_x1, quit_b_y1, quit_button_width, quit_button_height = draw_quit_button()

        back_button_width = 300
        back_button_height = 50

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if ((mouse_pos[0] > SCREEN_WIDTH // 2 - back_button_width // 2) and
                        (mouse_pos[0] < SCREEN_WIDTH // 2 + back_button_width // 2) and
                        (mouse_pos[1] > SCREEN_HEIGHT // 2 + 170) and
                        (mouse_pos[1] < SCREEN_HEIGHT // 2 + 170 + back_button_height)):
                    return
                if ((mouse_pos[0] > quit_b_x1) and (mouse_pos[0] < quit_b_x1 + quit_button_width) and
                        (mouse_pos[1] > quit_b_y1) and (mouse_pos[1] < quit_b_y1 + quit_button_height)):
                    pygame.quit()
        pygame.display.flip()


def bot_turn(circle_list):
    bot_selected = 0
    while not bot_selected:
        bot_selected = random.randint(8, 13)
        for circle in circle_list:
            if circle.get_number() == bot_selected and circle.get_nr_of_pebbles() != 0:
                highlight_bot_selected(circle)
                return circle
        bot_selected = 0


def highlight_bot_selected(circle):
    for i in range(1, 5):
        circle.draw_outline_hovered()
        pygame.time.wait(200)
        pygame.display.flip()


def bot_selection(circle_list, bot_selected):
    current_pebbles = bot_selected.get_nr_of_pebbles()
    bot_selected.remove_pebbles()
    i = 1
    last_circle = bot_selected
    while current_pebbles > 0:
        if (bot_selected.get_number() + i) % 14 == 7:
            i += 1
        last_circle = circle_list[(bot_selected.get_number() + i) % 14]
        last_circle.add_pebble()
        current_pebbles -= 1
        i += 1
    new_player_turn = last_circle_handling(last_circle, circle_list, 1)
    return new_player_turn


def draw_game_screen(playing, background_image, board_image, circle_list, player_turn, player_turn_images,
                     player_turn_highlights, num_flag_up, num_flag_down, player_one_flag, player_two_flag, pvp):
    while playing:
        screen.blit(background_image, (0, 0))
        board_position = (SCREEN_WIDTH // 2 - board_image.get_width() // 2,
                          SCREEN_HEIGHT // 2 - board_image.get_height() // 2)
        screen.blit(board_image, board_position)
        mouse_pos = pygame.mouse.get_pos()

        draw_pebbles(circle_list)
        draw_player_flags(player_one_flag, player_two_flag, circle_list[0].get_nr_of_pebbles(),
                          circle_list[7].get_nr_of_pebbles())
        draw_hovered_circles(circle_list, mouse_pos, num_flag_up, num_flag_down, player_turn)
        draw_opponent_flags(circle_list, num_flag_up, num_flag_down, player_turn)

        if not pvp and player_turn == 1:
            bot_selected = bot_turn(circle_list)
            player_turn = bot_selection(circle_list, bot_selected)

        draw_player_turn(player_turn, player_turn_images, player_turn_highlights, pvp)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                new_player_turn = circle_is_clicked(circle_list, mouse_pos, player_turn)
                if new_player_turn != 0:
                    player_turn = new_player_turn

        final_state = is_final_state(circle_list)
        if final_state != 0:
            distribute_last_pebbles(circle_list, final_state)
            return

        pygame.display.flip()


def setup(circle_list):
    for circle in circle_list:
        circle.remove_pebbles()
        circle.add_n_pebbles(4)

    circle_list[0].remove_pebbles()
    circle_list[7].remove_pebbles()

    # Testing
    # for i in range(1, 6):
    #     circle_list[i].remove_pebbles()


def main():
    board_image, board_width, board_height = get_board()
    background_image = get_background_image()
    num_flag_up, num_flag_down, player_one_flag, player_two_flag = get_flags()

    make_circles()
    circle_list = make_circles()

    player_turn = 1

    menu_screen = True
    playing = False
    winner_screen = False
    pvp = True

    while True:
        if menu_screen:
            pvp = draw_menu_screen(menu_screen, background_image)
            playing = True
            menu_screen = False
        elif playing:
            player_turn_images = load_player_turn_images(pvp)
            player_turn_highlights = load_player_turn_highlights()
            setup(circle_list)
            draw_game_screen(playing, background_image, board_image, circle_list, player_turn,
                             player_turn_images, player_turn_highlights, num_flag_up, num_flag_down,
                             player_one_flag, player_two_flag, pvp)
            playing = False
            winner_screen = True
        elif winner_screen:
            draw_winner_screen(winner_screen, background_image, circle_list, pvp)
            winner_screen = False
            menu_screen = True


if __name__ == '__main__':
    main()
