from collections import deque

# Graph as adjacency list
graph = {
    1: [2, 3],
    2: [1, 4],
    3: [1, 4],
    4: [2, 3]
}

# BFS
def bfs_graph(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)

    while queue:
        node = queue.popleft()
        print(node, end=" ")
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

# DFS
def dfs_graph(graph, node, visited=None):
    if visited is None:
        visited = set()
    visited.add(node)
    print(node, end=" ")
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_graph(graph, neighbor, visited)

# Test
print("BFS: ", end="")
bfs_graph(graph, 1)    # 1 2 3 4

print("\nDFS: ", end="")
dfs_graph(graph, 1)    # 1 2 4 3