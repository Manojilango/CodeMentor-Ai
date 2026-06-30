class Solution:
    def isValid(self, s:str):
        stack=[]
        close_to_open = {')': '(', ']': '[', '}': '{'}

        for c in s:
            if c in close_to_open:
                if stack and stack[-1] == close_to_open[c]:
                    stack.pop()
                else:
                    return False
            else:
                stack.append(c)
        return not stack 