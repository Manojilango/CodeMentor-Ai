def subsets(nums):
    result = []
    
    def backtrack(index, path):
        if index == len(nums):        # reached the end — done deciding
            result.append(path[:])     # save this complete path
            return
        
        # Choice 1: DON'T include nums[index]
        backtrack(index + 1, path)
        
        # Choice 2: DO include nums[index]
        path.append(nums[index])       # CHOOSE
        backtrack(index + 1, path)      # EXPLORE
        path.pop()                       # UN-CHOOSE
    
    backtrack(0, [])
    return result