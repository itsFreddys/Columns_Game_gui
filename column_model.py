# model
import copy
import features as f

import pygame
import random

Empty = 0

_PLAYER_WIDTH = 0.167
_PLAYER_HEIGHT = 0.076923
_PLAYER_SPEED = 0.167
_FALL_SPEED = 0.076923
Falling = True
BLUE = pygame.Color(0, 102, 204)
GREEN = pygame.Color(0, 200, 128)
RED = pygame.Color(158, 8, 8)
yellow = pygame.Color(245,221,66)
purple = pygame.Color(182,66,245)
orange = pygame.Color(245,158,66)
light_blue = pygame.Color(66,164,245)
solid_colors = [BLUE,GREEN,RED,yellow,purple,orange,light_blue]


class Fallen:
    def __init__(self, column: int):
        self._column = column

        self._actual_column = self._column + 1

        top_left_x = 100 * self._column/600
        top_left_y = 0

        self._fall_counter = 0
        self._fixed_status = Falling
        self._top_left = (top_left_x, top_left_y)
        self._border = 5
        self._color_selected = False
        self._color1 = None
        self._color2 = None
        self._color3 = None
        self._counter = 0
        self._press_counter = 0

    def get_fall_counter(self) -> int:
        """returns the values of the fall counter"""
        return self._fall_counter

    def increase_fall_counter(self) -> None:
        """increase thes fall counter by one"""
        self._fall_counter += 1

    def reset_fall_counter(self) -> None:
        """resets fall counter to 0"""
        self._fall_counter = 0

    def get_press_counter(self) -> int:
        """returns the value of the press counter"""
        return self._press_counter

    def increase_press_counter(self) -> None:
        """increases press counter by 1"""
        self._press_counter += 1

    def reset_press_counter(self) -> None:
        """resets the press counter to 0"""
        self._press_counter = 0

    def get_column(self) -> int:
        """returns the value of the column"""
        return self._column

    def get_border_rad(self) -> int:
        """returns the values of the border width"""
        return self._border

    def set_border_rad(self, val) -> None:
        """sets the value of the border radius"""
        self._border = val

    def color_stat(self) -> bool:
        """returns the status if colors have been selected"""
        return self._color_selected

    def change_fix_status(self) -> None:
        """changes the status to false for fixed status"""
        self._fixed_status = False

    def get_fall_stat(self) -> bool:
        """returns the boolean value of the fixed status attribute"""
        return self._fixed_status

    def set_color1(self, color) -> None:
        """sets the color for color1"""
        self._color1 = color

    def set_color2(self, color) -> None:
        """sets the color for color2"""
        self._color2 = color

    def set_color3(self, color) -> None:
        """sets the color for color3"""
        self._color3 = color

    def get_color1(self) -> int:
        """returns int value of color1"""
        return self._color1

    def get_color2(self) -> int:
        """returns int value of color2"""
        return self._color2

    def get_color3(self) -> int:
        """returns int value of color3"""
        return self._color3

    def get_fix_status(self) -> bool:
        """returns the boolean value of fixed status"""
        return self._fixed_status

    def top_left(self) -> tuple[float, float]:
        """returns the x and y position of top left corner of object"""
        return self._top_left

    def width(self) -> float:
        """"returns the block's width"""
        return _PLAYER_WIDTH

    def height(self) -> float:
        """returns the block's height"""
        return _PLAYER_HEIGHT


    # Movement
    def move_left(self) -> None:
        """moves block to the left"""
        self._move(-_PLAYER_SPEED, 0)

    def move_right(self) -> None:
        """moves block to the right"""
        self._move(_PLAYER_SPEED, 0)

    def move_down(self, bottom: int) -> None:
        """moves the block downward"""
        self._move_down_to_bottom(0, _FALL_SPEED, bottom)

    def _move_down_to_bottom(self, delta_x: float, delta_y: float, bottom: int) -> None:
        """moves block downward with respect to the bottom most on grid"""
        if not self.get_fix_status(): return

        tl_x, tl_y = self._top_left

        new_x = tl_x + delta_x
        new_y = tl_y + delta_y

        if bottom == 12:
            if new_y >= 1 - self.height() / 2:
                self._counter += 20
                self.set_border_rad(self._counter)
                if self._counter >= 50:
                    self.change_fix_status()
                return None
        elif bottom == 11:
            if new_y >= 1 - 2 * self.height():
                self._counter += 20
                self.set_border_rad(self._counter)
                if self._counter >= 50:
                    self.change_fix_status()
        elif bottom == 10:
            if new_y >= 1 - 5 * self.height():
                self._counter += 20
                self.set_border_rad(self._counter)
                if self._counter >= 50:
                    self.change_fix_status()
        elif bottom == 9:
            if new_y >= 1 - 5.7 * self.height():
                self._counter += 20
                self.set_border_rad(self._counter)
                if self._counter >= 50:
                    self.change_fix_status()
        elif bottom == 8:
            if new_y >= 1 - 7 * self.height():
                self._counter += 20
                self.set_border_rad(self._counter)
                if self._counter >= 50:
                    self.change_fix_status()
        elif bottom == 7:
            if new_y >= 1 - 8 * self.height():
                self._counter += 20
                self.set_border_rad(self._counter)
                if self._counter >= 50:
                    self.change_fix_status()
        elif bottom == 6:
            if new_y >= 1 - 9 * self.height():
                self._counter += 20
                self.set_border_rad(self._counter)
                if self._counter >= 50:
                    self.change_fix_status()
        elif bottom == 5:
            if new_y >= 1 - 10 * self.height():
                self._counter += 20
                self.set_border_rad(self._counter)
                if self._counter >= 50:
                    self.change_fix_status()
        elif bottom == 4:
            if new_y >= 1 - 11 * self.height():
                self._counter += 20
                self.set_border_rad(self._counter)
                if self._counter >= 50:
                    self.change_fix_status()
        elif bottom == 3:
            if new_y >= 1 - 12 * self.height():
                self._counter += 20
                self.set_border_rad(self._counter)
                if self._counter >= 50:
                    self.change_fix_status()
        elif bottom == 2:
            if new_y >= 1 - 14 * self.height():
                self._counter += 20
                self.set_border_rad(self._counter)
                if self._counter >= 50:
                    self.change_fix_status()
                    raise f.OutOfBounds()
        elif bottom == 1:
            if new_y >= 1 - 15 * self.height():
                self._counter += 20
                self.set_border_rad(self._counter)
                if self._counter >= 50:
                    self.change_fix_status()
                    raise f.OutOfBounds()
        elif bottom == -1 or bottom == 0:
            raise f.OutOfBounds()

        self._top_left = (new_x, new_y)

    def _move(self, delta_x: float, delta_y: float) -> None:
        """moves the block left or right"""
        if not self.get_fix_status(): return

        tl_x, tl_y = self._top_left

        new_x = tl_x + delta_x
        new_y = tl_y + delta_y

        # left
        if new_x <= 0.0:
            new_x = 0.001
        # right
        elif new_x >= 0.84:
            new_x = 1 - _PLAYER_WIDTH

        self._top_left = (new_x, new_y)

    def rotate(self) -> None:
        """ causes the rotation of the block's colors"""
        temp_color1 = self.get_color2()
        temp_color2 = self.get_color3()
        temp_color3 = self.get_color1()
        self.set_color1(temp_color1)
        self.set_color2(temp_color2)
        self.set_color3(temp_color3)





class Grid:
    def __init__(self):
        grid = self.empty_grid(13,6)
        self._grid = grid

    def get_grid(self) -> list[list]:
        """returns the grid"""
        return self._grid

    def empty_grid(self,rows: int, columns: int) -> list[list[int]]:
        """
        Creates an empty grid with specified columns and rows
        returns a list[list] of ints.
        """
        temp_grid = []
        for row in range(rows):
            temp_inner = []
            for column in range(columns):
                temp_inner.append(Empty)
            temp_grid.append(temp_inner)
        return temp_grid

    def update_grid(self,grid: list[list]) -> None:
        """updates the grid attribute with grid passed in"""
        self._grid = copy.deepcopy(grid)




class GameState:
    def __init__(self, column: int):
        self._fallen1 = Fallen(column)

    def player(self) -> Fallen:
        return self._fallen1
