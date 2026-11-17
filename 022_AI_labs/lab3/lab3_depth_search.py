from collections import deque

graph = {
    "A": ["B", "C"], "B": ["D", "E"], "C": ["F"],
    "D": [], "E": ["G"], "F": [], "G": []
}

def dls(start, goal, limit):
    def visit(node, path, depth):
        if node == goal:
            return "FOUND", path
        if depth == limit:
            if graph.get(node, []):
                return "CUTOFF", None
            return "FAILURE", None
        cutoff = False
        for nxt in graph.get(node, []):
            if nxt in path:
                continue
            status, result = visit(nxt, path + [nxt], depth + 1)
            if status == "FOUND":
                return status, result
            if status == "CUTOFF":
                cutoff = True
        return ("CUTOFF", None) if cutoff else ("FAILURE", None)
    return visit(start, [start], 0)

def iddfs(start, goal, maximum):
    attempts = []
    for limit in range(maximum + 1):
        status, path = dls(start, goal, limit)
        attempts.append((limit, status, path))
        if status == "FOUND":
            break
    return attempts

if __name__ == "__main__":
    print("DLS")
    for limit in range(1, 5):
        status, path = dls("A", "G", limit)
        print("limit", limit, status, path)
    print("IDDFS")
    for limit, status, path in iddfs("A", "G", 4):
        print("limit", limit, status, path)
    assert dls("A", "G", 2)[0] == "CUTOFF"
    assert dls("A", "G", 3)[0] == "FOUND"
    assert dls("A", "Z", 4)[0] == "FAILURE"
