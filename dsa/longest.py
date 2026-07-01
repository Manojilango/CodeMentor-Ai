class Solution:
    def longestConsecutive(self, nums):
        num_set = set(nums)
        longest = 0

        for num in num_set:
            # only start counting if this is the START of a sequence
            if num - 1 not in num_set:
                length = 1
                while num + length in num_set:
                    length += 1
                longest = max(longest, length)

        return longest


sol = Solution()
print(sol.longestConsecutive([100, 4, 200, 1, 3, 2]))  # 4