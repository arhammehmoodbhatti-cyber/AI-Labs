import heapq

graph = {
    "A": [("B", 1), ("C", 8)],
    "B": [("D", 1), ("E", 1)],
    "C": [("F", 2), ("G", 4)],
    "D": [], "E": [("G", 1)], "F": [], "G": []
}

def ucs(start, goal):
    queue = [(0, start, [start])]
    best = {start: 0}
    order = []
    while queue:
        cost, node, path = heapq.heappop(queue)
        if cost != best.get(node):
            continue
        order.append(node)
        if node == goal:
            return cost, path, order
        for nxt, weight in graph.get(node, []):
            new_cost = cost + weight
            if new_cost < best.get(nxt, float("inf")):
                best[nxt] = new_cost
                heapq.heappush(queue, (new_cost, nxt, path + [nxt]))
    return None, None, order

def path_cost(path):
    total = 0
    for a, b in zip(path, path[1:]):
        total += next(w for n, w in graph[a] if n == b)
    return total

if __name__ == "__main__":
    cost, path, order = ucs("A", "G")
    bfs_path = ["A", "C", "G"]
    print("UCS path:", " -> ".join(path), "cost:", cost)
    print("UCS processed:", order)
    print("Independent cost:", path_cost(path))
    print("BFS route:", " -> ".join(bfs_path), "cost:", path_cost(bfs_path))
    assert cost == path_cost(path) == 3
