class Solution:
    def longestOnes(self, nums: list[int], k: int) -> int:
        left = 0
        zero_count = 0
        max_len = 0

        for right in range(len(nums)):
            if nums[right] == 0:
                zero_count += 1

            while zero_count > k:
                if nums[left] == 0:
                    zero_count -= 1
                left += 1

            max_len = max(max_len, right - left + 1)

        return max_len
    

sol = Solution()

# Test 1 - the original example we traced together
print(sol.longestOnes([1,1,1,0,0,0,1,1,1,1,0], 2))   # expected: 6

# Test 2 - your longer array
print(sol.longestOnes([1,1,1,0,0,0,1,1,1,1,0,0,1,1], 2))   # let's see what this gives