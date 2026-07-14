from collections import deque   # ← this must be the FIRST line


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def dfs(node):
    if not node:
        return
    print(node.val)
    dfs(node.left)
    dfs(node.right)


def bfs(root):
    if not root:
        return
    queue = deque([root])
    while queue:
        node = queue.popleft()
        print(node.val)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)


root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
root.left.left = TreeNode(4)
root.left.right = TreeNode(5)

print("DFS:")
dfs(root)

print("BFS:")
bfs(root)