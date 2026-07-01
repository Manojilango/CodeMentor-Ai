class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        count = 0
        running_sum = 0
        sums_seen = {0: 1}

        for num in nums:
            running_sum += num
            complement = running_sum - k

            if complement in sums_seen:
                count += sums_seen[complement]

            sums_seen[running_sum] = sums_seen.get(running_sum, 0) + 1

        return count
    
sol = Solution()
print(sol.subarraySum([1,1,1], 2))    # expected: 2
print(sol.subarraySum([1,2,3], 3))    # expected: 2