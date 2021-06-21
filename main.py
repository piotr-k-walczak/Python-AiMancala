from tkinter import Tk

from AbPlayer import AbPlayer
from Board import Board
from Heuristic import beating_comparison, simple_score_comparison
from MinMaxPlayer import MinMaxPlayer
from RandomPlayer import RandomPlayer
from HumanPlayer import HumanPlayer
from UI import UI
from Player import Player

def run(p1, p2):
    root = Tk()
    app = UI(root, p1, p2)
    root.mainloop()

def run_hidden(depth1=5, depth2=5, heuristic1=simple_score_comparison, heuristic2=simple_score_comparison):
    board = Board()
    p1 = MinMaxPlayer(1, depth=depth1, heuristics=heuristic1)
    p2 = MinMaxPlayer(2, depth=depth2, heuristics=heuristic2)
    board.run(p1, p2)
    if board.has_player_won(1):
        results.append((p1.time_counter, p1.move_counter, p1.checked_moves_counter))
    elif board.has_player_won(2):
        results.append((p2.time_counter, -p2.move_counter, p2.checked_moves_counter))
    else:
        results.append((p2.time_counter, p2.move_counter, p2.checked_moves_counter))
#
# for i in range(8):
#     results = []
#     run_hidden(i + 1, i+1, beating_comparison, beating_comparison)
#
#     time_avg = sum([res[0] for res in results]) / len(results)
#     ch_m_avg = sum([res[2] for res in results]) / len(results)
#     print("Beating " + str(i+1) +" " + str(ch_m_avg) + " " + str(str(time_avg)))

heuristics = [simple_score_comparison, beating_comparison]

for h1 in range(len(heuristics)):
    for h2 in range(len(heuristics)):
        print("H1(" + ("Simple)" if h1 == 0 else "Beating)") + "H2(" + (
            "Simple)" if h2 == 0 else "Beating)"))
        for i in range(3, 10):
            for k in range(3, 10):
                results = []
                run_hidden(i+1, k+1, heuristics[h1], heuristics[h2])
                print(str(i+1) + " " + str(k+1) + " " + str(results[0][1]))


