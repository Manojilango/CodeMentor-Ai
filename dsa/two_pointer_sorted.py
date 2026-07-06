class Solution: 
    def towsum(self, arr, target):
        left=0
        right=len(arr)-1


        while left<right:
            current_sum= arr[left] + arr[right]
        
            if current_sum==target:
                return True 
            elif current_sum < target:
                left+=1
            else:
                right-=1
        return False
    
sol=Solution()
print(sol.towsum([1,2,3,4,5],9))
print(sol.towsum([1,2,3,4,5],10))