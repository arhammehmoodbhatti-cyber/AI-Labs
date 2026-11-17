from math import ceil, log2

scores = [3, 5, 2, 9, 0, 7]
depth = ceil(log2(len(scores)))
scores = scores + [0] * (2 ** depth - len(scores))

def minimax(level, index, maximizing, values, target, counter):
    if level == target:
        counter[0] += 1
        return values[index]
    left = minimax(level + 1, index * 2, not maximizing, values, target, counter)
    right = minimax(level + 1, index * 2 + 1, not maximizing, values, target, counter)
    return max(left, right) if maximizing else min(left, right)

if __name__ == "__main__":
    counter = [0]
    value = minimax(0, 0, True, scores, depth, counter)
    print("Leaf values:", scores)
    print("Root value:", value)
    print("Leaves evaluated:", counter[0])
    print("Padded tree depth:", depth)
