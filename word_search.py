class Solution:
    def exist(self, board, word):
        rows, cols = len(board), len(board[0])

        def backtrack(r, c, index):
            if index == len(word):
                return True

            if (r < 0 or r >= rows or c < 0 or c >= cols or
                board[r][c] != word[index]):
                return False

            temp = board[r][c]
            board[r][c] = "#"

            found = (
                backtrack(r-1, c, index+1) or  # up
                backtrack(r+1, c, index+1) or  # down
                backtrack(r, c-1, index+1) or  # left
                backtrack(r, c+1, index+1)     # right
            )

            board[r][c] = temp

            return found

        for i in range(rows):
            for j in range(cols):
                if backtrack(i, j, 0):
                    return True

        return False

sol = Solution()
board = [
  ['A','B','C','E'],
  ['S','F','C','S'],
  ['A','D','E','E']
]
print(sol.exist(board, "ABCCED"))  # True
print(sol.exist(board, "SEE"))     # True
print(sol.exist(board, "ABCB"))    # False