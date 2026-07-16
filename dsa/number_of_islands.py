class Solution:
    def numIslands(self, grid):
        count = 0

        def dfs(row, col):
            # boundary check
            if row < 0 or row >= len(grid):
                return
            if col < 0 or col >= len(grid[0]):
                return
            # water or visited
            if grid[row][col] == "0":
                return

            grid[row][col] = "0"  # mark visited

            # check all 4 directions
            dfs(row+1, col)  # down
            dfs(row-1, col)  # up
            dfs(row, col+1)  # right
            dfs(row, col-1)  # left

        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col] == "1":
                    count += 1
                    dfs(row, col)

        return count

sol = Solution()
print(sol.numIslands([
    ["1","1","0"],
    ["1","0","0"],
    ["0","0","1"]
]))  # 2

print(sol.numIslands([
    ["1","1","1","1","0"],
    ["1","1","0","1","0"],
    ["1","1","0","0","0"],
    ["0","0","0","0","0"]
]))  # 1