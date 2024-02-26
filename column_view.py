#project 5 pygame

import features as f
import pygame
import column_model as column
from user_class import User
from game_class import Game

_FRAME_RATE = 30
_INITIAL_WIDTH = 600
_INITIAL_HEIGHT = 700
_BACKGROUND_COLOR = pygame.Color(255, 255, 255)
Black = pygame.Color(222,222,222)
blue_fd = pygame.Color(0, 102, 204)
green_fd = pygame.Color(0, 204, 102)
red_fd = pygame.Color(255, 50, 50)
yellow_fd = pygame.Color(255,255,50)
purple_fd = pygame.Color(153,51,255)
orange_fd = pygame.Color(255,153,50)
turq_fd = pygame.Color(64,224,208)

color_list_game = ('B','G','R','Y','P','O','T')
color_list = [blue_fd,green_fd,red_fd,yellow_fd,purple_fd,orange_fd,turq_fd]


class Columns:
    def __init__(self):
        self._user = User()
        self._user.play_game_over_pygame()
        self._game = self._user.game()
        self._move_ready = True

        self._state = column.GameState(self._game.get_game_column())
        self._state_grid = column.Grid()
        self._running = True

    def run(self) -> None:
        pygame.init()

        try:
            clock = pygame.time.Clock()

            self._create_surface((_INITIAL_WIDTH, _INITIAL_HEIGHT))

            while self._running:
                clock.tick(_FRAME_RATE)
                self._handle_events()
                self._draw_frame()

        finally:
            pygame.quit()

    def _create_surface(self, size: tuple[int, int]) -> None:
        self._surface = pygame.display.set_mode(size, pygame.RESIZABLE)

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            self._handle_event(event)

        self._handle_keys()
        self.move_block_down()


    def _handle_event(self, event) -> None:
        if event.type == pygame.QUIT:
            self._stop_running()
        elif event.type == pygame.VIDEORESIZE:
            self._create_surface(event.size)

    def _handle_keys(self) -> None:
        """handles key input and performs an action according to the key pressed"""

        if self._state.player().get_press_counter() == 12:
            self._state.player().reset_press_counter()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self._state.player().get_press_counter() == 0:
            self._game.move_fallen_left()
            self._move_ready = False
            if self._game._fallen.get_moved_stat():
                self._state.player().move_left()
                self._state.player().increase_press_counter()
                self._game.cycle_game_in_pygame()
                self._game._fallen._moved = False
                self._move_ready = True

        if keys[pygame.K_RIGHT] and self._state.player().get_press_counter() == 0:
            self._game.move_fallen_right()
            self._move_ready = False
            if self._game._fallen.get_moved_stat():
                self._state.player().move_right()
                self._state.player().increase_press_counter()
                self._game.cycle_game_in_pygame()
                self._game._fallen._moved = False
                self._move_ready = True

        if keys[pygame.K_SPACE] and self._state.player().get_press_counter() == 0:
            if self._game.get_game_state():
                self._game.rotate_block()
                self._state.player().rotate()
                self._state.player().increase_press_counter()

        if self._state.player().get_press_counter() != 0:
            self._state.player().increase_press_counter()

    def move_block_down(self) -> None:
        """moves the block down on the grid"""
        if self._state.player().get_fall_counter() == 0:
            bottom_most = f.find_bottom_most(self._state_grid.get_grid(), self._game.get_game_column())
            self._state.player().move_down(bottom_most)
            self._game.cycle_game_in_pygame()
            self._state.player().increase_fall_counter()
        else:
            self._state.player().increase_fall_counter()
        if self._state.player().get_fall_counter() == 20:
            self._state.player().reset_fall_counter()

    def _stop_running(self) -> None:
        self._running = False

    def _draw_frame(self) -> None:
        """draws and handles the following components of the game:
            surface, grid, player block"""
        self._surface.fill(_BACKGROUND_COLOR)
        if not self._state.player().get_fix_status():
            self._state_grid.update_grid(self._game.get_grid())
            self._user.play_game_over_pygame()

            self._game = Game(self._game.get_grid())
            self._game.cycle_game_in_pygame()

            self._state = column.GameState(self._game.get_game_column())
        self._draw_player()
        self.draw_grid(self._state_grid.get_grid())
        pygame.display.flip()

    def _draw_player(self) -> None:
        self.draw_block()

    def draw_block(self) -> None:
        """draws the player's falling block"""

        if not self._state.player().color_stat():
            temp_colors = self.convert_game_colors_to_pygame(self._game.get_colors())

            self._state.player().set_color1(color_list[temp_colors[2]])
            self._state.player().set_color2(color_list[temp_colors[1]])
            self._state.player().set_color3(color_list[temp_colors[0]])

            self._state.player()._color_selected = True

        top_left_frac_x, top_left_frac_y = self._state.player().top_left()
        width_frac = self._state.player().width()
        height_frac = self._state.player().height()

        top_left_pixel_x = self._frac_x_to_pixel_x(top_left_frac_x)
        top_left_pixel_y = self._frac_y_to_pixel_y(top_left_frac_y)
        width_pixel = self._frac_x_to_pixel_x(width_frac)
        height_pixel = self._frac_y_to_pixel_y(height_frac)

        difference = self._surface.get_height() / 13

        player_rect1 = pygame.Rect(
            top_left_pixel_x, top_left_pixel_y,
            width_pixel, height_pixel)

        player_rect2 = pygame.Rect(
            top_left_pixel_x, top_left_pixel_y - difference,
            width_pixel, height_pixel)

        player_rect3 = pygame.Rect(
            top_left_pixel_x, top_left_pixel_y - difference * 2,
            width_pixel, height_pixel)

        color1 = self._state.player().get_color1()
        color2 = self._state.player().get_color2()
        color3 = self._state.player().get_color3()

        pygame.draw.rect(self._surface, color1, player_rect1, self._state.player().get_border_rad(), 5)
        pygame.draw.rect(self._surface, color2, player_rect2, self._state.player().get_border_rad(), 5)
        pygame.draw.rect(self._surface, color3, player_rect3, self._state.player().get_border_rad(), 5)


    def draw_lines(self) -> None:
        """draws vertical lines on the surface"""
        res_const = self._surface.get_width() / 6

        pygame.draw.line(self._surface, Black, (res_const * 1, 0), (res_const * 1, self._surface.get_height()), 3)
        pygame.draw.line(self._surface, Black, (res_const * 2, 0), (res_const * 2, self._surface.get_height()), 3)
        pygame.draw.line(self._surface, Black, (res_const * 3, 0), (res_const * 3, self._surface.get_height()), 3)
        pygame.draw.line(self._surface, Black, (res_const * 4, 0), (res_const * 4, self._surface.get_height()), 3)
        pygame.draw.line(self._surface, Black, (res_const * 5, 0), (res_const * 5, self._surface.get_height()), 3)
        pygame.draw.line(self._surface, Black, (res_const * 6, 0), (res_const * 6, self._surface.get_height()), 3)


    def _frac_x_to_pixel_x(self, frac_x: float) -> int:
        """returns a conversion of frac to pixel for x"""
        return self._frac_to_pixel(frac_x, self._surface.get_width())

    def _frac_y_to_pixel_y(self, frac_y: float) -> int:
        """returns a conversion of frac to pixel for y"""
        return self._frac_to_pixel(frac_y, self._surface.get_height())

    def _frac_to_pixel(self, frac: float, max_pixel: int) -> int:
        """converts frac to pixel"""
        return int(frac * max_pixel)

    def draw_block_on_grid(self, row: int, column_val: int, color1) -> None:
        """draws a one block onto grid with specified grid location"""
        top_left_frac_x = column_val * self._state.player().width()
        top_left_frac_y = row * self._state.player().height()
        width_frac = self._state.player().width()
        height_frac = self._state.player().height()

        top_left_pixel_x = self._frac_x_to_pixel_x(top_left_frac_x)
        top_left_pixel_y = self._frac_y_to_pixel_y(top_left_frac_y)
        width_pixel = self._frac_x_to_pixel_x(width_frac)
        height_pixel = self._frac_y_to_pixel_y(height_frac)

        rect1 = pygame.Rect(
            top_left_pixel_x, top_left_pixel_y,
            width_pixel, height_pixel)

        pygame.draw.rect(self._surface, color1, rect1, border_radius=5)

    def draw_grid(self, grid: list[list]) -> None:
        """draws the grid that is passed in"""
        self.draw_lines()
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col] != 0:
                    if grid[row][col] == 'B':
                        self.draw_block_on_grid(row,col,blue_fd)
                    elif grid[row][col] == 'G':
                        self.draw_block_on_grid(row, col, green_fd)
                    elif grid[row][col] == 'R':
                        self.draw_block_on_grid(row, col, red_fd)
                    elif grid[row][col] == 'Y':
                        self.draw_block_on_grid(row, col, yellow_fd)
                    elif grid[row][col] == 'P':
                        self.draw_block_on_grid(row, col, purple_fd)
                    elif grid[row][col] == 'O':
                        self.draw_block_on_grid(row, col, orange_fd)
                    elif grid[row][col] == 'T':
                        self.draw_block_on_grid(row, col, turq_fd)

    def convert_game_colors_to_pygame(self, game_colors: list) -> list:
        """converts list of color letters into a list of ints representing the colors"""
        temp_list = []
        for i in range(len(game_colors)):
            if game_colors[i] == 'B':
                temp_list.append(0)
            elif game_colors[i] == 'G':
                temp_list.append(1)
            elif game_colors[i] == 'R':
                temp_list.append(2)
            elif game_colors[i] == 'Y':
                temp_list.append(3)
            elif game_colors[i] == 'P':
                temp_list.append(4)
            elif game_colors[i] == 'O':
                temp_list.append(5)
            elif game_colors[i] == 'T':
                temp_list.append(6)
        return temp_list




if __name__ == '__main__':
    Columns().run()
