class Solution:
    def threeSum(self, nums):
        nums.sort()                    # Step 1 - sort (needed for two pointers)
        result = []                    # empty basket to collect triplets

        for i in range(len(nums)):
            # Skip duplicate values for nums[i]
            if i > 0 and nums[i] == nums[i-1]:
                continue

            left = i + 1
            right = len(nums) - 1
            target = -nums[i]          # what left+right need to sum to

            while left < right:
                current_sum = nums[left] + nums[right]

                if current_sum == target:
                    result.append([nums[i], nums[left], nums[right]])
                    left += 1
                    right -= 1

                    # Skip duplicates for left and right too
                    while left < right and nums[left] == nums[left-1]:
                        left += 1
                    while left < right and nums[right] == nums[right+1]:
                        right -= 1

                elif current_sum < target:
                    left += 1
                else:
                    right -= 1

        return result


sol = Solution()
print(sol.threeSum([-1, 0, 1, 2, -1, -4]))
# expected: [[-1, -1, 2], [-1, 0, 1]]