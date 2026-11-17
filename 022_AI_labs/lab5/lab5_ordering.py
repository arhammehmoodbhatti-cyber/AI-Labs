from lab5_alphabeta import alphabeta

scores = [3, 5, 2, 9, 3, 5, 2, 9]
depth = 3

for name, order in [("Left first", (0, 1)), ("Right first", (1, 0))]:
    counter = [0]
    result = alphabeta(0, 0, True, scores, depth,
                       float("-inf"), float("inf"), counter, order)
    print(name, "root value:", result, "leaves evaluated:", counter[0])
