import time
from copy import deepcopy

from Heuristic import simple_score_comparison
from Player import Player


class AbPlayer(Player):
    def __init__(self, playerNum: int, depth=0, heuristics=simple_score_comparison):
        super().__init__(playerNum, depth, heuristics)

    def choose_move(self, board):
        start = time.time()
        m, s, cm = self.move(board, self.depth)
        end = time.time()
        self.time_counter += end - start
        self.move_counter += 1
        self.checked_moves_counter += cm
        return m

    def move(self, board, depth):
        move = -1
        alpha = float('-inf')
        beta = float('inf')
        score = None
        legal_moves = board.get_legal_moves_for_player(self)
        counted_moves = 0
        for m in legal_moves:
            if depth == 0:
                return m, self.score(board), 1
            enemy = AbPlayer(self.enemyID, self.depth)
            nextBoard = deepcopy(board)
            nextBoard.move(self, m)
            em, s, cm = enemy.min_value(nextBoard, depth - 1, self, alpha, beta)
            counted_moves += cm
            if score is None or s > score:
                move = m
                score = s
            alpha = max(score, alpha)
        return move, -1, counted_moves

    def max_value(self, board, depth, turn, alpha, beta):
        if board.is_over():
            return -1, turn.score(board), 1
        best_score = None
        legal_moves = board.get_legal_moves_for_player(self)
        counted_moves = 0
        for m in legal_moves:
            if depth == 0:
                return -1, turn.score(board), 1
            enemy = AbPlayer(self.enemyID, self.depth)
            nextBoard = deepcopy(board)
            nextBoard.move(self, m)
            em, s, cm = enemy.min_value(nextBoard, depth - 1, turn, alpha, beta)
            counted_moves += cm + 1
            if best_score is None or s > best_score:
                best_score = s
            if best_score is not None and best_score >= beta:
                return -1, best_score, counted_moves
            alpha = max(best_score, alpha)
        return -1, best_score, counted_moves

    def min_value(self, board, depth, turn, alpha, beta):
        if board.is_over():
            return -1, turn.score(board), 1
        best_score = None
        legal_moves = board.get_legal_moves_for_player(self)
        counted_moves = 0
        for m in legal_moves:
            if depth == 0:
                return -1, turn.score(board), 1
            enemy = AbPlayer(self.enemyID, self.depth)
            nextBoard = deepcopy(board)
            nextBoard.move(self, m)
            em, s, cm = enemy.max_value(nextBoard, depth - 1, turn, alpha, beta)
            counted_moves += cm + 1
            if best_score is None or s > best_score:
                best_score = s
            if best_score is not None and best_score <= alpha:
                return -1, best_score, counted_moves
            beta = min(beta, best_score)
        return -1, best_score, counted_moves

    def __str__(self):
        return str(self.playerID)

