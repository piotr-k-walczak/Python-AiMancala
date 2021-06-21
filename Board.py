from typing import List
from Config import P2_SCORE, P1_SCORE, P1_HOLES, P2_HOLES, HOLES
from Player import Player


class Board:
    def __init__(self):
        self.scores: List[int] = [P1_SCORE, P2_SCORE]
        self.holesPlayer1: List[int] = P1_HOLES
        self.holesPlayer2: List[int] = P2_HOLES

    def reset(self):
        self.scores = [0, 0]
        self.holesPlayer1 = [4, 4, 4, 4, 4, 4]
        self.holesPlayer2 = [4, 4, 4, 4, 4, 4]

    def legal_move(self, player: Player, hole: int):
        playerHoles = self.get_players_holes(player.playerID)
        return 0 < hole <= len(playerHoles) and playerHoles[hole - 1] > 0

    def get_legal_moves_for_player(self, player: Player):
        playerHoles = self.get_players_holes(player.playerID)
        return [(m + 1) for m in range(len(playerHoles)) if playerHoles[m] > 0]

    def move(self, player: Player, currentHole: int):
        holes = self.get_players_holes(player.playerID)
        enemyHoles = self.get_players_holes(player.enemyID)

        startHoles = holes
        pickedUpStones = holes[currentHole - 1]
        holes[currentHole - 1] = 0

        currentHole += 1
        playAgain = False
        while pickedUpStones > 0:
            playAgain = False
            while currentHole <= len(holes) and pickedUpStones > 0:
                holes[currentHole - 1] += 1
                pickedUpStones = pickedUpStones - 1
                currentHole += 1
            if pickedUpStones == 0:
                break
            if holes == startHoles:
                self.scores[player.playerID - 1] += 1
                pickedUpStones = pickedUpStones - 1
                playAgain = True
            tempHoles = holes
            holes = enemyHoles
            enemyHoles = tempHoles
            currentHole = 1

        if not playAgain and holes == startHoles and holes[currentHole - 2] == 1:
            self.scores[player.playerID - 1] += enemyHoles[(HOLES - currentHole) + 1]
            enemyHoles[(HOLES - currentHole) + 1] = 0
            self.scores[player.playerID - 1] += 1

        if self.is_over():
            self.scores[0] += sum(self.holesPlayer1)
            self.holesPlayer1 = [0 for _ in range(HOLES)]
            self.scores[1] += sum(self.holesPlayer2)
            self.holesPlayer2 = [0 for _ in range(HOLES)]
            return False

        return playAgain

    def has_player_won(self, playerID: int):
        return self.scores[playerID - 1] > self.scores[2 - playerID] if self.is_over() else False

    def get_players_holes(self, playerID: int) -> List[int]:
        return self.holesPlayer1 if playerID == 1 else self.holesPlayer2

    def is_over(self):
        return sum(self.holesPlayer1) == 0 or sum(self.holesPlayer2) == 0

    def run(self, player1: Player, player2: Player):
        self.reset()
        currentPlayer = player1
        otherPlayer = player2
        while not self.is_over():
            again = True
            while again:
                move = currentPlayer.choose_move(self)
                again = self.move(currentPlayer, move)
            temp = currentPlayer
            currentPlayer = otherPlayer
            otherPlayer = temp

        # if self.has_player_won(currentPlayer.playerID):
        #     print("Player", currentPlayer, " won")
        # elif self.has_player_won(otherPlayer.playerID):
        #     print("Player", otherPlayer, " won")
        # else:
        #     print("DRAW")
        # print("Scores ["+str(self.scores[0]) + ","+str(self.scores[1])+"]")
