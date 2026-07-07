class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        seen = set()    # characters in current window
        left = 0        # left pointer
        max_len = 0     # longest window found

        for right in range(len(s)):
           
            while s[right] in seen:
                seen.remove(s[left])
                left += 1
           
            seen.add(s[right])
          
            max_len = max(max_len, right - left + 1)

        return max_len

sol = Solution()
print(sol.lengthOfLongestSubstring("abcabcbb"))  
print(sol.lengthOfLongestSubstring("bbbbb"))     
print(sol.lengthOfLongestSubstring("pwwkew"))    