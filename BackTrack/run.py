import time

from killer_sudoku import KillerSudoku
import cProfile
import pandas as pd


if __name__ == "__main__":
    N = 9
    initial_matrix = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    cage_constraints = [
        (3, [(1, 1), (1, 2)]),
        (15, [(1, 3), (1, 4), (1, 5)]),
        (22, [(1, 6), (2, 5), (2, 6), (3, 5)]),
        (4, [(1, 7), (2, 7)]),
        (16, [(1, 8), (2, 8)]),
        (15, [(1, 9), (2, 9), (3, 9), (4, 9)]),
        (25, [(2, 1), (2, 2), (3, 1), (3, 2)]),
        (17, [(2, 3), (2, 4)]),
        (9, [(3, 3), (3, 4), (4, 4)]),
        (8, [(3, 6), (4, 6), (5, 6)]),
        (20, [(3, 7), (3, 8), (4, 7)]),
        (6, [(4, 1), (5, 1)]),
        (14, [(4, 2), (4, 3)]),
        (17, [(4, 5), (5, 5), (6, 5)]),
        (17, [(4, 8), (5, 7), (5, 8)]),
        (13, [(5, 2), (5, 3), (6, 2)]),
        (20, [(5, 4), (6, 4), (7, 4)]),
        (12, [(5, 9), (6, 9)]),
        (27, [(6, 1), (7, 1), (8, 1), (9, 1)]),
        (6, [(6, 3), (7, 2), (7, 3)]),
        (20, [(6, 6), (7, 6), (7, 7)]),
        (6, [(6, 7), (6, 8)]),
        (10, [(7, 5), (8, 4), (8, 5), (9, 4)]),
        (14, [(7, 8), (7, 9), (8, 8), (8, 9)]),
        (8, [(8, 2), (9, 2)]),
        (16, [(8, 3), (9, 3)]),
        (15, [(8, 6), (8, 7)]),
        (13, [(9, 5), (9, 6), (9, 7)]),
        (17, [(9, 8), (9, 9)]),
    ]

    killer_log = []
    normal_log = []
    for N in [4, 9, 16]:
        initial_matrix = [list(0 for _ in range(N)) for _ in range(N)]
        for l in range(2, N):
            cage_constraints = eval(open(f"../sudokus/{N}_{l}_killer.txt").read())
            
            print("Killer", N, l)

            for i in range(1):
                sudoku = KillerSudoku(N, initial_matrix, cage_constraints)
                t = sudoku.solve()
                killer_log.append(("backtrack with new rules", N, l, t))
            log = pd.DataFrame(killer_log, columns=["method", "N", "Max cage length", "Time"])
            log.to_csv("killer_temp.csv")

            # for i in range(3):
            #     sudoku = KillerSudoku(N, initial_matrix, cage_constraints, False)
            #     t = sudoku.solve()
            #     killer_log.append(("backtrack with no new rules", N, l, t))
            # log = pd.DataFrame(killer_log, columns=["method", "N", "Max cage length", "Time"])
            # log.to_csv("killer_temp.csv")
            # log = pd.DataFrame(normal_log, columns=["N", "Empty cell percentage", "Time"])
            # log.to_csv("normal_temp.csv")

        for p in range(5, 100, 5):
            p = float(p / 100.0)
            matrix = eval(open(f"../sudokus/{N}_{p:.2f}_normal.txt").read())

            print("Normal", N, p)

            for i in range(3):
                sudoku = KillerSudoku(N, matrix, [])
                t = sudoku.solve()
                normal_log.append((N, p, t))

            log = pd.DataFrame(normal_log, columns=["N", "Empty cell percentage", "Time"])
            log.to_csv("normal_temp.csv")

    # log = pd.DataFrame(killer_log, columns=["method", "N", "Max cage length", "Time"])
    # log.to_csv("killer.csv")
    # log = pd.DataFrame(normal_log, columns=["N", "Empty cell percentage", "Time"])
    # log.to_csv("normal.csv")

    # cProfile.run('KillerSudoku(N, initial_matrix, cage_constraints).solve()')

    # sudoku = KillerSudoku(N, initial_matrix, cage_constraints)
    # sudoku.solve()
