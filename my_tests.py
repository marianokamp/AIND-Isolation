import isolation
import game_agent
import sample_players

import unittest

class TestIsolation(unittest.TestCase):

#    def setUp(self):
#        self.grid = s.create_grid()


    def setup_board(self):
        player1 = sample_players.RandomPlayer()
        player2 = sample_players.RandomPlayer()
        game = isolation.Board(player1, player2)

        game.apply_move((3, 2)) #1
        game.apply_move((4, 2))

        game.apply_move((2, 2)) #1
        game.apply_move((5, 2))

        game.apply_move((1, 2)) #1
        game.apply_move((6, 2))

        game.apply_move((0, 2)) #1
        game.apply_move((6, 3))

        game.apply_move((0, 1)) #1
        game.apply_move((6, 4))

        '''
     0   1   2   3   4   5   6
0  |   | 1 | - |   |   |   |   |
1  |   |   | - |   |   |   |   |
2  |   |   | - |   |   |   |   |
3  |   |   | - |   |   |   |   |
4  |   |   | - |   |   |   |   |
5  |   |   | - |   |   |   |   |
6  |   |   | - | 2 |   |   |   |
        '''

        return game

    def test_heuristics_lmbl(self):

        game = self.setup_board()

        print(game.to_string())
        score = game_agent.custom_score(game, game.active_player, "lmlb")
        assert(score == -2)

    def test_heuristics_ds(self):

        game = self.setup_board()

        print(game.to_string())
        score = game_agent.custom_score(game, game.active_player, "ds")
        assert(score == -2)

    def test_heuristics_schadenfreude(self):

        game = self.setup_board()

        print(game.to_string())
        score = game_agent.custom_score(game, game.active_player, "schadenfreude")
        assert(score == -2)

if __name__ == '__main__':
    unittest.main()
