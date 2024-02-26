from game_class import Game
import features as f


class User:
    def __init__(self):
        self._row = 13
        self._column = 6
        self._grid = None
        self.create_my_grid()
        self._game = None

    def create_my_grid(self) -> None:
        """creates the game grid using user type selection"""
        self._grid = f.empty_grid(self._row,self._column)
        # f.print_grid1(self._grid)

    def create_game(self) -> None:
        """creates an object of class Game
            assigns object to user attribute game"""
        self._game = Game(self._grid)
    def game(self):
        return self._game

    def play_game(self) -> None:
        """cycles through the game until quit or game over or error"""
        while True:
            self.create_game()
            self._game.cycle_game()
            self._grid = self._game.get_grid()
            if self.check_if_list_is_full(): raise f.OutOfBounds()
            # f.print_grid1(self._grid)

    def play_game_over_pygame(self) -> None:
        """cycles through the game using pygame until quit is triggered"""
        self.create_game()
        self._game.cycle_game_in_pygame()
        self._grid = self._game.get_grid()
        # if self.check_if_list_is_full(): raise f.OutOfBounds()
        # f.print_grid1(self._grid)

    def check_if_list_is_full(self) -> bool:
        """Checks if the grid is full, causing a game over"""
        if any(0 in nested_list for nested_list in self._grid):
            return False
        else:
            return True



def run():
    user1 = User()
    user1.play_game()




if __name__ == '__main__':
    run()
