class Solution:
    def topKFrequent(self, nums: list[int], k: int) -> list[int]:
        
        # Step 1 — count frequency
        freq = {}
        for num in nums:
            freq[num] = freq.get(num, 0) + 1
        # freq = {1:3, 2:2, 3:1}

        # Step 2 — sort by frequency + take top k
        return sorted(freq, key=lambda x: freq[x], reverse=True)[:k]
        # sorted = [1,2,3] → [:2] = [1,2]

sol = Solution()
print(sol.topKFrequent([1,1,1,2,2,3], 2))  # [1, 2]
print(sol.topKFrequent([1], 1))             # [1]
print(sol.topKFrequent([1,2], 2))           # [1, 2]                                                                  