import pygame
import random

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# FONT = pygame.font.SysFont("Arial", 30)
"""Fonts used in the game:"""
FONT = pygame.font.Font('Fonts/LEMONMILK-Medium.otf', 30)
MEDIUM_FONT = pygame.font.Font('Fonts/LEMONMILK-Regular.otf', 30)
BOLD_FONT = pygame.font.Font('Fonts/Unigeo64-Bold-trial.ttf', 30)
WINNER_FONT = pygame.font.Font('Fonts/Unigeo64-Bold-trial.ttf', 60)
TITLE_FONT = pygame.font.Font('Fonts/CameraObscuraDEMO.otf', 160)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mancala")


class Circle:
    """ Class for the circles on the board.
    Each circle represents a hole in the board. That includes the two holes for the player's points.
    """
    radius = 53
    diameter = radius * 2
    outline_thickness = 7
    hover_outline_color = "white"

    def __init__(self, x, y, number):
        """Constructor for the Circle class.

        Parameters:
        - number (int) : represents the given number of the circle, from 0 to 13 (0 and 7 correspond to the player's
        points holes). The numbers are assigned from the top left (the first player's points hole) going
        counterclockwise.
        - x, y (float) represent the coordinates of the center of the circle.

        Variables:
        - pebbles (int) represents the number of pebbles found in the circle. By default, they are 4.
        """
        self.number = number
        self.x = x
        self.y = y
        self.pebbles = 4

    def is_hovered_over(self, mouse_pos):
        """Check if the mouse is hovering over the circle."""
        distance_from_center = ((self.x - mouse_pos[0]) ** 2 + (self.y - mouse_pos[1]) ** 2) ** 0.5
        return distance_from_center <= self.radius

    def draw_outline_hovered(self):
        """Draw the outline of the circle when the mouse is hovering over it."""
        pygame.draw.circle(screen, self.hover_outline_color, (self.x, self.y), 45 +
                           self.outline_thickness, self.outline_thickness)

    def get_number(self):
        """Get the number of the circle."""
        return self.number

    def add_pebble(self):
        """Increase the number of pebbles for circle by 1."""
        self.pebbles += 1

    def add_n_pebbles(self, n):
        """Increase the number of pebbles for circle by n."""
        self.pebbles += n

    def get_nr_of_pebbles(self):
        """Get the number of pebbles in the circle."""
        return self.pebbles

    def remove_pebbles(self):
        """Remove all pebbles from the circle."""
        self.pebbles = 0


def get_background_image():
    """Load, rescale and return the background image of the game."""
    background_image = pygame.image.load('Images/background.png').convert()
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    return background_image


def get_board():
    """Load, rescale, and return the board image and its new width and height."""
    board_image = pygame.image.load('Images/mancala_board_blurred.png').convert_alpha()
    board_width = board_image.get_width() * 0.75
    board_height = board_image.get_height() * 0.75
    board_image = pygame.transform.scale(board_image, (int(board_width), int(board_height)))
    return board_image, board_width, board_height


def get_flags():
    """Load and return the images of the flags.
    The flags are used to show the number of pebbles in a circle:
    - num_flag_up and num_flag_down are used on the circles from the top and bottom rows
    - player_one_flag and player_two_flag are used to show the number of points for each player and are displayed on
    the side of each "player's points" hole
    """
    num_flag_up = pygame.image.load('Images/number-flag-up.png').convert_alpha()
    num_flag_down = pygame.image.load('Images/number-flag-down.png').convert_alpha()
    player_one_flag = pygame.image.load('Images/player-one.png').convert_alpha()
    player_two_flag = pygame.image.load('Images/player-two.png').convert_alpha()
    return num_flag_up, num_flag_down, player_one_flag, player_two_flag


def make_circles():
    """Create and return the circles on the board.
    The circles are created starting from the top left (the first player's points hole), going counterclockwise.

    Variables:
    - y1 and y2 correspond to the y coordinates of the first and the second row of circles
    - circ0 and circ7 are the first and second player's points holes
    - circ1 to circ6 are circles from the second row and correspond to the second player's circles
    - circ8 to circ13 are circles from the first row and correspond to the first player's circles
    """
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
    """Draw the outline and the flag of a circle when the mouse is hovering over it.

    Parameters:
    - circle_list (list) : list of the circles on the board
    - mouse_pos (tuple) : tuple of the x and y coordinates corresponding to the mouse's position
    - num_flag_up, num_flag_down (loaded images) : images of the flags that show the number of pebbles in a circle
    - player_turn (int) : represents the current player's turn (1 or 2)

    If the mouse is hovering over a circle from the top row (7 < circle.get_number() <= 13) and it's the first
    player's turn, draw the outline and the flag of the circle.
    If the mouse is hovering over a circle from the bottom row (0 < circle.get_number() <= 6) and it's the second
    player's turn, draw the outline and the flag of the circle.
    """
    for circle in circle_list:
        if circle.is_hovered_over(mouse_pos):
            if player_turn == 1 and circle.get_number() > 7:
                circle.draw_outline_hovered()
                draw_nr_of_pebbles_flags(circle_list, mouse_pos, num_flag_up, num_flag_down)
            elif player_turn == 2 and 0 < circle.get_number() <= 6:
                circle.draw_outline_hovered()
                draw_nr_of_pebbles_flags(circle_list, mouse_pos, num_flag_up, num_flag_down)


def draw_flag_numbers(circle, rendered_number):
    """Draw the number of pebbles in a circle on the flag of the circle.

    Parameters:
    - circle (Circle) : the circle in question
    - rendered_number (rendered text) : the number of pebbles in the circle
    """
    y_addition = 90
    if 7 < circle.get_number() <= 13:
        y_addition = -130
    screen.blit(rendered_number, (circle.x - rendered_number.get_width() / 2, circle.y + y_addition))


def draw_nr_of_pebbles_flags(circle_list, mouse_pos, num_flag_up, num_flag_down):
    """Draw the flag that shows the number of pebbles on the hovered circle.

    Parameters:
    - circle_list (list) : list of the circles on the board
    - mouse_pos (tuple) : tuple of the x and y coordinates corresponding to the mouse's position
    - num_flag_up, num_flag_down (loaded images) : images of the flags that show the number of pebbles in a circle

    If the mouse is hovering over a circle from the top row (7 < circle.get_number() <= 13), draw the flag above the
    circle and then draw the number of pebbles on the flag.
    If the mouse is hovering over a circle from the bottom row (0 < circle.get_number() <= 6), draw the flag below the
    circle and then draw the number of pebbles on the flag.
    """
    for circle in circle_list:
        nr_of_pebbles = circle.get_nr_of_pebbles()
        rendered_number = FONT.render(str(nr_of_pebbles), True, "white")
        if circle.is_hovered_over(mouse_pos):
            if 7 < circle.get_number() <= 13:
                screen.blit(num_flag_up, (circle.x - num_flag_up.get_width() / 2,
                                          circle.y - 1.75 * num_flag_up.get_height()))
                draw_flag_numbers(circle, rendered_number)
            elif 0 < circle.get_number() <= 6:
                screen.blit(num_flag_down, (circle.x - num_flag_down.get_width() / 2,
                                            circle.y + 1.5 * num_flag_down.get_height() / 2))
                draw_flag_numbers(circle, rendered_number)


def draw_opponent_flags(circle_list, num_flag_up, num_flag_down, player_turn):
    """Draw the flags that show the number of pebbles in the opponent's circles.

    Parameters:
    - circle_list (list) : list of the circles on the board
    - num_flag_up, num_flag_down (loaded images) : images of the flags that show the number of pebbles in a circle
    - player_turn (int) : represents the current player's turn (1 or 2)

    If it's the first player's turn, draw the flags and the numbers on them for the circles in the bottom row.
    If it's the second player's turn, draw the flags and the numbers on them for the circles in the top row.
    """
    for circle in circle_list:
        nr_of_pebbles = circle.get_nr_of_pebbles()
        rendered_number = FONT.render(str(nr_of_pebbles), True, "white")
        if player_turn == 1 and 0 < circle.get_number() <= 6:
            screen.blit(num_flag_down,
                        (circle.x - num_flag_down.get_width() / 2, circle.y + 1.5 * num_flag_down.get_height() / 2))
            draw_flag_numbers(circle, rendered_number)
        elif player_turn == 2 and 7 < circle.get_number() <= 13:
            screen.blit(num_flag_up,
                        (circle.x - num_flag_up.get_width() / 2, circle.y - 1.75 * num_flag_up.get_height()))
            draw_flag_numbers(circle, rendered_number)


def draw_player_flags(player_one_flag, player_two_flag, player_one_points, player_two_points):
    """Draw the players' points flags and the number of points on them.

    Parameters:
    - player_one_flag, player_two_flag (loaded images) : images of the flags for the players' points flags
    - player_one_points, player_two_points (int) : the number of points for each player
    """
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
    """Load and return the images of pebbles. There is an image for 1 pebble, 2 pebbles and 3 or more pebbles."""
    one_pebble = pygame.image.load('Images/1-pebble-heart.png').convert_alpha()
    two_pebbles = pygame.image.load('Images/2-pebbles.png').convert_alpha()
    three_pebbles = pygame.image.load('Images/3-pebbles.png').convert_alpha()
    return one_pebble, two_pebbles, three_pebbles


def draw_pebbles(circle_list):
    """Draw the pebbles in the circles.

    Parameter:
    - circle_list (list) : list of the circles on the board

    For each circle on the board, check the number of pebbles in the circle and draw the corresponding image of
    pebbles in the circle.
    """
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
    """Check if a circle is clicked and return the new player's turn.

    Parameters:
    - circle_list (list) : list of the circles on the board
    - mouse_pos (tuple) : tuple of the x and y coordinates corresponding to the mouse's position
    - player_turn (int) : represents the current player's turn (1 or 2)

    If a circle on the current player's side of the board is clicked, remove all pebbles from that circle and
    redistribute them to the next circles counterclockwise, one pebble at a time, skipping the opponent's hole.
    Remember the last circle where a pebble was dropped and calculate the next player's turn using the
    last_circle_handling function.
    """
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
    """Return the new player's turn based on the previous player's turn and the last circle where a pebble was dropped.

    Parameters:
    - last_circle (Circle) : the last circle where a pebble was dropped
    - circle_list (list) : list of the circles on the board
    - player_turn (int) : represents the last player's turn (1 or 2)

    If the last_circle was the last player's points hole, the player gets another turn.
    If the last_circle did not have any pebbles in it (so now has 1 pebble) and it is on the last player's side of
    the board, the player gets all the pebbles from that last_circle and from the circle opposite of it and adds them to
    their points.
    Otherwise, the next player's turn is the other player's turn.
    """
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
    """Load and return the images that show which player's turn it is after checking if the game is PvP or PvE.

    Parameter:
    - pvp (bool) : True if the game is PvP, False if the game is PvE

    If the game is PvP, load images showing "Player I's turn" and "Player II's turn".
    If the game is PvE, load images showing "Bot's turn" and "Your turn".
    """
    if pvp:
        player_one_turn = pygame.image.load('Images/player-one-turn.png').convert_alpha()
        player_two_turn = pygame.image.load('Images/player-two-turn.png').convert_alpha()
    else:
        player_one_turn = pygame.image.load('Images/bot-turn.png').convert_alpha()
        player_two_turn = pygame.image.load('Images/your-turn.png').convert_alpha()
    return player_one_turn, player_two_turn


def load_player_turn_highlights():
    """Load, rescale and return image highlights showing which player's turn it is."""
    player_one_highlight = pygame.image.load('Images/player-one-highlight.png').convert_alpha()
    player_two_highlight = pygame.image.load('Images/player-two-highlight.png').convert_alpha()
    highlight_width = player_one_highlight.get_width() * 0.75
    highlight_height = player_one_highlight.get_height() * 0.75
    player_one_highlight = pygame.transform.scale(player_one_highlight, (int(highlight_width), int(highlight_height)))
    player_two_highlight = pygame.transform.scale(player_two_highlight, (int(highlight_width), int(highlight_height)))
    return player_one_highlight, player_two_highlight


def draw_player_turn(player_turn, player_turn_images, player_turn_highlights, pvp):
    """Draw at the top of the screen which player's turn it is and highlight on the top left or bottom right sides of
    the board which player's turn it is."""
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
    """Draw at the bottom of the screen a hint for the current player."""
    if player_turn == 1 and pvp is True:
        hint = "Player I : Select a circle from the top row"
    else:
        hint = "Player II : Select a circle from the bottom row"
    rendered_hint = BOLD_FONT.render(hint, True, "white")
    screen.blit(rendered_hint, (SCREEN_WIDTH // 2 - rendered_hint.get_width() // 2,
                                SCREEN_HEIGHT - rendered_hint.get_height() - 15))


def is_final_state(circle_list):
    """Check if the state of the game is a final one and return the number of the player that finished the game. If the
    game is not in a final state, return 0.
    The game is in a final state when all the holes from a player's side are empty.
    """
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
    """Distribute the pebbles from the other player's side of the board (the player which didn't finish the game) to
    that player's points hole.

    Parameters:
    - circle_list (list) : list of the circles on the board
    - final_state (int) : the number of the player that finished the game (1 or 2)
    """
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
    """Load, rescale and draw the winner banner, the winner text on it and the players' points below them.

    Parameters:
    - player_one_points, player_two_points (int) : the number of points for each player
    - pvp (bool) : True if the game is PvP, False if the game is PvE
    """
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
    """Render and draw the title of the game."""
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
    """Draw the buttons on the menu screen for PvP and PvE and change their color if the mouse is hovering over them.

    Parameters:
    - button_width, button_height (int) : the width and height of the buttons
    - mouse_pos (tuple) : tuple of the x and y coordinates corresponding to the mouse's position

    The buttons have black rectangles behind them to make them more visible and for aesthetic purposes.
    """
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
    """Return True if the mouse is hovering over the PvP button or False otherwise."""
    if ((mouse_pos[0] > SCREEN_WIDTH // 2 - button_width - 50) and (mouse_pos[0] < SCREEN_WIDTH // 2 - 50) and
            (mouse_pos[1] > SCREEN_HEIGHT // 2 + 75) and (mouse_pos[1] < SCREEN_HEIGHT // 2 + 75 + button_height)):
        return True
    return False


def check_pve(button_width, button_height, mouse_pos):
    """Return True if the mouse is hovering over the PvE button or False otherwise."""
    if ((mouse_pos[0] > SCREEN_WIDTH // 2 + 50) and (mouse_pos[0] < SCREEN_WIDTH // 2 + button_width + 50) and
            (mouse_pos[1] > SCREEN_HEIGHT // 2 + 75) and (mouse_pos[1] < SCREEN_HEIGHT // 2 + 75 + button_height)):
        return True
    return False


def menu_button_pressed(pvp, pve, button_width, button_height):
    """Draw the pressed button in another color.

    Parameters:
    - pvp (bool) : True if the PvP button was pressed, False otherwise
    - pve (bool) : True if the PvE button was pressed, False otherwise
    - button_width, button_height (int) : the width and height of the buttons (they have the same width and height)
    """
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
    """This is the main function for the menu screen.
    Draw the menu screen, the PvP button, the PvE button and the Quit button and check if the mouse is hovering over a
    button or if a button is pressed.
    Return True if the PvP button was pressed or False if the PvE button was pressed.
    Quit the game if the Quit button was pressed or the X button was pressed (the one from top right).

    Parameters:
    - menu_screen (bool) : True if the menu screen is displayed, False otherwise
    - background_image (loaded image) : the background image for the menu screen
    """
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
    """Draw the Quit button and change its color if the mouse is hovering over it.
    Return the coordinates and dimensions of the button.
    """
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
    """Draw the Back to menu button and change its color if the mouse is hovering over it."""
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
    """This is the main function for the winner screen.
    Draw the winner screen and check if the mouse is hovering over the buttons or if a button is pressed.
    Return to the menu screen if the Back to menu button was pressed.
    Quit the game if the Quit button was pressed or if the X button was pressed (the one from top right).

    Parameters:
    - winner_screen (bool) : True if the winner screen is displayed, False otherwise
    - background_image (loaded image) : the background image for the winner screen
    - circle_list (list) : list of the circles on the board
    - pvp (bool) : True if the game is PvP, False if the game is PvE
    """
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
    """Select a random circle which has pebbles in it from the top side (the bot's side) of the board and return it.
    This function makes the bot's selection.

    Parameter:
    - circle_list (list) : list of the circles on the board
    """
    bot_selected = 0
    while not bot_selected:
        bot_selected = random.randint(8, 13)
        for circle in circle_list:
            if circle.get_number() == bot_selected and circle.get_nr_of_pebbles() != 0:
                highlight_bot_selected(circle)
                return circle
        bot_selected = 0


def highlight_bot_selected(circle):
    """Highlight the circle selected by the bot for a period of time.
    This function was created to make the bot's selection more visible for the player.
    """
    for i in range(1, 10):
        circle.draw_outline_hovered()
        pygame.time.wait(200)
        pygame.display.flip()


def bot_selection(circle_list, bot_selected):
    """Distribute the pebbles from the selected circle and return the next player's turn.
    This function is called after the bot selected a circle, so only in PvE mode and is similar to the
    circle_is_clicked function.

    Parameters:
    - circle_list (list) : list of the circles on the board
    - bot_selected (Circle) : the circle selected by the bot
    """
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
    """This is the main function for the game screen - it captures the playing phase.
    Draw the game screen, the board, the pebbles, the player's and opponent's flags and the hovered circles.
    Draw the player's turn banner from the top of the screen and the hint at the bottom.
    Check if the mouse is hovering over a circle and if a circle is clicked.
    Check if the game is in PvE mode and make the bot's selection if it's the bot's turn.
    Check if the game is in a final state and distribute the pebbles accordingly and then return.
    Quit the game if the X button was pressed (the one from top right).

    Parameters:
    - playing (bool) : True if the game screen is displayed, False otherwise
    - background_image, board_image, player_turn_images, player_turn_highlights (loaded images)
    - circle_list (list) : list of the circles on the board
    - player_turn (int) : the number of the player which has the turn
    - num_flag_up, num_flag_down, player_one_flag, player_two_flag (loaded images) : flag images
    - pvp (bool) : True if the game is PvP, False if the game is PvE
    """
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
            draw_opponent_flags(circle_list, num_flag_up, num_flag_down, 2)
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
    """Set up the board for a new game: that means removing the pebbles from the player's holes and adding 4 pebbles
    to the rest of them each.
    """
    for circle in circle_list:
        circle.remove_pebbles()
        circle.add_n_pebbles(4)

    circle_list[0].remove_pebbles()
    circle_list[7].remove_pebbles()

    # Testing
    # for i in range(1, 6):
    #     circle_list[i].remove_pebbles()


def main():
    """This is the main function of the game.
    It loads some images (the board, the background, the flags).
    It creates the circle objects and stores them in a list. (it is actually a tuple, but it sounds better to say
    it's a list(sorry))
    It sets the first player's turn to 1 (player I), but that can be changed to a random choice between 1 and 2.
    It sets the menu_screen to True and the other screens to false.
    In the while loop, which can be exited only by quitting the game (pressing the X button or the Quit button where
    there is one), the menu screen is displayed at first and the game starts when the player presses the PvP or PvE
    button.
    The game screen is displayed then (after making the setup for a new game), in PvP or PvE mode (depending on the
    previous choice) and it is played until it reaches a final state.
    After that, the winner screen is displayed in which the player can choose between going back to the menu and
    starting another game, or quitting the game.
    """
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

    # print(main.__doc__)

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
