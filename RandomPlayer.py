from random import choice
from Board import Board
from Heuristic import simple_score_comparison
from Player import Player


class RandomPlayer(Player):
    def __init__(self, playerNum: int, depth=0, heuristics=simple_score_comparison):
        super().__init__(playerNum, depth, heuristics)

    def choose_move(self, board: Board):
        move = choice(board.get_legal_moves_for_player(self))
        return move

