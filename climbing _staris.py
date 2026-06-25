class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 2:
            return n
        
        a = 1
        b = 2
        
        for i in range(3, n + 1):
            a, b = b, a + b
        
        return b

sol = Solution()
print(sol.climbStairs(3))  
print(sol.climbStairs(4)) 
print(sol.climbStairs(5))  