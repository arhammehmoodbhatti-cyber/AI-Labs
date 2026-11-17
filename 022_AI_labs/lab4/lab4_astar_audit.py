import heapq

graph = {
    "S": [("A", 1), ("B", 4)],
    "A": [("C", 2)],
    "B": [("G", 5)],
    "C": [("G", 3)],
    "G": []
}
heuristic = {"S": 5, "A": 4, "B": 4, "C": 2, "G": 0}

def astar(h):
    queue = [(h["S"], 0, "S", ["S"])]
    best = {"S": 0}
    processed = []
    expanded = []
    trace = []
    while queue:
        f, g, node, path = heapq.heappop(queue)
        if g != best.get(node):
            continue
        processed.append(node)
        trace.append((node, g, h[node], f, sorted((x[2], x[1], x[0]) for x in queue)))
        if node == "G":
            return g, path, processed, expanded, trace
        expanded.append(node)
        for nxt, weight in graph[node]:
            new_g = g + weight
            if new_g < best.get(nxt, float("inf")):
                best[nxt] = new_g
                heapq.heappush(queue, (new_g + h[nxt], new_g, nxt, path + [nxt]))
    return None, None, processed, expanded, trace

def route_cost(path):
    return sum(next(w for n, w in graph[a] if n == b) for a, b in zip(path, path[1:]))

def audit(h):
    rows = []
    for node, edges in graph.items():
        for nxt, cost in edges:
            rows.append((node, nxt, h[node], cost + h[nxt], h[node] <= cost + h[nxt]))
    return rows

if __name__ == "__main__":
    for label, h in [("A* supplied", heuristic), ("UCS", {n: 0 for n in graph}),
                     ("A* overestimate", {**heuristic, "C": 10})]:
        cost, path, processed, expanded, trace = astar(h)
        print("\n", label)
        print("path:", path, "cost:", cost, "independent:", route_cost(path))
        print("processed:", processed)
        print("expanded:", expanded, "count:", len(expanded))
        for row in trace[:3]:
            print("frontier step:", row)
    print("\nConsistency audit")
    for row in audit(heuristic):
        print(row)
    assert astar(heuristic)[0] == 6
    assert astar({n: 0 for n in graph})[0] == 6
    assert astar({**heuristic, "C": 10})[0] == 9
