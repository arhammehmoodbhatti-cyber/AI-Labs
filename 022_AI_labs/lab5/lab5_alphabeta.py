from math import log2

scores = [3, 5, 2, 9, 3, 5, 2, 9]
depth = int(log2(len(scores)))

def alphabeta(level, index, maximizing, values, target, alpha, beta, counter, order=(0, 1)):
    if level == target:
        counter[0] += 1
        return values[index]
    if maximizing:
        best = float("-inf")
        for child in order:
            result = alphabeta(level + 1, index * 2 + child, False,
                               values, target, alpha, beta, counter, order)
            best = max(best, result)
            alpha = max(alpha, best)
            if alpha >= beta:
                break
        return best
    best = float("inf")
    for child in order:
        result = alphabeta(level + 1, index * 2 + child, True,
                           values, target, alpha, beta, counter, order)
        best = min(best, result)
        beta = min(beta, best)
        if alpha >= beta:
            break
    return best

if __name__ == "__main__":
    counter = [0]
    value = alphabeta(0, 0, True, scores, depth,
                      float("-inf"), float("inf"), counter)
    print("Leaf values:", scores)
    print("Root value:", value)
    print("Leaves evaluated:", counter[0])
