class Solution:
    def is_valid(self, s):
        stack = []
        pairs = {')': '(', '}': '{', ']': '['}
        for char in s:
            if char in '([{':
                stack.append(char)
            else:
                if not stack or stack[-1] != pairs[char]:
                    return False
                stack.pop()
        return len(stack) == 0


sol = Solution()
print(sol.is_valid("()"))       # expected: True
print(sol.is_valid("()[]{}"))   # expected: True
print(sol.is_valid("(]"))       # expected: False
print(sol.is_valid(")("))       # expected: False