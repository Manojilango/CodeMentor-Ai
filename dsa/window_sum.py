class Solution:
    def minSubArrayLen(self, target, nums):
        left = 0
        window_sum = 0
        min_len = float('inf')

        for right in range(len(nums)):
            window_sum += nums[right]

            while window_sum >= target:
                min_len = min(min_len, right - left + 1)
                window_sum -= nums[left]
                left += 1

        return min_len if min_len != float('inf') else 0


sol = Solution()
nums = [2, 3, 1, 2, 4, 3]
target = 7
print(sol.minSubArrayLen(target, nums))   # expected: 2