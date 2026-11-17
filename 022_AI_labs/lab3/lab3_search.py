from collections import deque

graph = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": [],
    "E": ["G"],
    "F": [],
    "G": []
}

def bfs(start, goal):
    queue = deque([(start, [start])])
    seen = {start}
    order = []
    while queue:
        node, path = queue.popleft()
        order.append(node)
        if node == goal:
            return path, order
        for nxt in graph.get(node, []):
            if nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, path + [nxt]))
    return None, order

def dfs(start, goal):
    stack = [(start, [start])]
    seen = set()
    order = []
    while stack:
        node, path = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        order.append(node)
        if node == goal:
            return path, order
        for nxt in reversed(graph.get(node, [])):
            if nxt not in seen:
                stack.append((nxt, path + [nxt]))
    return None, order

if __name__ == "__main__":
    for name, search in [("BFS", bfs), ("DFS", dfs)]:
        path, order = search("A", "G")
        print(name, "path:", " -> ".join(path or []))
        print(name, "processed:", order)
