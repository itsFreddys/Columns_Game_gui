import copy
Empty = 0
Freeze = -1


class OutOfBounds(Exception):
    def __init__(self):
        print("GAME OVER")
        quit()


class PlayerQuit(Exception):
    def __init__(self):
        quit()


def print_grid1(grid) -> None:
    """print the grid in any condition it is in"""
    grid_copy = copy.deepcopy(grid)
    for row in range(len(grid_copy)):
        print(end='|')
        for column in range(len(grid_copy[row])):
            if column == len(grid_copy[row]) - 1:
                if grid_copy[row][column] != 0:
                    if grid_copy[row][column].startswith('[') \
                            or grid_copy[row][column].startswith('|') \
                            or grid_copy[row][column].startswith('*'):
                        print(f"{grid_copy[row][column]}", end='')
                    else:
                        print(f" {grid_copy[row][column]}", end=' ')
                else:
                    print('  ', end=' ')
            elif grid_copy[row][column] != 0:
                if grid_copy[row][column].startswith('[') \
                        or grid_copy[row][column].startswith('|') \
                        or grid_copy[row][column].startswith('*'):
                    print(f"{grid_copy[row][column]}", end='')
                else:
                    print(f" {grid_copy[row][column]}", end=' ')
            else:
                print('  ', end=' ')
        print('|')
    print('', '---' * len(grid_copy[0]),"")


def append_to_grid(grid, column, value) -> list[list[int]]:
    """added value onto grid if space is available
        returns updated grid"""
    grid_copy = copy.deepcopy(grid)
    if grid[0][column] == 0:
        grid_copy[0][column] = value
    return grid_copy


def empty_grid(rows: int, columns: int) -> list[list[int]]:
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


def fallen_fit(grid, column) -> bool:
    """checks if fallen piece fits in specified column"""
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


def drop_down_all(old_grid: list[list]) -> list[list[int]]:
    """
    drops only fallen pieces, one iteration at a time
    """
    grid_copy = copy.deepcopy(old_grid)
    for row in range(len(old_grid) - 1, -1, -1):
        for col in range(len(old_grid[0])):
            bottom_most = find_bottom_most(grid_copy, col)
            if old_grid[row][col] != 0 and old_grid[row][col].isalpha() and row <= bottom_most:
                grid_copy[bottom_most][col] = old_grid[row][col]
                grid_copy[row][col] = Empty

    return grid_copy


def find_bottom_most(grid: list[list], column_val: int) -> int:
    """finds the bottom most value in the specified column
        returns bottom most or -1 if no bottom"""
    for i in range(len(grid) - 1, -1, -1):
        if grid[i][column_val] == Empty:
            return i
    return -1


def check_matching_seq(grid: list[list]) -> list or int:
    """initiates the search for matches, returns a list if there are matches
        else returns 0"""
    match = 0

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            match = three_in_a_row(grid, col, row)
            if type(match) == list:
                return match
    return match


def three_in_a_row(grid: list[list], col: int, row: int) -> list or int:
    """checks for matches of length 3, if matches found,
        returns list of matches, else 0"""
    starting_point = grid[row][col]
    matches = 0
    match_list = [(row, col)]

    if starting_point == Empty:
        return matches
    else:
        if horizontal_match(grid, starting_point, row, col):
            match_list.append((row, col + 1))
            match_list.append((row, col + 2))
        elif vertical_match(grid, starting_point, row, col):
            match_list.append((row + 1, col))
            match_list.append((row + 2, col))
        else:
            return matches

        temp_match = check_for_stragglers(grid, match_list, starting_point, row, col)

        return temp_match


def check_for_stragglers(grid: list[list], match_list: list, starting_point: str, row: int, col: int) -> list[tuple]:
    """checks for any more matches that are beyond the 3 matches
        returns updated matching list"""
    temp_copy = copy.deepcopy(match_list)
    for i in range(0, len(grid[0]) - 3):
        delta_column = 3 + i
        if starting_point == grid[row][delta_column]:
            temp_copy.append((row, delta_column))

    for i in range(1, len(grid) - 3):
        delta_row = 3 + i
        if starting_point == grid[delta_row][col]:
            temp_copy.append((delta_row, col))

    return temp_copy


def horizontal_match(grid: list[list], starting_point: str, row: int, column: int) -> bool:
    """checks for matches of 3 horizontally, returns true if found"""
    statement = None  # cycles from true and false
    for i in range(1, 3):
        if not is_valid_column(grid, column + i): return False
        if starting_point == grid[row][column + i] and grid[row][column + i] != 0:
            statement = True
        else:
            return False
    return statement


def vertical_match(grid: list[list], starting_point: str, row: int, column: int) -> bool:
    """checks for matches of 3 vertically, returns true if found"""
    statement = None
    for i in range(1, 3):
        if not is_valid_row(grid, row + i): return False
        if starting_point == grid[row + i][column] and grid[row + i][column] != 0:
            statement = True
        else:
            return False
    return statement


def matches_on_grid(grid: list[list], matches: list[tuple]) -> list[list]:
    """updates the grid with the matched values applies the print formatting
        returns updated grid"""
    grid_copy = copy.deepcopy(grid)
    match_color = grid[matches[0][0]][matches[0][1]]
    for i in range(len(matches)):
        row = matches[i][0]
        col = matches[i][1]
        grid_copy[row][col] = '*' + match_color + '*'
    return grid_copy


def clear_matches(grid: list[list], matches: list[tuple]) -> list[list]:
    """removes all matches from grid
        returns updated grid"""
    grid_copy = copy.deepcopy(grid)
    for i in range(len(matches)):
        row = matches[i][0]
        col = matches[i][1]
        grid_copy[row][col] = Empty
    return grid_copy


def is_valid_column(grid: list[list], column: int) -> bool:
    """returns true if column is valid, else false"""
    return 0 <= column < len(grid[0])


def is_valid_row(grid: list[list], row: int) -> bool:
    """returns true if row is valid, else false"""
    return 0 <= row < len(grid)





def run():
    fall_str = "F 3 X Y Z"
    fallen_piece = ['[X]', '[Y]', '[Z]']

    grid_check = empty_grid(5, 4)

    grid_check[0][1] = 'b'
    grid_check[4][1] = 'A'
    grid_check[3][1] = 'A'
    grid_check[2][1] = 'A'
    grid_check[1][1] = 'A'

    grid_check[2][3] = 'b'
    grid_check[2][2] = 'b'
    grid_check[2][1] = 'A'
    grid_check[2][0] = 'b'

    # grid_check[3][3] = 'b'
    # grid_check[3][2] = 'c'
    # grid_check[3][1] = 'd'
    # grid_check[3][0] = 'e'
    print_grid1(grid_check)
    grid_check = drop_down_all(grid_check)

    match = check_matching_seq(grid_check)
    if type(match) == list:
        grid_check = matches_on_grid(grid_check, match)
    print_grid1(grid_check)
    if type(match) == list:
        grid_check = clear_matches(grid_check, match)
    grid_check = drop_down_all(grid_check)
    print_grid1(grid_check)

    match = check_matching_seq(grid_check)
    if type(match) == list:
        grid_check = matches_on_grid(grid_check, match)
    print_grid1(grid_check)
    if type(match) == list:
        grid_check = clear_matches(grid_check, match)
    grid_check = drop_down_all(grid_check)
    print_grid1(grid_check)


if __name__ == '__main__':
    run()
