import copy
import random
import features as f
from fallen_class import Fallen

colors_list = ('B', 'G', 'R', 'Y', 'P', 'O', 'T')


class Game:
    def __init__(self, grid):
        self._grid = copy.deepcopy(grid)
        self._counter = -1
        self._game_state = True
        self._fallen = None
        self._column = None
        self._colors = None
        self.collect_fallen_input()
        self._matches = False

    def get_frozen_status(self) -> bool:
        """returns the boolean value of fallen status"""
        return self._fallen.get_status()

    def set_column(self, col: int) -> None:
        """sets the column with passed in value"""
        self._column = col

    def get_game_column(self) -> int:
        """returns column"""
        return self._column

    def get_colors(self) -> list:
        """returns a list of colors"""
        return self._colors

    def get_grid(self) -> list[list]:
        """returns grid"""
        return self._grid

    def get_game_state(self) -> bool:
        """returns game state status"""
        return self._game_state

    def get_fallen_state(self) -> bool:
        """returns fallen status"""
        return self._fallen.get_status()

    def change_game_state(self) -> None:
        """changes game state status to false"""
        self._game_state = False

    def collect_fallen_input(self) -> None:
        """collects input from user for fallen object column and colors"""
        if self._counter != -1:
            self._counter = -1
        rand_column = random.randint(0,5)
        self._column = rand_column

        color1 = random.choice(colors_list)
        color2 = random.choice(colors_list)
        color3 = random.choice(colors_list)
        self._colors = [color1,color2,color3]

        self._fallen = Fallen(rand_column,self.get_colors())
        self._grid = f.append_to_grid(
            self._grid,
            self._fallen.get_column(),
            self._fallen.get_fallen_piece(self._counter)
        )
        self._counter = self._counter - 1

    def unfreeze_check_matches(self) -> None:
        """unfreezes all fallen pieces and checks for matches
            if matches are found then print grid with matches"""
        temp_grid = self.get_grid()
        temp_col = self._fallen.get_column()
        self._grid = self._fallen.unfreeze_piece(temp_grid, temp_col)
        match = f.check_matching_seq(self._grid)
        if type(match) != list:
            pass
            # f.print_grid1(self._grid)
        else:
            self._grid = f.matches_on_grid(self._grid, match)
            # if self._matches:
            #     f.input_pause()
            # f.print_grid1(self._grid)
            self._grid = f.clear_matches(self._grid, match)
            self._grid = f.drop_down_all(self._grid)
            # f.input_pause()
            self.unfreeze_check_matches()
            self._matches = True

    def cycle_game(self) -> None:
        """cycles through the game and its methods
            to have the game run"""
        while self.get_game_state():
            if self._fallen.get_freeze_status():
                if self._counter >= -3:
                    self._grid = self._fallen.drop_down_fallen(self.get_grid(), self._fallen.get_column())
                    # f.print_grid1(self.get_grid())
                    col = self._fallen.get_column()
                    fallen_piece = self._fallen.get_fallen_piece(self._counter)
                    self._grid = f.append_to_grid(self._grid, col, fallen_piece)
                    self._counter = self._counter - 1
                else:
                    self._grid = self._fallen.drop_down_fallen(self._grid, self._fallen.get_column())
                    # f.print_grid1(self.get_grid())
            else:
                self.unfreeze_check_matches()
                self.change_game_state()

    def cycle_game_in_pygame(self) -> None:
        """cycles through the game and its methods
            to have the game run"""
        if self.get_game_state():
            if self._fallen.get_freeze_status():
                if self._counter >= -3:
                    self._grid = self._fallen.drop_down_fallen(self.get_grid(), self._fallen.get_column())
                    col = self._fallen.get_column()
                    fallen_piece = self._fallen.get_fallen_piece(self._counter)
                    self._grid = f.append_to_grid(self._grid, col, fallen_piece)
                    self._counter = self._counter - 1
                else:
                    self._grid = self._fallen.drop_down_fallen(self._grid, self._fallen.get_column())
                    # f.print_grid1(self.get_grid())
            else:
                self.unfreeze_check_matches()
                self.change_game_state()

    def move_fallen_right(self) -> None:
        """moves the fallen piece to the right by one if available"""
        self._grid = self._fallen.move_right_grid(self.get_grid(), self.get_game_column())
        if self._fallen._moved:
            self.set_column(self.get_game_column() + 1)

    def move_fallen_left(self) -> None:
        """moves the fallen piece to the left by one if available"""
        self._grid = self._fallen.move_left_grid(self.get_grid(), self.get_game_column())
        if self._fallen._moved:
            self.set_column(self.get_game_column() - 1)

    def rotate_block(self) -> None:
        """rotates the colors of the fallen block"""
        self._grid = self._fallen.rotate_fallen(self._grid)




def run():
    grid = f.empty_grid(13, 6)
    # grid[3][0] = 'Z'
    # grid[3][1] = 'Z'
    # #grid[3][2] = 'Z'
    # grid[2][0] = 'X'
    # grid[2][1] = 'X'
    #grid[1][1] = 'b'
    #grid[2][2] = 'X'
    f.print_grid1(grid)
    game1 = Game(grid)
    game1.cycle_game()
    # while game1.get_game_state():
    #     if game1.get_fallen_state():
    #         game1.collect_actions()
    #     else:
    #         game1.collect_actions()
    #         game1.unfreeze_check_matches()
    #         f.print_grid1(game1.get_grid())
    #         game1.change_game_state()


if __name__ == '__main__':
    run()

