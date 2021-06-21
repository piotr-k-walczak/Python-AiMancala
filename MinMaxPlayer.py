import time
from copy import deepcopy
from Board import Board
from Heuristic import simple_score_comparison
from Player import Player


class MinMaxPlayer(Player):
    def __init__(self, playerNum: int, depth=0, heuristics=simple_score_comparison):
        super().__init__(playerNum, depth, heuristics)

    def choose_move(self, board):
        start = time.time()
        m, s, cm = self.max_value(board, self.depth, self)
        end = time.time()
        self.time_counter += end - start
        self.move_counter += 1
        self.checked_moves_counter += cm
        return m

    def max_value(self, board: Board, depth: int, turn):
        if board.is_over():
            return -1, turn.score(board), 1
        move = -1
        best_score = None
        legal_moves = board.get_legal_moves_for_player(self)
        counted_moves = 0
        for m in legal_moves:
            if depth == 0:
                return -1, turn.score(board), 1
            enemy = MinMaxPlayer(self.enemyID, self.depth)
            nextBoard = deepcopy(board)
            nextBoard.move(self, m)
            em, s, cm = enemy.min_value(nextBoard, depth - 1, turn)
            counted_moves += cm
            if best_score is None or s > best_score:
                move = m
                best_score = s
        return move, best_score, counted_moves + len(legal_moves)

    def min_value(self, board, depth, turn):
        if board.is_over():
            return -1, turn.score(board), 1
        move = -1
        best_score = None
        legal_moves = board.get_legal_moves_for_player(self)
        counted_moves = 0
        for m in legal_moves:
            if depth == 0:
                return -1, turn.score(board), 1
            enemy = MinMaxPlayer(self.enemyID, self.depth)
            nextBoard = deepcopy(board)
            nextBoard.move(self, m)
            em, s, cm = enemy.max_value(nextBoard, depth - 1, turn)
            counted_moves += cm
            if best_score is None or s < best_score:
                move = m
                best_score = s
        return move, best_score, counted_moves + len(legal_moves)

    def __str__(self):
        return str(self.playerID)

