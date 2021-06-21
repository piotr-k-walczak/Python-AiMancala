from tkinter import *
from Board import *
from Config import *
from HumanPlayer import HumanPlayer
from Player import *


class UI:
    def __init__(self, master, p1: Player, p2: Player):
        self.board = Board()
        self.p1 = self.currentPlayer = p1
        self.p2 = self.otherPlayer = p2
        self.root = master

        frame = Frame(master)
        frame.pack()

        self.status = Label(frame, text="Press 'Start' to Begin")
        self.status.config(font=("Courier", 44))
        self.status.pack(side=TOP)
        self.generate_board(frame)
        self.button = Button(frame, text="Start!", command=self.new_game)
        self.button.config(font=("Courier", 44))
        self.button.pack(side=TOP)

    def generate_board(self, frame):
        boardFrame = Frame(frame)
        boardFrame.pack(side=TOP)

        holesFrame = Frame(boardFrame)
        topRow = Frame(holesFrame)
        bottomRow = Frame(holesFrame)
        topRow.pack(side=TOP)
        bottomRow.pack(side=TOP)

        holeWidth = TOTAL_BOARD_WIDTH / HOLES
        holeHeight = WINDOW_HEIGHT / 2

        self.holes = [[], []]
        for i in range(HOLES):
            c = Canvas(bottomRow, width=holeWidth, height=holeHeight)
            c.pack(side=LEFT)
            self.holes[0] += [c]
            c = Canvas(topRow, width=holeWidth, height=holeHeight)
            c.pack(side=LEFT)
            self.holes[1] += [c]

        self.masterHoleP1 = Canvas(boardFrame, width=MASTER_HOLE_WIDTH, height=WINDOW_HEIGHT)
        self.masterHoleP2 = Canvas(boardFrame, width=MASTER_HOLE_WIDTH, height=WINDOW_HEIGHT)

        self.masterHoleP2.pack(side=LEFT)
        holesFrame.pack(side=LEFT)
        self.masterHoleP1.pack(side=LEFT)

        self.generate_element_images()

    def generate_element_images(self):
        self.masterHoleP2.create_rectangle(0, 0, MASTER_HOLE_WIDTH, 0.9 * WINDOW_HEIGHT, width=2, fill="blue")
        for j in [0, 1]:
            for i in range(HOLES):
                self.holes[j][i].create_rectangle(0, 0, TOTAL_BOARD_WIDTH / HOLES, WINDOW_HEIGHT / 2, fill=("green" if j == 0 else "blue"))
        self.masterHoleP1.create_rectangle(0, 0 + 0.1 * WINDOW_HEIGHT, MASTER_HOLE_WIDTH, WINDOW_HEIGHT, width=2, fill="green")

    def new_game(self):
        self.board.reset()
        self.currentPlayer = self.p1
        self.otherPlayer = self.p2
        s = "Player " + str(self.currentPlayer) + "'s turn."
        self.status['text'] = s
        self.reset()
        self.next_turn()

    def next_turn(self):
        self.root.update()
        if self.board.is_over():
            if self.board.has_player_won(self.p1.playerID):
                self.status['text'] = "Player " + str(self.p1) + " won"
            elif self.board.has_player_won(self.p2.playerID):
                self.status['text'] = "Player " + str(self.p2) + " won"
            else:
                self.status['text'] = "It is a draw"
            return
        if isinstance(self.currentPlayer, HumanPlayer):
            self.enable_clicks()
        else:
            move = self.currentPlayer.choose_move(self.board)
            playAgain = self.board.move(self.currentPlayer, move)
            if not playAgain:
                self.change_current_player()
            self.reset()
            self.next_turn()

    def enable_clicks(self):
        for i in [0, 1]:
            for j in range(HOLES):
                self.holes[i][j].bind("<Button-1>", self.on_click)

    def disable_clicks(self):
        for i in [0, 1]:
            for j in range(HOLES):
                self.holes[i][j].unbind("<Button-1>")

    def change_current_player(self):
        temp = self.currentPlayer
        self.currentPlayer = self.otherPlayer
        self.otherPlayer = temp
        self.status['text'] = "Player " + str(self.currentPlayer) + "\'s turn."

    def reset(self):
        for i in range(len(self.board.holesPlayer2)):
            index = (len(self.board.holesPlayer2) - i) - 1
            self.clear_hole(self.holes[1][index])
            self.holes[1][index].create_text(HOLE_WIDTH / 2, 0.05 * WINDOW_HEIGHT, text=str(self.board.holesPlayer2[i]), tag="num")
        for i in range(len(self.board.holesPlayer1)):
            self.clear_hole(self.holes[0][i])
            self.holes[0][i].create_text(HOLE_WIDTH / 2, 0.05 * WINDOW_HEIGHT, text=str(self.board.holesPlayer1[i]), tag="num")
        self.clear_hole(self.masterHoleP1)
        self.clear_hole(self.masterHoleP2)
        self.masterHoleP2.create_text(MASTER_HOLE_WIDTH / 2, 10, text=str(self.board.scores[1]), tag="num")
        self.masterHoleP1.create_text(MASTER_HOLE_WIDTH / 2, 10 + 0.1 * WINDOW_HEIGHT, text=str(self.board.scores[0]), tag="num")

    def clear_hole(self, cup: Canvas):
        cup.delete(cup.find_withtag("num"))
        cup.delete(cup.find_withtag("stone"))

    def on_click(self, event):
        moveAgain = True
        self.disable_clicks()
        if self.currentPlayer.playerID == 1:
            for i in range(len(self.holes[0])):
                if self.holes[0][i] == event.widget:
                    if self.board.isMoveLegal(self.currentPlayer, i + 1):
                        moveAgain = self.board.move(self.currentPlayer, i + 1)
                        if not moveAgain:
                            self.change_current_player()
                        self.reset()
        else:
            for i in range(len(self.holes[1])):
                if self.holes[1][i] == event.widget:
                    index = HOLES - i
                    if self.board.isMoveLegal(self.currentPlayer, index):
                        moveAgain = self.board.move(self.currentPlayer, index)
                        if not moveAgain:
                            self.change_current_player()
                        self.reset()
        if moveAgain:
            self.enable_clicks()
        else:
            self.next_turn()
