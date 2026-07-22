class Solution:
    def uniquePaths(self, m, n):
        dp = [[1] * n for i in range(m)]
        for i in range(1, m):
            for j in range(1, n):
                dp[i][j] = dp[i-1][j] + dp[i][j-1]
        return dp[m-1][n-1]

sol = Solution()
print(sol.uniquePaths(3, 7))   # 28
print(sol.uniquePaths(3, 2))   # 3
