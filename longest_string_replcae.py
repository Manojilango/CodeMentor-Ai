class Solution:
    def moveZeroes(self, nums):
        slow = 0
        for fast in range(len(nums)):
            if nums[fast] != 0:
                nums[slow], nums[fast] = nums[fast], nums[slow]
                slow += 1
        return nums

sol = Solution()
print(sol.moveZeroes([0,1,0,3,12]))
print(sol.moveZeroes([0,0,1]))