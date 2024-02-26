import features as f
import copy
FALLEN = True
FREEZE = False
FROZEN = False
EMPTY = 0


class Fallen:
    def __init__(self, column, colors):
        self._fallen_block_colors = self.convert_colors_to_fallen(colors)
        self._colors = colors.copy()
        self._column = column
        self._state = FALLEN
        self._freeze_state = FALLEN
        self._top = None
        self._mid = None
        self._bottom = None
        self._fit = True
        self._moved = False

    def get_moved_stat(self) -> bool:
        """returns the boolean status if object was moved"""
        return self._moved

    def get_fit_status(self) -> bool:
        """returns the status is piece fits"""
        return self._fit

    def get_fallen_piece(self, row: int) -> int:
        """
        returns the value of the status
        """
        return self._fallen_block_colors[row]

    def get_status(self) -> bool:
        """
        returns the value of the status
        """
        return self._state

    def get_freeze_status(self) -> bool:
        """
        returns the value of the status
        """
        return self._freeze_state

    def get_column(self) -> int:
        """
        returns the value of the status
        """
        return self._column

    def get_top(self) -> tuple:
        """
        returns the value of the top
        """
        return self._top

    def get_mid(self) -> tuple:
        """
        returns the value of the mid
        """
        return self._mid

    def get_bottom(self) -> tuple:
        """
        returns the value of the bottom
        """
        return self._bottom

    def assign_top(self, points: tuple) -> None:
        """
        assigns top with points that specify its location on
            the game grid
        """
        self._top = points

    def assign_mid(self, points: tuple) -> None:
        """
        assigns mid with points that specify its location on
            the game grid
        """
        self._mid = points

    def assign_bottom(self, points: tuple) -> None:
        """
        assigns bottom with points that specify its location on
            the game grid
        """
        self._bottom = points

    def assign_column(self, column: int) -> None:
        """
        assigns bottom with points that specify its location on
            the game grid
        """
        self._column = column

    def convert_colors_to_fallen(self, colors: list) -> list:
        """
        coverts users selected colors and makes them into a fallen block
        returns a list of all the colors in fallen format
        """
        temp_list = colors.copy()
        for i in range(len(colors)):
            var = temp_list[i]
            temp_list[i] = "[" + var + "]"
        return temp_list

    def move_left_grid(self, grid: list[list], column_val: int) -> list[list]:
        """
                moves the fallen block left if available
                return the grid updated if move was made
                """
        grid_copy = copy.deepcopy(grid)
        for row in range(len(grid) - 1, -1, -1):
            if not grid[row][column_val] != 0: continue
            if grid[row][column_val].startswith('['):
                column_val_left = column_val - 1
                if grid[row][column_val - 1] == EMPTY and column_val - 1 >= 0:
                    grid_copy[row][column_val - 1] = grid[row][column_val]
                    grid_copy[row][column_val] = EMPTY
                    self.assign_column(column_val_left)
                    self._moved = True
                else:
                    return grid
        return grid_copy

    def move_right_grid(self, grid: list[list], column_val: int) -> list[list]:
        """
                moves the fallen block right if available
                return the grid updated if move was made
                """
        grid_copy = copy.deepcopy(grid)
        for row in range(len(grid) - 1, -1, -1):
            if not grid[row][column_val] != 0: continue
            if grid[row][column_val].startswith('['):
                column_val_right = column_val + 1
                if not f.is_valid_column(grid, column_val_right): return grid
                if column_val + 1 <= len(grid[0]) and grid[row][column_val + 1] == EMPTY:
                    grid_copy[row][column_val + 1] = grid[row][column_val]
                    grid_copy[row][column_val] = EMPTY
                    self.assign_column(column_val_right)
                    self._moved = True
                else:
                    return grid
        return grid_copy

    def make_all_fallen_freeze(self,grid, column) -> list[list]:
        """if any fallen piece is not frozen, then this freezes all fallen
            it just reassures their all frozen"""
        grid_copy = copy.deepcopy(grid)
        counter = 0
        for row in range(len(grid) - 1, -1, -1):
            if grid[row][column] != 0 and grid[row][column].startswith('['):
                counter += 1
                temp_var = grid[row][column]
                grid_copy[row][column] = "|" + temp_var[1] + "|"
        if counter >= 1:
            self._fit = False
        return grid_copy

    def drop_down_fallen(self, old_grid: list[list], column: int) -> list[list[int]]:
        """
        drops only fallen pieces, one iteration at a time
        returns an update grid with drop iteration
        """
        if not self.get_status():
            return old_grid

        grid_copy = copy.deepcopy(old_grid)
        bottom_most = f.find_bottom_most(old_grid, column)

        row_counter = 0
        for row in range(len(old_grid) - 1, -1, -1):
            row_counter += 1
            if old_grid[row][column] != 0 and row < bottom_most +1:
                if old_grid[row][column].startswith('['):
                    grid_copy[row + 1][column] = old_grid[row][column]
                    grid_copy[row][column] = EMPTY

        bottom_most_temp = f.find_bottom_most(grid_copy,column)
        if bottom_most_temp == -1:
            grid_copy = self.freeze_fallen(grid_copy,column)
            return grid_copy
        if bottom_most_temp != bottom_most:
            grid_copy = self.freeze_fallen(grid_copy, column)
            return grid_copy
        return grid_copy

    def fallen_fit(self, grid: list[list], column: int) -> bool:
        """Checks if all the fallen block has been placed in the grid
            returns false if not all three of block pieces are inside"""
        fallen_size = 3
        fallen_counter = 0
        for row in range(len(grid) - 1, -1, -1):
            if grid[row][column] != 0:
                if grid[row][column].startswith('[') or grid[row][column].startswith('|'):
                    fallen_counter += 1
        if fallen_counter >= fallen_size:
            return True
        else:
            return False

    def freeze_fallen(self, grid: list[list], column: int) -> list[list]:
        """alters the fallen block and create it into a block that is about to freeze
            returns an updated grid with new freezing blocks"""
        grid_copy = copy.deepcopy(grid)
        for row in range(len(grid) - 1, -1, -1):
            if grid[row][column] != 0 and grid[row][column].startswith('['):
                temp_var = grid[row][column]
                grid_copy[row][column] = "|" + temp_var[1] + "|"
        self._freeze_state = False
        return grid_copy

    def unfreeze_piece(self, grid: list[list], column) -> list[list]:
        """unfreezes the fallen pieces and creates them as permanent pieces
            returns updated grid"""
        grid_copy = copy.deepcopy(grid)
        for row in range(len(grid) - 1, -1, -1):
            if grid[row][column] != 0 and grid[row][column].startswith('|'):
                temp_var = grid[row][column]
                grid_copy[row][column] = temp_var[1]
        return grid_copy

    def get_position_of_fallen(self, grid: list[list]) -> None:
        """collects the location of the fallen pieces and
            updates the fallen attributes with the collected data"""
        col = self.get_column()
        temp_list = []
        for i in range(len(grid)):
            if grid[i][col] != 0:
                if grid[i][col].startswith('[') or grid[i][col].startswith('|'):
                    temp_list.append((i, col))
        if len(temp_list) == 3:
            self.assign_top(temp_list[0])
            self.assign_mid(temp_list[1])
            self.assign_bottom(temp_list[2])

        if len(temp_list) == 2:
            self.assign_mid(temp_list[0])
            self.assign_bottom(temp_list[1])

        if len(temp_list) == 1:
            self.assign_bottom(temp_list[0])

    def rotate_fallen(self, grid: list[list]) -> list[list]:
        """rotates the fallen block pieces
            returns updated grid"""
        temp_grid = copy.deepcopy(grid)
        self.get_position_of_fallen(grid)
        temp_top = self.get_top()
        temp_mid = self.get_mid()
        temp_bottom = self.get_bottom()

        temp_grid[temp_top[0]][temp_top[1]] = grid[temp_bottom[0]][temp_bottom[1]]
        temp_grid[temp_mid[0]][temp_mid[1]] = grid[temp_top[0]][temp_top[1]]
        temp_grid[temp_bottom[0]][temp_bottom[1]] = grid[temp_mid[0]][temp_mid[1]]

        return temp_grid

    def change_stat(self) -> None:
        """changes the status from fallen to frozen,
            signifies that the block is unalterable"""
        self._state = FROZEN



def run():
    pass

if __name__ == '__main__':
    run()
