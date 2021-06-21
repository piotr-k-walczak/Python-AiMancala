def simple_score_comparison(board, playerID: int, enemyID: int):
    return board.scores[playerID - 1] - board.scores[enemyID - 1]


def beating_comparison(board, playerID: int, enemyID: int):
    return (board.scores[playerID - 1] - board.scores[enemyID - 1]) - sum(board.get_players_holes(playerID))