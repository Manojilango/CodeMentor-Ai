class Solution:
    def subsets(self, nums):
        result = []

        def backtrack(start, current):
            result.append(list(current))  # save EVERY time!

            for i in range(start, len(nums)):
                current.append(nums[i])
                backtrack(i+1, current)   # i+1 = no reuse!
                current.pop()

        backtrack(0, [])
        return result

sol = Solution()
print(sol.subsets([1,2,3]))
print(sol.subsets([0]))