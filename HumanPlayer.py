from Player import Player


class HumanPlayer(Player):
    def __init__(self, playerNum: int, depth=5):
        super().__init__(playerNum, depth)